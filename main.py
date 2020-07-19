"""
Descr: main module to operate log parsing
@author: corvit
Created: Sun Jul 19 2020 14:05 MSK
"""
# import __main__
import codecs
# import logging
# import pandas as pd
import yaml as yml
from os import path
# from shutil import copy2

# own function to handle an uploaded file
from my_logger import logging_setup

def general_init():
    global logger, full_path
    logger = logging_setup()

    # get script path
    full_path, filename = path.split(path.realpath(__file__))
    logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))


def load_cfg():
    # read configuration
    cfg_file = full_path + '\\' + "parser.yaml"
    msg = 'Loading configuration:\nOpening {}'.format(cfg_file)
    logger.debug(msg)
    print(msg)

    with codecs.open(cfg_file, mode='rb', encoding='utf-8') as yml_fl:
        cfg = yml.safe_load(yml_fl)

    msg = 'Config loaded successfully'
    logger.debug(msg)
    print(msg)

    logger.debug(cfg)

    return cfg


def parse_data(file_to_proc):
    """
    parsing of log file
    receives parameters:
    file_to_proc - name of the file to be processed
    returns something
    """

    general_init()

    conf = load_cfg()

    msg = f'Loaded the following configuration:\n{conf}'

    parse_result = ''

    logger.debug("That's all folks")
    print("\nThat's all folks")

    return parse_result


# main starts here
if __name__ == "__main__":
    # print("Please call 'parse_data(path_to_file_to_process)' to parse xlsx file getting DF as output")
    parse_data('')

# TODO:
