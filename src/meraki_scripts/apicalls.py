"""Script to monitor API calls per second

https://developer.cisco.com/meraki/api-v1/get-organization-api-requests/
"""

import logging

from meraki_scripts.universal import fileops, merakiops

log = logging.getLogger(__name__)
fileops.setup_logging("apicalls")


def main():
    fileops.clear_screen()
    log.info("Starting script apicalls")
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
    output_file = settings["apicalls"]["output_file"]
    # If getting 429 errors constantly, the key is the timespan parameter
    response = dashboard.organizations.getOrganizationApiRequests(
        org_id, timespan="300"
    )
    fileops.writelines_to_file(output_file, response, "json")


if __name__ == "__main__":
    main()
