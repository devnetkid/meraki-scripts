"""Copies group policies from a source network to a destination

Meraki API
https://developer.cisco.com/meraki/api/update-network-group-policy/

"""

import logging
import sys

from meraki_scripts.universal import fileops, merakiops

log = logging.getLogger(__name__)
fileops.setup_logging("updategp")


def main():
    settings = fileops.load_settings()
    fileops.clear_screen()
    print(fileops.colorme(settings["title"], "red"))
    log.info("Starting script copygp")


if __name__ == "__main__":
    main()
