"""
Updates email list of who to notify on certain alerts
"""

import logging

from meraki_scripts.universal import fileops, merakiops

log = logging.getLogger(__name__)
fileops.setup_logging("cellular")


def main():
    fileops.clear_screen()
    log.info("Starting script to pull the addresses for an org")
    settings = fileops.load_settings("input/settings.toml")
    log.debug("The settings have been loaded from input/settings.toml")
    print(fileops.colorme(settings["title"], "red"))
    log.debug("Instantiating an instance of the Meraki dashboard")
    networks = settings["alerts"]["network_list"]
    dashboard = merakiops.get_dashboard()
    for network in networks:
        if network.startswith("L_") or network.startswith("N_"):
            network_id = network.split(",")[0]
            print(network.split(",")[1])
            response = dashboard.networks.updateNetworkAlertsSettings(
                network_id,
                alerts=[
                    {
                        "type": "switchDown",
                        "enabled": True,
                        "alertDestinations": {
                            "emails": [],
                            "snmp": False,
                            "allAdmins": False,
                            "httpServerIds": [],
                        },
                        "filters": {"timeout": 10},
                    }
                ],
            )
            print(response)


if __name__ == "__main__":
    main()
