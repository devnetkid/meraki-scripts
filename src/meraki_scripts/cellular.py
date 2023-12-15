"""Find all sites with cellular connection create csv file from data

CSV file includes:
    Site, Model, Status, Connection, Signal, APN, ICCID, RSRP, RSRQ

"""

import logging

from meraki_scripts.universal import fileops, merakiops

log = logging.getLogger(__name__)
logging.basicConfig(
    filename="output/cellular.log",
    level=logging.DEBUG,
    format=(
        "%(asctime)2s %(filename)22s:%(lineno)6s "
        "%(levelname)11s > %(message)s"
    ),
    datefmt="%m/%d/%Y %I:%M:%S %p",
)


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


def main():
    log.debug("Starting the main function from cellular.py")
    fileops.clear_screen()
    welcome = fileops.colorme(
        "Starting script to search for cellular uplinks", "blue"
    )
    print(welcome)
    dashboard = merakiops.get_dashboard()
    log.debug("Prompting user to select an organization")
    orgs = merakiops.select_organization(dashboard)
    org_name = fileops.colorme(orgs[1], "blue")
    print(
        f"Searching the selected organization {org_name} "
        "for cellular uplinks\n"
    )
    log.debug(f"The user has selected the {orgs[1]} organization")
    log.debug("Attempting to pull all uplinks for the selected organization")
    network_list = []
    has_list = input("Do you have a file with network IDs to filter on? [y or n]: ")
    if has_list.lower() == 'y':
        network_file = input("Enter in the name of the file: ")
        log.debug(f"User has selected to filter based on networks in the file {network_file}")
        network_list = fileops.readlines_in_file(network_file)
    try:
        appliances = dashboard.appliance.getOrganizationApplianceUplinkStatuses(
            orgs[0], networkIds=network_list, total_pages="all"
        )
        mg_appliances = dashboard.cellularGateway.getOrganizationCellularGatewayUplinkStatuses(
            orgs[0], networkIds=network_list, total_pages='all'
        )
    except Exception as e:
        log.exception(e)
    appliances.extend(mg_appliances)
    log.debug(
        "All uplinks have been pulled and assigned to appliances variable"
    )
    log.debug("Attempting to find all networks that have cellular uplinks")
    cellular_uplinks = find_cellular_uplinks(appliances)
    log.debug(
        "Using the found cellular uplinks list to extract desired cell data"
    )
    networks = merakiops.get_networks(dashboard, orgs[0])
    cellular_sites = convert_network_id_to_name(networks, cellular_uplinks)
    output_file = fileops.colorme("output/cellular-data.csv", "blue")
    print(f"Writing the cellular data to file {output_file}")
    fileops.writelines_to_file("output/cellular-data.csv", cellular_sites)
    log.debug("--- The script finished successfully ---\n")
    print("\nScript completed successfully")


if __name__ == "__main__":
    main()
