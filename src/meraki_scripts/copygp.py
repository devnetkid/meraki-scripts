"""Copies group policies from a source network to a destination

Meraki API
https://developer.cisco.com/meraki/api/update-network-group-policy/

"""

import logging
import sys

from meraki_scripts.universal import fileops, merakiops

log = logging.getLogger(__name__)
fileops.setup_logging("copygp")


def main():
    # Initialize and print title
    settings = fileops.load_settings()
    fileops.clear_screen()
    print(fileops.colorme(settings["title"], "red"))
    log.info("Starting script copygp")

    # Load source network settings
    source_network = settings["copygp"]["source_network"].split(",")
    source_net_id = source_network[0]
    color_source = fileops.colorme(source_network[1], "blue")
    log.info(f"Pulling group policies from network {source_network[1]}")
    log.info(f"The source network ID is {source_network[0]}")
    print(f"\nPreparing to copy group policies from {color_source}")

    # Load group policies 
    policy_list = settings["copygp"]["copy_policies"]
    for policy in policy_list:
        log.info(f"policy ID: {policy}")
        print(f"Using policy {fileops.colorme(policy, 'blue')} as the source")

    # Load destinations file
    destinations = settings["copygp"]["destination_networks"]
    color_networks = fileops.colorme(destinations, "blue")
    log.info(f"Loading destinations network file {destinations}")
    print(f"To the destinations listed in network file {color_networks}")
    destination_networks = fileops.load_file(destinations)

    # Verify settings are correct before continuing
    choice = input("\nPress [Enter] to continue or [q] to quit: ")
    print()
    if "q" in choice:
        log.info("You chose not to continue")
        sys.exit()

    # Create an instance of the dashboard
    dashboard = merakiops.get_dashboard()
    # Verify that the source policy exists and load it
    source_policy = merakiops.get_source_policy(dashboard, source_net_id, policy_list)
    # Copy policy to destination networks
    done = 0
    total = len(destination_networks)
    for network in destination_networks:
        bar = fileops.progress_bar(done, total)
        print(bar, end="", flush=True)
        netinfo = network.split(",")
        net_id = netinfo[0]
        net_name = netinfo[1].strip()
        log.info(f"Attempting to copy policy to {net_name}")

        try:
            dashboard.networks.createNetworkGroupPolicy(
                net_id, policy_list[0],
                firewallAndTrafficShaping=source_policy
            )
        except Exception as e:
            log.info(f"Failed to copy policy to {net_name}")
            log.info(str(e))
        done += 1
        print("\b" * len(bar), end="", flush=True)

    bar = fileops.progress_bar(done, total)
    print(bar, end="", flush=True)
    log.info("Script completed successfully")
    print("\n\nScript completed successfully. See output/logs for details")


if __name__ == "__main__":
    main()
