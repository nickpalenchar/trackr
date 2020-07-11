
from datetime import datetime, timedelta
from collections import namedtuple

Entry = namedtuple('Entry', ('time', 'percent'))


class CollectiveTasks:

    def __init__(self):
        self.tasks = {}
        self.total = timedelta()

    def __setitem__(self, key, value: timedelta):
        if type(value) is not timedelta:
            raise ValueError('must pass a timedelta')
        if key in self.tasks:
            self.total -= self.tasks[key]
        print('setting')
        self.tasks[key] = value
        self.total += self.tasks[key]

    def __delitem__(self, key):
        self.total -= self.tasks[key]
        del self.tasks[key]

    def __getitem__(self, item):
        task = self.tasks[item]
        return Entry(time=task, percent=(task / self.total))

    def __contains__(self, item):
        return item in self.tasks


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

        result = []

        current_date = self.rows[0][1]
        day_tasks = CollectiveTasks()
        for task, start, end in self.rows:
            # TODO: this does not account for the edge case of a task that spans 2+ days
            if start.day != current_date.day:
                result.append(day_tasks)
                day_tasks = CollectiveTasks()
                current_date = start
            task_length = end - start
            day_tasks[task] = day_tasks[task].time + task_length if task in day_tasks else task_length

        result.append(day_tasks)
        print('\n'.join(result))




"""
the timeline (already there):
the total on each day, in time and percentage.

{
    totals: { task: 
"""