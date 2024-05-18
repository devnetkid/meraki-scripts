"""Frequently used functions for accessing the Meraki dashboard"""

import os
import sys

import meraki

from meraki_scripts.universal import fileops


def get_dashboard(key=None, print_console=False, output_log=False):
    """Instantiate the Meraki dashboard

    Args:
        key (str): The API KEY
        print_console (bool): Flag used to determine writing to CLI
        output_log (bool): Flag used to determine writing to logs

    Returns:
        DashboardAPI
    """

    # Load settings and check for api key
    settings = fileops.load_settings()
    if settings["meraki"]["api_key"]:
        key = settings["meraki"]["api_key"]

    # TODO: look into log_file_prefix=os.path.basename(__file__)
    if key:
        try:
            return meraki.DashboardAPI(
                key,
                output_log=output_log,
                print_console=print_console,
                suppress_logging=True,
            )
        except AttributeError as e:
            sys.exit("Make sure meraki library is installed. Try `pip install meraki`")

    if "MERAKI_DASHBOARD_API_KEY" in os.environ:
        try:
            return meraki.DashboardAPI(
                output_log=False, print_console=False, suppress_logging=True
            )
        except AttributeError as e:
            sys.exit("Make sure meraki library is installed. Try `pip install meraki`")

    sys.exit("MERAKI_DASHBOARD_API_KEY not found.")


def validate_integer_in_range(end_range):
    while True:
        try:
            selected = int(input("\nOption >> "))
            assert selected in range(1, end_range + 1)
        except ValueError:
            print("\tThat is not an integer!\n")
        except AssertionError:
            print(f"\n\tYou must enter a number between 1 and {end_range}")
        else:
            break
    print()
    return selected - 1


def select_organization(dashboard):
    """Lists all the organizations and prompts the user to select one

    Args:
        dashboard (object): An instance of the Meraki dashboard
    Returns:
        A tuple containing organization ID and name
    """
    organizations = dashboard.organizations.getOrganizations()
    organizations.sort(key=lambda x: x["name"])
    print("\nSelect an organization:\n")
    for line_num, organization in enumerate(organizations, start=1):
        row = fileops.colorme((f'  {line_num} - {organization["name"]}'), "green")
        print(row)
    selected = validate_integer_in_range(len(organizations))
    return (
        organizations[int(selected)]["id"],
        organizations[int(selected)]["name"],
    )


def select_network(dashboard, org, lines_to_display=25):
    """Lists the organization networks and prompts user to select one

    Args:
        dashboard (obj): The Meraki dashboard instance
        org (str): The selected organization ID
        lines_to_display (int): The number of lines before pausing

    Returns:
        list: the selected network ID and network name
    """

    network_list = []
    networks = dashboard.organizations.getOrganizationNetworks(org)

    while not network_list:
        search_name = input(
            "Enter a name to search for or leave blank for all networks: "
        )
        if search_name:
            for network in networks:
                if search_name.lower() in network["name"].lower():
                    network_list.append(network)
        else:
            network_list = networks
        if network_list:
            network_list.sort(key=lambda x: x["name"])
            print("\nNetworks:")
            for line_num, net in enumerate(network_list, start=1):
                net_name = net["name"]
                print(f"{line_num} - {net_name}")
                if line_num % lines_to_display == 0:
                    user_response = input(
                        "\nPress Enter to continue, or q + Enter to quit search: "
                    )
                    if "q" in user_response:
                        break
        else:
            print(f"No networks found matching {search_name}")

    selected = validate_integer_in_range(len(network_list))
    return [network_list[int(selected)]["id"], network_list[int(selected)]["name"]]


def get_networks(dashboard, org):
    try:
        networks = dashboard.organizations.getOrganizationNetworks(org)
        return networks
    except meraki.APIError as e:
        print(f"reason = {e.reason}")


