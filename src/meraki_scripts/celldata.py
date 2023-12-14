"""Doc_String"""

import logging
from meraki_scripts.universal import merakiops

log = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log', level=logging.DEBUG)

def main():
    dashboard = merakiops.get_dashboard()
    orgs = merakiops.select_organization(dashboard)
    networks = merakiops.select_network(dashboard, orgs[0])
    sn = merakiops.get_mx_serial_number(dashboard, networks[0])
    print(sn[1])
    try:
        response = dashboard.devices.getDeviceLossAndLatencyHistory(sn[1], ip='8.8.8.8', uplink="wan1")
        print(response)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
