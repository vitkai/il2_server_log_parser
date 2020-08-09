"""
Descr: main module to operate log parsing
@author: corvit
Created: Sun Jul 19 2020 14:05 MSK
"""
# import __main__
import unicodedata
import logging
import os
import pytz
import sys
import time
from django.conf import settings
from datetime import datetime#, timedelta

# import pandas as pd
# from shutil import copy2

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
# Ensure settings are read
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# own function to handle an uploaded file
from handlers import atype_handlers, param_handlers, check_mission, proc_data#, event_handlers
from data.models import Mission_Log#Mission,

class UnexpectedATypeWarning(Warning):
    pass

logger = logging.getLogger(__name__)


def parse_line(line):
    """
    :type line: str
    :rtype: dict | None
    """
    line = unicodedata.normalize('NFKD', line)
    #logger.debug(f'normalized line {line}')

    atype_id = int(line.partition('AType:')[2][:2])
    #logger.debug(f'atype_id: {atype_id}')

    if 0 <= atype_id <= 22:
        data = atype_handlers[atype_id].match(line.strip()).groupdict()
        data['atype_id'] = atype_id
        #logger.debug(f'data: {data}')
        for key, value in list(data.items()):
            if key in param_handlers:
                data[key] = param_handlers[key](value)
        logger.debug(f'data: {data}')
        return data
    else:
        raise UnexpectedATypeWarning


"""def check_mission(mis_name):
    time_zone = pytz.timezone(settings.MISSION_REPORT_TZ)
    mission_timestamp = int(time.mktime(time.strptime(mis_name, '%Y-%m-%d_%H-%M-%S')))

    if Mission.objects.filter(timestamp=mission_timestamp).exists():
        logger.info(f'{mission_timestamp} - exists in the DB')
        # return
    else:
        real_date = time_zone.localize(datetime.fromtimestamp(mission_timestamp))
        real_date = real_date.astimezone(pytz.UTC)

        # Add mission
        mission = Mission(name=mis_name, timestamp=mission_timestamp, date_start=real_date, date_end=real_date,
                          duration=0)
        mission.save()
"""

def parse_data(files_to_proc, log_path):
    """
    parsing of log file
    :param files_to_proc: Mission_Log[]: list of Mission_Log object corresponding to the log files to be processed
    :param log_path: path to log files dir
    :return: something
    """
    rec: Mission_Log
    parse_result = ''
    # lines = []

    #for work_fl in files_to_proc:
    for rec in files_to_proc:
        check_mission(rec.name)
        file_path = 'missionReport(' + str(rec.name) + ')[' + str(rec.miss_log_id) + '].txt'
        #print(file_path)

        work_fl = os.path.join(log_path, file_path)
        # work_fl = full_path + '\\' + file_path
        logger.debug(f'processing file: [{work_fl}]')
        with open(work_fl, mode='r') as f:
            for line in f:
                # ignore "bad" strings
                if 'AType' not in line:
                    logger.warning('ignored bad string: [{}]'.format(line))
                    continue
                # lines.append(line)

                try:
                    #logger.debug(f'processing line:\n{line.strip()}')
                    parse_result = parse_line(line)
                    proc_data(parse_result)
                    """#atype_id = parse_result.pop('atype_id')
                    atype_id = parse_result['atype_id']
                    logger.debug(f"atype_id = {atype_id}")
                    logger.debug(f"event_handlers[atype_id] = {event_handlers[atype_id]}")
                    event_handlers[atype_id](**parse_result)"""

                    """except AttributeError:
                    logger.error('bad line: [{}]'.format(line.strip()))
                    continue
                    except UnexpectedATypeWarning:
                    logger.warning('unexpected atype: [{}]'.format(line))
                    continue"""
                except Exception as err:
                    print("Unexpected error:", err)
                    raise

    # logger.debug(f'atype_handlers: {atype_handlers}')

    logger.debug("That's all folks")
    print("\nThat's all folks")

    #return parse_result


# main starts here
if __name__ == "__main__":
    print("Please call 'parse_data(path_to_file_to_process)' to parse log files")
    #parse_data('')

# TODO:
