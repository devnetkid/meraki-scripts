"""Takes an input file as source data and returns a sorted list
to write to the specified output file.

"""

import logging
import re

from meraki_scripts.universal import fileops

log = logging.getLogger(__name__)
fileops.setup_logging("sort")

def sort_data(csv_data, column, regex):
    temp_data = []
    for line in csv_data:
        line = line.split(",")
        for match in re.findall(regex, line[column]):
            if match:
                line.append(match)
            temp_data.append(line)
    return sorted(temp_data, key=lambda row: row[-1])


def main():
    fileops.clear_screen()
    log.info("Starting script sort")
    settings = fileops.load_settings("input/settings.toml")
    input_file = settings["sort"]["input_file"]
    output_file = settings["sort"]["output_file"]
    search_column = settings["sort"]["search_column"]
    search_pattern = settings["sort"]["regex_pattern"]
    regex = re.compile(search_pattern)
    data = fileops.load_file(input_file)
    sortedlist = sort_data(data, search_column, regex)
    temp_list = []
    for item in sortedlist:
        item.pop(-1)
        temp_str = ",".join(item)
        temp_list.append(temp_str)
    fileops.writelines_to_file(output_file, temp_list)
    log.info("Script Finished successfully")
    print("Script finished successfully")


if __name__ == "__main__":
    main()
