"""Updates an existing group policy with additional changes

Notes: Make sure to update the settings.toml file with
    network_list: This is a file containing network ID, network name
    new_group_policy: This is the json formated file with policy changes
    existing_name: This is the current name of the group policy

Meraki API
https://developer.cisco.com/meraki/api/update-network-group-policy/

"""

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
    print()
    if "q" in choice:
        log.info("You chose not to continue")
        sys.exit()
    networks = fileops.load_file(networks_file)
    policy = fileops.load_file(group_policies, "json")
    # Loop through each network updating the specified group policy
    dashboard = merakiops.get_dashboard()
    done = 0
    total = len(networks)
    for network in networks:
        bar = fileops.progress_bar(done, total)
        print(bar, end="", flush=True)
        if network.startswith("L_") or network.startswith("N_"):
            network_id = network.split(",")[0]
            network_name = network.split(",")[1]
            log.info(f"Checking {network_name.strip()} for existing policy")
            response = dashboard.networks.getNetworkGroupPolicies(network_id)
            policy_found = False
            for each in response:
                if each["name"] == existing_name:
                    group_policy_id = each["groupPolicyId"]
                    dashboard.networks.updateNetworkGroupPolicy(
                        network_id, group_policy_id, contentFiltering=policy
                    )
                    log.info(f"Group policy ID {group_policy_id} updated")
                    policy_found = True
            if not policy_found:
                log.info(f"Did not find a policy with name {existing_name}")
        done += 1
        print("\b" * len(bar), end="", flush=True)
    bar = fileops.progress_bar(done, total)
    print(bar, end="", flush=True)
    log.info("Script completed successfully.")
    print(f"\n\nScript completed successfully. See output/logs for details")


if __name__ == "__main__":
    main()
