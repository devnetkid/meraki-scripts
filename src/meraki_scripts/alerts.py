"""
Updates email list of who to notify on certain alerts
"""

import logging
import sys

from meraki_scripts.universal import fileops, merakiops

log = logging.getLogger(__name__)
fileops.setup_logging("alerts")


def main():
    log.info("Starting script alerts.py")

    # Load the settings
    log.info("Attempting to load settings")
    settings = fileops.load_settings("input/settings.toml")
    log.info("The settings have been loaded from input/settings.toml")

    # Get the file location for the target list of networks
    networks_path = settings["alerts"]["network_list"]
    networks_color = fileops.colorme(networks_path, "blue")
    log.info("Attempting to load the target networks")
    networks = fileops.load_file(networks_path)
    log.info(f"The networks have been loaded from {networks_path}")

    # Ensure that at least one of the alerts have been setup
    alert_defaults_path = settings["alerts"]["default_destinations"]
    alerts_path = settings["alerts"]["alerts"]
    log.info(f"alert defaults is set to {alert_defaults_path}")
    log.info(f"alerts is set to {alerts_path}")
    alert_defaults_color = fileops.colorme(alert_defaults_path, "blue")
    alerts_color = fileops.colorme(alerts_path, "blue")
    if not (alert_defaults_path or alerts_path):
        sys.exit("You need to setup the alerts json files in the settings.")
    if alert_defaults_path:
        alert_defaults_json = fileops.load_file(alert_defaults_path, "json")
    else:
        alert_defaults_json = {}
    if alerts_path:
        alerts_json = fileops.load_file(alerts_path, "json")
    else:
        alerts_json = []

    # Display menu, prompting user to confirm making the changes
    fileops.clear_screen()
    print(fileops.colorme(settings["title"], "red"))
    print(f"\n  For the list of networks from {networks_color}")
    print(f"  Update the default alert settings from {alert_defaults_color}")
    print(f"  Update the alert settings from {alerts_color}")

    # Get confirmation before continuing
    choice = input("\nPress [Enter] to continue or [q] to quit: ")
    print()
    if "q" in choice:
        log.info("You chose not to continue")
        sys.exit()

    # Update network alerts
    log.info("Creating an instance of the Meraki dashboard")
    dashboard = merakiops.get_dashboard()
    for network in networks:
        if network.startswith("L_") or network.startswith("N_"):
            network_id, network_name = network.split(",")
            log.info(f"Updating alert settings for the {network_name.strip()} network")
            response = dashboard.networks.updateNetworkAlertsSettings(
                network_id, defaultDestinations=alert_defaults_json, alerts=alerts_json
            )


if __name__ == "__main__":
    main()
