"""Creates a csv file showing loss, latency, and jitter"""

import logging

from meraki_scripts.universal import fileops, merakiops

log = logging.getLogger(__name__)
logging.basicConfig(filename="output/debug.log", level=logging.DEBUG)

UPLINK = "cellular"
IP = "8.8.8.8"

def main():
    dashboard = merakiops.get_dashboard()
    orgs = merakiops.select_organization(dashboard)
    log.info(f"The selected organization is {orgs[1]}")
    network = merakiops.select_network(dashboard, orgs[0])
    log.info(f"The seleted network is {network[1]}")
    pri_mx_sn = merakiops.get_mx_serial_number(dashboard, network[0])
    log.info(f"The serial number found is {pri_mx_sn[1]}")
    try:
        response = dashboard.devices.getDeviceLossAndLatencyHistory(
            pri_mx_sn[1], ip=IP, uplink=UPLINK
        )
    except Exception as e:
        print(e)
    lines = []
    for stats in response:
        start = stats["startTs"]
        end = stats["endTs"]
        loss = stats["lossPercent"]
        latency = stats["latencyMs"]
        jitter = stats["jitter"]
        line = (
            start
            + ","
            + end
            + ","
            + str(loss)
            + ","
            + str(latency)
            + ","
            + str(jitter)
            + "\n"
        )
        lines.append(line)
    fileops.writelines_to_file("output/stats.csv", lines)


if __name__ == "__main__":
    main()
