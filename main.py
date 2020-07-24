"""
Descr: main module to operate log parsing
@author: corvit
Created: Sun Jul 19 2020 14:05 MSK
"""
# import __main__
import codecs
import unicodedata
# import logging
# import pandas as pd
import yaml as yml
from os import path
# from shutil import copy2

# own function to handle an uploaded file
from my_logger import logging_setup
from handlers import atype_handlers, param_handlers

class UnexpectedATypeWarning(Warning):
    pass


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


def parse_line(line):
    """
    :type line: str
    :rtype: dict | None
    """
    line = unicodedata.normalize('NFKD', line)
    logger.debug(f'normalized line {line}')

    atype_id = int(line.partition('AType:')[2][:2])
    logger.debug(f'atype_id: {atype_id}')

    if 0 <= atype_id <= 22:
        data = atype_handlers[atype_id].match(line.strip()).groupdict()
        data['atype_id'] = atype_id
        logger.debug(f'data: {data}')
        for key, value in list(data.items()):
            if key in param_handlers:
                data[key] = param_handlers[key](value)
        logger.debug(f'data: {data}')
        return data
    else:
        raise UnexpectedATypeWarning


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
    logger.debug(msg)

    parse_result = ''
    # lines = []

    files = ('\media\log_samples\missionReport(2020-07-16_20-55-42)[0].txt',)

    for file_path in files:
        work_fl = full_path + '\\' + file_path
        logger.debug(f'processing file: [{work_fl}]')
        with open(work_fl, mode='r') as f:
            for line in f:
                # игнорируем "плохие" строки без
                if 'AType' not in line:
                    logger.warning('ignored bad string: [{}]'.format(line))
                    continue
                # lines.append(line)

                try:
                    logger.debug(f'processing line: [{line}]')
                    parse_result = parse_line(line)
                except AttributeError:
                    logger.error('bad line: [{}]'.format(line.strip()))
                    continue
                except parse_mission_log_line.UnexpectedATypeWarning:
                    logger.warning('unexpected atype: [{}]'.format(line))
                    continue

    # logger.debug(f'atype_handlers: {atype_handlers}')

    logger.debug("That's all folks")
    print("\nThat's all folks")

    return parse_result


# main starts here
if __name__ == "__main__":
    # print("Please call 'parse_data(path_to_file_to_process)' to parse xlsx file getting DF as output")
    parse_data('')

# TODO:
