from typing import List
from datetime import datetime, timedelta
from collections import namedtuple

# Entry = namedtuple('Entry', ('time', 'percent'))

class Entry:

    def __init__(self, time, percent):
        self.time = time
        self._percent = percent

    @property
    def percent(self):
        return int((self._percent * 100) // 1)

class CollectiveTasks:

    CELL_WIDTH = 14

    def __init__(self, title=None):
        """
        Report time spent on tasks by how much time is logged over total time of all tasks. Used for creating rows
        in a report.
        
        :param title {str} - What should go in the first cell. Usually represents the day.
        """
        self.tasks = {}
        self.total = timedelta()
        self.title = title

    def __setitem__(self, key, value: timedelta):
        if type(value) is not timedelta:
            raise ValueError('must pass a timedelta')
        if key in self.tasks:
            self.total -= self.tasks[key]
        self.tasks[key] = value
        self.total += self.tasks[key]

    def __delitem__(self, key):
        self.total -= self.tasks[key]
        del self.tasks[key]

    def __getitem__(self, item) -> Entry:
        task = self.tasks[item]
        return Entry(time=task, percent=(task / self.total))

    def __contains__(self, item):
        return item in self.tasks

    def __str__(self) -> str:
        result = []
        for key, val in self.tasks.items():
            result.append(f'{key}: {self[key].percent}%,')
        return ' '.join(result)

    @staticmethod
    def reportheader(header: List[str] = None, cell_width=CELL_WIDTH) -> str:
        return f'|{"|".join([name.center(cell_width) for name in header])}|'

    def reportrow(self, header: List[str] = None, cell_width=CELL_WIDTH) -> str:
        if header is None:
            header = self.tasks.keys()
        result = []
        for task in header:
            if task not in self.tasks:
                result.append(''.center(cell_width))
            else:
                result.append(f'{self[task].percent}%'.center(cell_width))
        return f'|{"|".join(result)}|'


class Report:
    """
    Report of tasks worked on.
    Pass a list of rows with (task, start, end) items in it.
    """

    def __init__(self, *rows):
        self.rows = rows

    def show_report(self):
        if not self.rows:
            print('No data to report!')
            return

        result: List[CollectiveTasks] = []

        task_header = set()
        current_date = self.rows[0][1]
        day_tasks = CollectiveTasks()
        for task, start, end in self.rows:
            task_header.add(task)
            # TODO: this does not account for the edge case of a task that spans 2+ days
            if start.day != current_date.day:
                result.append(day_tasks)
                # breakpoint()
                day_tasks = CollectiveTasks()
                current_date = start
            task_length = end - start
            print('header>> ', task_header)
            day_tasks[task] = day_tasks[task].time + task_length if task in day_tasks else task_length

        result.append(day_tasks)
        print(CollectiveTasks.reportheader(task_header))
        print('\n'.join([r.reportrow(task_header) for r in result]))




"""
the timeline (already there):
the total on each day, in time and percentage.

{
    totals: { task: 
"""