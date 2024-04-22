"""Create a file listing all the networks in an organization"""

import logging
import sys

from meraki_scripts.universal import fileops, merakiops

log = logging.getLogger(__name__)
fileops.setup_logging("networks")

def main():
    log.info("Starting script networks")
    settings = fileops.load_settings()
    fileops.clear_screen()
    print(fileops.colorme(settings["title"], "red"))
    dashboard = merakiops.get_dashboard()
    org_id, org_name = merakiops.select_organization(dashboard)
    color_org = fileops.colorme(org_name, "blue")
    log.info(f"You selected '{org_name}'")
    out_file = "output/" + org_name + "_networks.txt"
    color_output = fileops.colorme(out_file, "blue")
    log.info(f"Collecting list of networks and writing them to '{out_file}'")
    # Handle 429 or other dashboard errors
    try:
        networks = merakiops.get_networks(dashboard, org_id)
    except:
        sys.exit()
    network_list = []
    for network in networks:
        new_line = network["id"] + "," + network["name"] + "\n"
        network_list.append(new_line)
    fileops.writelines_to_file(out_file, network_list)
    log.info("Script completed successfully")
    print("Script completed successfully")
    print(f"\nNetworks for {color_org} written to {color_output}")


if __name__ == "__main__":
    main()
