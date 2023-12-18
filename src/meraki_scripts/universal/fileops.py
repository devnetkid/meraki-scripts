'''Common file operations'''

import os
import platform
import sys
from datetime import datetime
import tomlkit
import logging


def writelines_to_file(filename, filedata):
    # Write text to given path
    try:
        with open(filename, 'w', encoding='utf-8') as file_data:
            file_data.writelines(filedata)
    except FileNotFoundError:
        sys.exit('Error opening file')


def append_to_file(filename, filedata):
    # Write text to given path
    try:
        with open(filename, 'a', encoding='utf-8') as file_data:
            file_data.writelines(filedata)
    except FileNotFoundError:
        sys.exit('Error opening file')


def progress_bar(progress, total, width=40):
    char = chr(9632)
    if progress >= total:
        fill_char = colorme(char, 'green')
    else:
        fill_char = colorme(char, 'red')
    completed = int(width * (progress / total))
    bar = 'Progress: [' + fill_char * completed + '-' * (width - completed) + '] '
    percent_done = round(progress / total * 100, 1)
    bar += str(percent_done) + '% ' + str(progress) + '/' + str(total)
    return bar


def clear_screen():
    if(platform.system().lower()=='windows'):
        cmd = 'cls'
    else:
        cmd = 'clear'
    os.system(cmd)


def colorme(msg, color):
    if color == 'red':
        wrapper = '\033[91m'
    elif color == 'blue':
        wrapper = '\033[94m'
    elif color == 'green':
        wrapper = '\033[92m'
    else:
        # Defaults to white if invalid color is given
        wrapper = '\033[47m'
    return wrapper + msg + '\033[0m'


def load_settings(settings_path="input/settings.toml"):
    try:
        with open(settings_path, "r") as file:
            settings = tomlkit.loads(file.read())
    except tomlkit.exceptions.TOMLKitError as e:
        raise ValueError(f"Error decoding TOML file: {str(e)}")
    except FileNotFoundError:
        sys.exit("Couldn't find settings.toml file. "
        "Make sure to add it to input folder in the root directory")
    # Make sure the needed keys are there
    required_keys = ["title", "addresses", "cellular", "uplinkstats", "logging"]
    for key in required_keys:
        if key not in settings:
            sys.exit(f"Missing key {key}, please make sure all settings are set")
    return settings


def load_file(filename):
    """Opens a file for reading and formats the network data

    Args:
        filename (str): The filename to be opened

    Returns:
        list: The data found in the file
    """

    try:
        with open(filename, "r", encoding="UTF-8") as file:
            data = file.read().replace('\n','')
        return data
    except FileNotFoundError:
        sys.exit(f"Could not find file {filename}")


def readlines_in_file(filename):
        try:
            with open(filename, "r", encoding="UTF-8") as file:
                data = file.readlines()
            return [item.split() for item in data]
        except FileNotFoundError:
            sys.exit(f"Could not find file {filename}")


def setup_logging(script_name):
    settings = load_settings("input/settings.toml")
    log_level = settings["logging"]["file_log_level"]
    log_file = settings["logging"]["file_log_path"]
    time_stamp = datetime.now().strftime("__%Y-%m-%d__%H-%M-%S")
    logname = log_file + script_name + time_stamp + ".log"

    logging.basicConfig(
        filename=logname,
        level=log_level.upper(),
        format=(
            "%(asctime)2s %(filename)22s:%(lineno)6s "
            "%(levelname)11s > %(message)s"
        ),
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )
