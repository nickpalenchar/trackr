#!/bin/env/python3
"""
Trackr.

Usage:
    trackr start <task>
    trackr stop
"""

import csv
import os
from os import path
from datetime import datetime
from .csvhandler import CSVHandler
from docopt import docopt
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

class Commands:
    """
    All commands that can be called by the cli
    """

    @staticmethod
    def start(task):
        """Begin working on a task, ending a task in progress, if any."""
        stopped_task = stop_current_task()
        if stopped_task:
            print(f'Note: Stopped current task {stopped_task}')
        with CSVHandler(CURRENT_TASK_FULL_PATH, FIELDNAMES, 'a') as writer:
            writer.writeheader()
            writer.writerow({'task': task, 'begin': str(datetime.utcnow())})
        print(f'Task {task} started.')

    @staticmethod
    def stop():
        task_stopped = stop_current_task()
        if task_stopped:
            print(f'Task {task_stopped} stopped')
        else:
            print()


def stop_current_task():
    """
    Stops the current task if there is an entry in current.csv (and removes the file afterwards)
    Returns the str of the task name if the current task was removed, None if there was no current task
    """
    task_current = get_task_current()
    if task_current is None:
        return None
    task_current['end'] = str(datetime.utcnow())
    with CSVHandler(CONFIG_FULL_PATH, FIELDNAMES) as writer:
        writer.writerow(task_current)
    os.unlink(CURRENT_TASK_FULL_PATH)
    return task_current['task']



def get_task_current():
    """Returns the current task as an ordered dict, or None if none exists"""
    if not os.path.exists(CURRENT_TASK_FULL_PATH):
        return None
    with CSVHandler(path.join(CURRENT_TASK_FULL_PATH), mode='r') as ch:
        return list(ch)[0]


def main():
    """
    Invoke trackr.

    arguments are passed via argv and parsed with docopt. Commands and options are defined at the top of cli.py docstring.
    """
    create_file_if_needed()
    args = docopt(__doc__)
    command = [key for key, value in args.items() if not key.startswith('<') and value is True][0]
    parsedargs = {key.strip('<>'): val for key, val in args.items() if key.startswith('<') and val is not None}
    getattr(Commands, command)(**parsedargs)


if __name__ == '__main__':
    main()

