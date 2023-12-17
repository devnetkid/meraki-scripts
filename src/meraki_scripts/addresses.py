"""Creates a csv file with each sites network name, ID, and address

This script pulls the site address from the MX or MZ, if available,
for all networks in a specified organization.

This script requires that your API key is defined in your os environment
variables as MERAKI_DASHBOARD_API_KEY or in settings.toml file

Updated: 11/24/2023
"""

import logging

from meraki_scripts.universal import fileops, merakiops

log = logging.getLogger(__name__)
fileops.setup_logging("addresses")


def main():
    fileops.clear_screen()
    log.info("Starting script to pull the addresses for an org")
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
    output_file = settings["addresses"]["output_file"]
    log.debug(
        f"The location specified in settings for the output file is {output_file}"
    )
    networks = dashboard.organizations.getOrganizationNetworks(org_id)
    done = 0
    total = len(networks)
    rows = ["Network Name;Network ID;Address\n"]
    log.info(f"Getting addresses for {org_name} and writing them to {output_file}")
    for network in networks:
        bar = fileops.progress_bar(done, total)
        print(bar, end="", flush=True)
        address = ""
        devices = dashboard.networks.getNetworkDevices(network["id"])
        for device in devices:
            if "MX" in device["model"]:
                address = device["address"].replace("\n", " ")
                # Handle condition where there is a spare MX
                if not address:
                    continue
                break
            if "MZ" in device["model"]:
                address = device["address"].replace("\n", " ")
                break
        row = network["name"] + ";" + network["id"] + ";" + address + "\n"
        rows.append(row)
        done += 1
        print("\b" * len(bar), end="", flush=True)
    bar = fileops.progress_bar(done, total)
    print(bar, end="", flush=True)
    fileops.writelines_to_file(output_file, rows)
    log.info(f"Script completed successfully. See {output_file} for details")
    print(f"\n\nScript completed successfully. See {output_file} for details")


if __name__ == "__main__":
    main()
