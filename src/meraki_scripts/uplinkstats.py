"""Creates a csv file showing loss, latency, and jitter

https://developer.cisco.com/meraki/api-v1/get-device-loss-and-latency-history/

"""

import logging

from meraki_scripts.universal import fileops, merakiops

log = logging.getLogger(__name__)
logging.basicConfig(filename="output/debug.log", level=logging.DEBUG)

settings = fileops.load_settings("input/settings.toml")
dst_ip = settings["uplinkstats"]["destination_ip"]
uplink = settings["uplinkstats"]["uplink_interface"]
output_file = settings["uplinkstats"]["output_file"]

def main():
    fileops.clear_screen()
    print(fileops.colorme(settings["title"], "red"))
    dashboard = merakiops.get_dashboard()
    orgs = merakiops.select_organization(dashboard)
    log.info(f"The selected organization is {orgs[1]}")
    network = merakiops.select_network(dashboard, orgs[0])
    log.info(f"The seleted network is {network[1]}")
    pri_mx_sn = merakiops.get_mx_serial_number(dashboard, network[0])
    log.info(f"The serial number found is {pri_mx_sn[1]}")
    try:
        response = dashboard.devices.getDeviceLossAndLatencyHistory(
            pri_mx_sn[1], ip=dst_ip, uplink=uplink
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
    fileops.writelines_to_file(output_file, lines)


if __name__ == "__main__":
    main()
