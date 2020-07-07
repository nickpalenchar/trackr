#!/bin/env/python3
"""
Trackr.

Usage:
    trackr add <task>
    trackr start <task> [-a]
    trackr stop
    trackr tasks
    trackr current
    trackr report
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
LOG_FILENAME = 'time.csv'
LOG_FILEPATH = path.join(CONFIG_PATH, LOG_FILENAME)
CURRENT_TASK_FILEPATH = path.join(CONFIG_PATH, 'current.csv')
TASKS_FILEPATH = path.join(CONFIG_PATH, 'tasks.txt')
FIELDNAMES = ['task', 'begin', 'end']


def create_file_if_needed(config_path=CONFIG_PATH, config_file=LOG_FILENAME):
    _create_log_file_if_needed(config_path, config_file)
    _create_tasks_file_if_needed(TASKS_FILEPATH)


def _create_log_file_if_needed(config_path, config_file):
    if not path.exists(path.join(config_path, config_file)):
        os.mkdir(CONFIG_PATH)
        with open(path.join(CONFIG_PATH, LOG_FILENAME), 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(FIELDNAMES)


def _create_tasks_file_if_needed(tasks_filepath):
    if not path.exists(tasks_filepath):
        print('ADDINGG')
        open(tasks_filepath, 'a').close()


class Commands:
    """
    All commands that can be called by the cli
    """

    @staticmethod
    def start(task, a=False):
        """Begin working on a task, ending a task in progress, if any."""
        if task not in get_all_tasks() and a is False:
            print(f'Sorry: {task} is not in tasklist. Try with -a or `trackr add <task>`')
            return
        _add_task_to_tasklist(task)
        stopped_task = stop_current_task()
        if stopped_task:
            print(f'Note: Stopped current task {stopped_task}')
        with CSVHandler(CURRENT_TASK_FILEPATH, FIELDNAMES, 'a') as writer:
            writer.writeheader()
            writer.writerow({'task': task, 'begin': str(datetime.utcnow())})
        print(f'Task {task} started.')

    @staticmethod
    def stop():
        task_stopped = stop_current_task()
        if task_stopped:
            print(f'Task {task_stopped} stopped')
        else:
            print('No task to stop.')

    @staticmethod
    def report():
        """Get a weekly report of how much time has been spent and where"""
        raise NotImplementedError

    @staticmethod
    def tasks():
        """list all known tasks"""
        print(get_all_tasks())
        for task in filter(bool, get_all_tasks()):
            print(task)

    @staticmethod
    def add(task):
        """Register a new task"""
        if task in get_all_tasks():
            print(f'Task {task} is already in the tasklist')
        else:
            _add_task_to_tasklist(task)
            print(f'Task {task} added to tasklist.')

    @staticmethod
    def current():
        """Report the current task"""
        raise NotImplementedError


def _add_task_to_tasklist(task):
    if task in get_all_tasks():
        return None
    with open(TASKS_FILEPATH, 'a') as fh:
        fh.writelines(['\n', task])


def stop_current_task():
    """
    Stops the current task if there is an entry in current.csv (and removes the file afterwards)
    Returns the str of the task name if the current task was removed, None if there was no current task
    """
    task_current = get_task_current()
    if task_current is None:
        return None
    task_current['end'] = str(datetime.utcnow())
    with CSVHandler(LOG_FILEPATH, FIELDNAMES) as writer:
        writer.writerow(task_current)
    os.unlink(CURRENT_TASK_FILEPATH)
    return task_current['task']


def get_task_current():
    """Returns the current task as an ordered dict, or None if none exists"""
    if not os.path.exists(CURRENT_TASK_FILEPATH):
        return None
    with CSVHandler(path.join(CURRENT_TASK_FILEPATH), mode='r') as ch:
        return list(ch)[0]


def get_all_tasks():
    with open(TASKS_FILEPATH, 'r') as fh:
        return [line.rstrip() for line in fh.readlines()]


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

