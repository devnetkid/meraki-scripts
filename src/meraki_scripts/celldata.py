"""Doc_String"""

import logging
from meraki_scripts.universal import fileops, merakiops

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
    lines = []
    for stats in response:
        start = stats["startTs"]
        end = stats["endTs"]
        loss = stats["lossPercent"]
        latency = stats["latencyMs"]
        jitter = stats["jitter"]
        line = start + "," + end + "," + str(loss) + "," + str(latency) + "," + str(jitter) + "\n"
        lines.append(line)
    fileops.writelines_to_file("output/stats.csv", lines)


if __name__ == "__main__":
    main()
