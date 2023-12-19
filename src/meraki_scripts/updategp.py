"""Updates an existing group policy with additional changes"""

import logging
import sys

from meraki_scripts.universal import fileops, merakiops

log = logging.getLogger(__name__)
fileops.setup_logging("updategp")


def main():
    settings = fileops.load_settings()
    fileops.clear_screen()
    print(fileops.colorme(settings["title"], "red"))
    log.info("Starting script updategp")
    settings = fileops.load_settings()
    log.debug("The settings have been loaded")
    networks_file = settings["updategp"]["network_list"]
    color_networks = fileops.colorme(networks_file, "blue")
    group_policies = settings["updategp"]["new_group_policy"]
    color_policies = fileops.colorme(group_policies, "blue")
    existing_name = settings["updategp"]["existing_name"]
    color_existing = fileops.colorme(existing_name, "blue")
    log.info(f"Loading the networks file named {networks_file}")
    print(f"\n  For the list of networks from {color_networks}")
    log.info(f"Loading the group policies file named {group_policies}")
    print(f"  Write the new group policy found in {color_policies}")
    log.info(f"The existing policy to search for is {existing_name}")
    print(f"  If there is an existing policy {color_existing}")
    # Get confirmation before continuing
    choice = input("\nPress [Enter] to continue or [q] to quit: ")
    if "q" in choice:
        log.info("You chose not to continue")
        sys.exit()
    networks = fileops.new_readlines(networks_file)
    policy = fileops.load_json_file(group_policies)
    dashboard = merakiops.get_dashboard()
    for network in networks:
        if network.startswith('L_') or network.startswith('N_'):
            network_id = network.split(',')[0]
            network_name = network.split(',')[1]
            log.info(f"Checking {network_name.strip()} for existing policy")
            response = dashboard.networks.getNetworkGroupPolicies(network_id)
            found_policy = False
            for each in response:
                if each['name'] == existing_name:
                    group_policy_id = each['groupPolicyId']
                    dashboard.networks.updateNetworkGroupPolicy(
                        network_id, group_policy_id, 
                        contentFiltering=policy
                    )
                    log.info(f"Group policy ID {group_policy_id} updated")
                    found_policy = True
            if not found_policy:
                log.info(f"Did not find a policy with name {existing_name}")


if __name__ == '__main__':
    main()
