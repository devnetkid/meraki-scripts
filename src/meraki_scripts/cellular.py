"""Find all sites with cellular connection create csv file from data

CSV file includes:
    Site, Model, Status, Connection, Signal, APN, ICCID, RSRP, RSRQ

"""

import logging
import sys

from meraki_scripts.universal import fileops, merakiops

log = logging.getLogger(__name__)
fileops.setup_logging("cellular")


def convert_network_id_to_name(networks, cellular_data):
    new_cellular_data = []
    log.debug("The convert_network_id_to_name function has been called")
    for site in cellular_data:
        if site.split(",")[0] == "Site":
            new_cellular_data.append(site)
            continue
        site_data = site.split(",")
        log.debug(f"The current network ID is {site_data[0]}")
        for network in networks:
            if network["id"] == site_data[0]:
                site_name = network["name"]
                log.debug(f"The corresponding site name is {site_name}")
                site_data[0] = site_name
                site_data = ",".join(site_data)
                log.debug(f"The final site data is {site_data.strip()}")
                break
        new_cellular_data.append(site_data)
    return new_cellular_data


def find_cellular_uplinks(appliances):
    cellular_uplinks = ["Site,Model,Status,Type,Signal,APN,ICCID,RSRP,RSRQ\n"]
    log.debug("The find_cellular_uplinks function has been called")
    for appliance in appliances:
        for each_link in appliance["uplinks"]:
            if "cellular" in each_link["interface"]:
                site = appliance["networkId"] + ","
                model = appliance["model"] + ","
                status = each_link["status"] + ","
                if each_link["connectionType"]:
                    conn = each_link["connectionType"] + ","
                else:
                    conn = "" + ","
                if each_link["signalType"]:
                    signal = each_link["signalType"] + ","
                else:
                    signal = "" + ","
                if each_link["apn"]:
                    apn = each_link["apn"] + ","
                else:
                    apn = "" + ","
                if each_link["iccid"]:
                    iccid = each_link["iccid"] + ","
                else:
                    iccid = "" + ","
                if each_link["signalStat"]:
                    rsrp = each_link["signalStat"]["rsrp"] + ","
                else:
                    rsrp = "" + ","
                if each_link["signalStat"]:
                    rsrq = each_link["signalStat"]["rsrq"] + "\n"
                else:
                    rsrq = "" + "\n"
                cell_data = conn + signal + apn + iccid + rsrp + rsrq
                new_line = site + model + status + cell_data
                cellular_uplinks.append(new_line)
    return cellular_uplinks


def process_settings():
    # Ensure that the required settings have been setup
    log.info("Ensuring that settings are set correctly before continuing")
    settings = fileops.load_settings()
    fileops.clear_screen()
    print(fileops.colorme(settings["title"], "red"))
    if "output_file" not in settings["cellular"]:
        missing_key = fileops.colorme("output_file", "red")
        log.info(
            "Missing a required key 'output_file', "
            "add it to settings.toml and try again"
        )
        sys.exit(
            f"Missing a required key {missing_key}"
            "\nAdd it to the settings.toml file and try again"
        )
    if "filter_list" not in settings["cellular"]:
        missing_key = fileops.colorme("filter_list", "red")
        log.info(
            "Missing a required key 'filter_list', "
            "add it to settings.toml and try again"
        )
        sys.exit(
            f"Missing a required key {missing_key}"
            "\nAdd it to the settings.toml file and try again"
        )
    output_file = settings["cellular"]["output_file"]
    filter_list = settings["cellular"]["filter_list"]
    color_output_file = fileops.colorme(output_file, "blue")
    if filter_list:
        color_filter_list = fileops.colorme(filter_list, "blue")
    else:
        color_filter_list = fileops.colorme("Not set", "blue")
    if not output_file:
        required = fileops.colorme("Output file is required to continue.", "red")
        required += "\nUpdate the cellular output_file in settings.toml file"
        log.info("Output file was not specified and is required to continue")
        sys.exit(required)
    fileops.clear_screen()
    print(fileops.colorme(settings["title"], "red"))
    print("\nYou are about to pull cellular data with the following settings:")
    print(f"\n    Filter list: {color_filter_list}")
    print(f"    Output file: {color_output_file}")
    choice = input("\nPress [Enter] to continue or [q] to quit: ")
    if "q" in choice:
        log.info("You chose not to continue")
        sys.exit("The settings.toml file should be in the input folder")
    return {
        "title": settings["title"],
        "output_file": output_file,
        "filter_list": filter_list,
    }


def main():
    settings = process_settings()
    filter_list = settings["filter_list"]
    output_file = settings["output_file"]
    color_output_file = fileops.colorme(output_file, "blue")
    fileops.clear_screen()
    print(fileops.colorme(settings["title"], "red"))
    log.debug("Starting the main function from cellular.py")
    dashboard = merakiops.get_dashboard()
    log.debug("Prompting user to select an organization")
    orgs = merakiops.select_organization(dashboard)
    org_name = fileops.colorme(orgs[1], "blue")
    print(f"Searching the selected organization {org_name} " "for cellular uplinks\n")
    log.debug(f"The user has selected the {orgs[1]} organization")
    log.info(f"The {orgs[1]} organization has been selected")
    log.debug("Attempting to pull all uplinks for the selected organization")
    network_list = []
    if filter_list:
        log.info(f"Filtering based on networks in the file {filter_list}")
        netid_list = fileops.load_file(filter_list)
        for each_network in netid_list:
            network_list.append(each_network.split(",")[0])
    # Research possibly replacing current cellular uplink status checks with just this one
    # dashboard.organizations.getOrganizationUplinksStatuses(orgs[0], total_pages='all')
    try:
        appliances = dashboard.appliance.getOrganizationApplianceUplinkStatuses(
            orgs[0], networkIds=network_list, total_pages="all"
        )
        mg_appliances = (
            dashboard.cellularGateway.getOrganizationCellularGatewayUplinkStatuses(
                orgs[0], networkIds=network_list, total_pages="all"
            )
        )
    except Exception as e:
        log.exception(e)
    appliances.extend(mg_appliances)
    log.debug("All uplinks have been pulled and assigned to appliances variable")
    log.debug("Attempting to find all networks that have cellular uplinks")
    cellular_uplinks = find_cellular_uplinks(appliances)
    log.debug("Using the found cellular uplinks list to extract desired cell data")
    networks = merakiops.get_networks(dashboard, orgs[0])
    cellular_sites = convert_network_id_to_name(networks, cellular_uplinks)
    print(f"Writing the cellular data to file {color_output_file}")
    log.info(f"Writing the cellular data to file {output_file}")
    fileops.writelines_to_file(output_file, cellular_sites)
    log.info("--- The script finished successfully ---")
    print("\nScript completed successfully")


if __name__ == "__main__":
    main()
