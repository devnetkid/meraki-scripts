"""Takes an input file as source data and returns a sorted list
to write to the specified output file.

"""

import csv
import logging
import re

from meraki_scripts.universal import fileops

log = logging.getLogger(__name__)
logging.basicConfig(filename='output/sort.log', level=logging.DEBUG,
    format=(
        "%(asctime)2s %(filename)22s:%(lineno)6s "
        "%(levelname)11s > %(message)s"),
    datefmt="%m/%d/%Y %I:%M:%S %p",
)


def sort_data(csv_data, column, regex):
    temp_data = []
    for line in csv_data:
        line_str = ",".join(line)
        new_line = line_str.split(",")
        for match in re.findall(regex, new_line[column]):
            if match:
                new_line.append(match)
            temp_data.append(new_line)
    return sorted(temp_data, key=lambda row: row[-1])


def writelines_to_file(file, lines):
    with open(file, "w") as f:
        wr = csv.writer(f)
        wr.writerows(lines)


def main():
    log.debug("Starting the main function from sort.py")
    log.debug("Prompt user for input file")
    input_file = input("Enter the location/file for the input data: ")
    log.debug("Prompt user for output file")
    output_file = input("Enter the location/file for the output data: ")
    log.debug("Prompt user for column to search file")
    search_column = int(input("Enter the column to sort by: "))
    log.debug("Prompt user for regex search pattern")
    search_pattern = input("Enter the regex search pattern: ")
    regex = re.compile(search_pattern)
    data = fileops.readlines_in_file(input_file)
    sortedlist = sort_data(data, search_column, regex)
    print(sortedlist)
    writelines_to_file(output_file, sortedlist)
    log.debug("--- End of script Finished successfully ---\n")
    print("Script finished successfully")


if __name__ == "__main__":
    main()
