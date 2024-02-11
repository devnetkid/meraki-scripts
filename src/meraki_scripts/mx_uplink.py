"""Get the uplink and vlan settings for a particular network

"""

import logging

from meraki_scripts.universal import fileops, merakiops

log = logging.getLogger(__name__)
fileops.setup_logging("mx_uplink")


def main():
    """Selects organization and network for getting uplink info"""

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

    # Select a network to pull uplink info from
    net_id, net_name = merakiops.select_network(dashboard, org_id)
    filename = "output/" + net_name + ".txt"
    netname = fileops.colorme(net_name, "blue")
    netid = fileops.colorme(net_id, "blue")
    log.info(f'The "{net_name}" network with ID {net_id} has been selected')
    print(f"The {netname} network with ID {netid} has been selected\n")

    # Get the uplink info for the selected network
    uplink_info = merakiops.get_mx_uplink_information(dashboard, net_id)
    fileops.writelines_to_file(filename, uplink_info, "json")


if __name__ == "__main__":
    main()
