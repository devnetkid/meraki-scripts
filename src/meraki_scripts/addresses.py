"""Creates a csv file with each sites network name, ID, and address

This script pulls the site address from the MX or MZ, if available,
for all networks in a specified organization.

This script requires that your API key is defined in your os environment
variables as MERAKI_DASHBOARD_API_KEY

Updated: 11/24/2023
"""

import os

from meraki_scripts.universal import fileops, merakiops


def main():
    fileops.clear_screen()
    settings = fileops.load_settings("input/settings.toml")
    print(fileops.colorme(settings["title"], "red"))
    dashboard = merakiops.get_dashboard()
    org_id, org_name = merakiops.select_organization(dashboard)
    orgname = fileops.colorme(org_name, "blue")
    orgid = fileops.colorme(org_id, "blue")
    print(f"The {orgname} organization with ID {orgid} has been selected\n")
    file_path = "output"
    file_name = "addresses.txt"
    output_file = os.path.join(file_path, file_name)
    print(output_file)
    networks = dashboard.organizations.getOrganizationNetworks(org_id)
    done = 0
    total = len(networks)
    rows = ["Network Name;Network ID;Address\n"]
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


if __name__ == "__main__":
    main()
