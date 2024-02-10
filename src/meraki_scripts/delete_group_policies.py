"""Deletes all group policies for the specified network"""

import logging
import sys

from meraki_scripts.universal import fileops, merakiops

log = logging.getLogger(__name__)
fileops.setup_logging("delete_group_policies")


def main():
    """Handles the menu and user interaction for deleting group policies"""

    # Display menu and prompt for the selection of an organization
    fileops.clear_screen()
    settings = fileops.load_settings("input/settings.toml")
    log.debug("The settings have been loaded from input/settings.toml")
    print(fileops.colorme(settings["title"], "red"))
    log.debug("Instantiating an instance of the Meraki dashboard")
    dashboard = merakiops.get_dashboard()
    org_id, org_name = merakiops.select_organization(dashboard)
    orgname = fileops.colorme(org_name, "blue")
    orgid = fileops.colorme(org_id, "blue")
    log.info(f'The "{org_name}" organization with ID {org_id} has been selected')
    print(f"The {orgname} organization with ID {orgid} has been selected\n")

    # Select a network from which to delete all group policies
    net_id, net_name = merakiops.select_network(dashboard, org_id)
    netname = fileops.colorme(net_name, "blue")
    netid = fileops.colorme(net_id, "blue")
    log.info(f'The "{net_name}" network with ID {net_id} has been selected')
    print(f"The {netname} network with ID {netid} has been selected\n")

    # Display WARNING message giving user a chance to back out
    warn = fileops.colorme("WARNING: ", "red")
    print(f"{warn}You are about to make changes to the network that cannot be undone.")
    choice = input("\nType yes to continue or no to quit [no]: ")
    print()
    if "yes" not in choice:
        log.info("You chose not to continue")
        sys.exit()

    # Delete all group policies for the specified network
    print("Deleting group policies")
    merakiops.delete_group_policies(dashboard, net_id)
    log.info(f"The group policies for {net_name} have all been deleted")
    print(f"The group policies for {net_name} have all been deleted")


if __name__ == "__main__":
    main()
