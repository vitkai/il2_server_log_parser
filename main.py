"""
Descr: main module to operate log parsing
@author: corvit
Created: Fri Jul 24 2020 11:05 MSK
"""
#import glob
import codecs
import os
from pathlib import Path
import re
import yaml as yml


# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
# Ensure settings are read
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# My application specific imports
from data.models import *
from my_logger import logging_setup
from handlers import check_mission
from parse import parse_data


def general_init():
    global logger, full_path
    logger = logging_setup()

    # get script path
    full_path, filename = os.path.split(os.path.realpath(__file__))
    logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))


def load_cfg():
    # read configuration

    """global log_dir_path

    print(f'load_cfg().full_path={full_path}')"""

    cfg_file = os.path.join(full_path,"parser.yaml")
    msg = 'Loading configuration:\nOpening {}'.format(cfg_file)
    logger.debug(msg)
    print(msg)

    with codecs.open(cfg_file, mode='rb', encoding='utf-8') as yml_fl:
        cfg = yml.safe_load(yml_fl)

    msg = 'Config loaded successfully'
    logger.debug(msg)
    print(msg)

    #log_dir_path = os.path.join(full_path, cfg['settings']['log_path'])

    # logger.debug(cfg)

    return cfg


def tst_user():
    # Add user
    #user = User(name="corvit", email="corvit@mail.ru")
    #user.save()

    # Application logic
    first_user = User.objects.all()[0]

    print(first_user.name)
    print(first_user.email)


def get_files_lst(log_path, log_ptrn):
    """
    :param log_path: path to log files dir
    :param log_ptrn: pattern for log files
    (data is populated to db)
    :return: lst: sorted list of Mission_Log objects
    """
    MISSION_NAME_LOG_ID = re.compile(r'^.*\[(?P<index>\d+)\].*$')
    # MISSION_LOG_FILE_RE = re.compile(r'^.*port\(\d\d\d\d-\d\d-\d\d_\d\d-\d\d-\d\d\)')
    MISSION_NAME = re.compile(r'^.*port\((?P<mission_name>\d\d\d\d-\d\d-\d\d_\d\d-\d\d-\d\d)\)')

    #folder_ptrn = os.path.join(full_path, log_path)  # + log_ptrn
    folder_ptrn = Path(log_path)  # + log_ptrn

    # lst = glob.escape(folder_ptrn)
    lst = folder_ptrn.glob(log_ptrn)
    # for m_report_file in MISSION_REPORT_PATH.glob('missionReport*[[]0[]].txt'):

    #logger.debug(f'filter pattern:\n{folder_ptrn}')
    #logger.debug(f'filtered log files:\n{lst}')
    #print(f'filtered log files:')
    for file in lst:
        logger.debug(f'file: {file}')
        #print(f'{file}')
        mission_name = MISSION_NAME.match(str(file)).groupdict()['mission_name']
        mission_name_log_id = MISSION_NAME_LOG_ID.match(str(file)).groupdict()['index']
        logger.debug(f'mission_name: {mission_name} | log_id: {mission_name_log_id}')

        #ftlr_exists = Mission_Log.objects.filter(name=mission_name, miss_log_id=mission_name_log_id).exists()

        if not Mission_Log.objects.filter(name=mission_name, miss_log_id=mission_name_log_id).exists():
            # Add mission log record to the base
            miss_log = Mission_Log(name=mission_name, miss_log_id=mission_name_log_id)
            miss_log.save()
            logger.debug('Adding record to db')
        else:
            logger.debug('The record exists in db')
            pass

    #lst = (full_path + '\log_samples\missionReport(2020-07-16_20-55-42)[0].txt',)

    # get sorted file list
    lst = Mission_Log.objects.filter(is_processed=False).order_by('name', 'miss_log_id')

    """
    for item in lst:
        #print(f'idx:{idx} | item: {item}')
        print(f'items: {item.name}, {item.miss_log_id}')
        #print(f'idx:{idx} | item: {lst[idx]}')
    print(lst)
    """
    return lst


# main starts here
def main():
    #global full_path#, log_dir_path

    #full_path, filename = os.path.split(os.path.realpath(__file__))

    print('Running main module')

    general_init()
    conf = load_cfg()
    msg = f'Loaded the following configuration:\n{conf}'
    logger.debug(msg)

    log_dir_path = os.path.join(full_path, conf['settings']['log_path'])

    #tst_user()

    files = get_files_lst(log_dir_path, conf['settings']['log_ptrn'])

    """msg = f'files to process list:\n{files}'
    logger.debug(msg)"""


    for rec in files:
        check_mission(rec.name)
        file_path = 'missionReport(' + str(rec.name) + ')[' + str(rec.miss_log_id) + '].txt'

        work_fl = os.path.join(log_dir_path, file_path)
        logger.debug(f'processing file: [{work_fl}]')
        parse_data(work_fl)

    print("\nThat's all folks")


if __name__ == "__main__":
    main()

# TODO: