"""
Descr: main module to operate log parsing
@author: corvit
Created: Fri Jul 24 2020 11:05 MSK
"""
import glob
import os
# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
# Ensure settings are read
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import codecs
import yaml as yml

# My application specific imports
from data.models import *
from my_logger import logging_setup
from parse import parse_data


def general_init():
    global logger, full_path
    logger = logging_setup()

    # get script path
    full_path, filename = os.path.split(os.path.realpath(__file__))
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
    folder_ptrn = full_path + log_path + log_ptrn
    lst = glob.escape(folder_ptrn)
    # for m_report_file in MISSION_REPORT_PATH.glob('missionReport*[[]0[]].txt'):

    logger.debug(f'filter pattern:\n{folder_ptrn}')
    logger.debug(f'filtered log files:\n{lst}')

    lst = (full_path + '\log_samples\missionReport(2020-07-16_20-55-42)[0].txt',)

    return lst


# main starts here
def main():
    print('Running main module')

    general_init()
    conf = load_cfg()
    msg = f'Loaded the following configuration:\n{conf}'
    logger.debug(msg)

    tst_user()

    #files = (full_path + '\media\log_samples\missionReport(2020-07-16_20-55-42)[0].txt',)
    files = get_files_lst(conf['settings']['log_path'], conf['settings']['log_ptrn'])
    msg = f'files to process list:\n{files}'
    logger.debug(msg)

    parse_data(files)

    print("\nThat's all folks")


if __name__ == "__main__":
    main()

# TODO: