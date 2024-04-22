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
    print(f"  Preparing to copy group policies from {color_source}")

    # Load group policies 
    policy_list = settings["copygp"]["copy_policies"]
    for policy in policy_list:
        log.info(f"  policy ID: {policy}")
        print(f"    Policy ID: {fileops.colorme(policy, 'blue')}")

    # Load destinations file
    destinations = settings["copygp"]["destination_networks"]
    color_networks = fileops.colorme(destinations, "blue")
    log.info(f"Loading destinations network file {destinations}")
    print(f"  To the destinations listed in network file {color_networks}")

    # Verify settings are correct before continuing
    choice = input("\nPress [Enter] to continue or [q] to quit: ")
    print()
    if "q" in choice:
        log.info("You chose not to continue")
        sys.exit()


if __name__ == "__main__":
    main()
