"""Create a file listing all the networks in an organization"""


from meraki_scripts.universal import fileops, merakiops


def main():
    dashboard = merakiops.get_dashboard()
    org_id, org_name = merakiops.select_organization(dashboard)
    out_file = "output/" + org_name + "_networks.txt"
    networks = merakiops.get_networks(dashboard, org_id)
    network_list = []
    for network in networks:
        new_line = network["id"] + "," + network["name"] + "\n"
        network_list.append(new_line)
    fileops.writelines_to_file(out_file, network_list)


if __name__ == "__main__":
    main()