def get_mx_serial_number(dashboard, net_id):
    has_spare = False
    primary_mx_sn = None
    spare_mx_sn = None
    try:
        warm_spare = dashboard.appliance.getNetworkApplianceWarmSpare(net_id)
        if warm_spare["enabled"]:
            has_spare = True
            spare_mx_sn = warm_spare["spareSerial"]
        primary_mx_sn = warm_spare["primarySerial"]
        return (has_spare, primary_mx_sn, spare_mx_sn)
    except meraki.APIError as e:
        print(f"reason = {e.reason}")
        print(f"error = {e.message}")


def get_mx_uplink_information(dashboard, net_id):
    """Build a list of uplink information for MX(s) in given network"""

    # Check if given network has a spare MX
    try:
        mx_appliance = dashboard.appliance.getNetworkApplianceWarmSpare(net_id)
    except meraki.APIError as api_error:
        sys.exit(api_error.message)

    # Extract primary and spare serial numbers
    primary_mx_sn = mx_appliance["primarySerial"] or None
    spare_mx_sn = mx_appliance["spareSerial"] or None

    # If uplink has wan1 and/or wan2 grab info
    uplink_info = []
    if mx_appliance.get("wan1"):
        uplink_info.append({"wan1": mx_appliance["wan1"]})
    if mx_appliance.get("wan2"):
        uplink_info.append({"wan2": mx_appliance["wan2"]})

    # Pull uplink info for serial number
    if primary_mx_sn:
        try:
            pri_wan_info = dashboard.appliance.getDeviceApplianceUplinksSettings(
                primary_mx_sn
            )
            uplink_info.append({"primary_mx": pri_wan_info})
        except meraki.APIError as api_error:
            sys.exit(api_error.message)

    if spare_mx_sn:
        try:
            spare_wan_info = dashboard.appliance.getDeviceApplianceUplinksSettings(
                spare_mx_sn
            )
            uplink_info.append({"spare_mx": spare_wan_info})
        except meraki.APIError as api_error:
            sys.exit(api_error.message)

    return uplink_info


def delete_group_policies(dashboard, net_id):
    """Grab all group policies for a network ID and delete them"""

    # Return a list of all group policies for the given network
    response = dashboard.networks.getNetworkGroupPolicies(net_id)

    # Loop through each group policy to get the policy ID
    for group_policy in response:
        group_policy_id = group_policy["groupPolicyId"]

        # Delete the found group policy
        dashboard.networks.deleteNetworkGroupPolicy(net_id, group_policy_id)


def group_policy_exists(policy, group_policies):
    """For a given policy, check group policies for a match"""

    for group_policy in group_policies:
        if group_policy["name"] == policy:
            return group_policy
    
    return ""


def copy_group_policies(dashboard, src_net_id, policy_list, dst_list):
    """Copy policies from source network to destination network"""

    # Ensure that the policy_list provided is part of the src_net_id
    try:
        group_policies = dashboard.networks.getNetworkGroupPolicies(src_net_id)
    except Exception as e:
        print(str(e))
        sys.exit()

    for policy in policy_list:
        policy_source = group_policy_exists(policy, group_policies)
        if not policy_source: 
            sys.exit(f"The specified policy {policy} was not found in {src_net_id}")
            
        # Copy specified policies to destination networks
        print(policy_source)
        name = policy_source.get("name", "")
        splash_settings = policy_source.get("splashAuthSettings", "") 
        scheduling = policy_source.get("scheduling", {})
        bandwidth = policy_source.get("bandwidth", {})
        firewall = policy_source.get("firewallAndTrafficShaping", {})
        content_filtering = policy_source.get("contentFiltering", {})
        vlan_tagging = policy_source.get("vlanTagging", {})
        bonjour = policy_source.get("bonjourForwarding", {})

        # Loop through destination networks
        for network in dst_list:
            netinfo = network.split(',')
            net_id = netinfo[0]
            net_name = netinfo[1]

            dashboard.networks.createNetworkGroupPolicy(
                net_id, name, 
                scheduling=scheduling,
                bandwidth=bandwidth,
                firewallAndTrafficShaping=firewall,
                contentFiltering=content_filtering,
                splashAuthSettings=splash_settings, 
                vlanTagging=vlan_tagging,
                bonjourForwarding=bonjour
            )
