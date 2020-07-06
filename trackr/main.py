import csv
import docopt
import os
from os import path
from datetime import datetime
from csvhandler import CSVHandler

# str( datetime.utcnow() )
# datetime.fromisoformat()

CONFIG_PATH = f'{os.environ.get("HOME")}/trackr'
CONFIG_FILE = 'time.csv'
CONFIG_FULL_PATH = path.join(CONFIG_PATH, CONFIG_FILE)
CURRENT_TASK_FULL_PATH = path.join(CONFIG_PATH, 'current.csv')
FIELDNAMES = ['task', 'begin', 'end']


def create_file_if_needed(config_path=CONFIG_PATH, config_file=CONFIG_FILE):
    if not path.exists(path.join(config_path, config_file)):
        os.mkdir(CONFIG_PATH)
        with open(path.join(CONFIG_PATH, CONFIG_FILE), 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(FIELDNAMES)
    else:
        print('nothing to do')


def start(task):
    """Begin working on a task, ending a task in progress, if any."""
    with CSVHandler(path.join(CURRENT_TASK_FULL_PATH), FIELDNAMES, 'a') as writer:
        writer.writerow({'task': task, 'begin': str(datetime.utcnow())})


def stop():
    task_current = get_task_current()
    if task_current is None:
        print('nothing to stop')
        return
    if task_current['end']:
        print('Already ended')
        return


def get_task_current():
    """Returns the current task as an ordered dict, or None if none exists"""
    if not os.path.exists(CURRENT_TASK_FULL_PATH):
        return None
    with CSVHandler(path.join(CURRENT_TASK_FULL_PATH), mode='r') as ch:
        return ch.readline()

if __name__ == '__main__':
    start('test')
