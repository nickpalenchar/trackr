from typing import List, Iterable, Set, Union
from datetime import datetime, timedelta
from collections import namedtuple, defaultdict

# Entry = namedtuple('Entry', ('time', 'percent'))

WEEKDAY_LETTERS = ('Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su')

class Entry:

    def __init__(self, time, percent):
        self.time = time
        self._percent = percent

    @property
    def percent(self):
        value = str(int((self._percent * 100) // 1))
        if value == '0':
            value = '<1'
        return value

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
    def reportheader(header: List[str] = None, cell_width=CELL_WIDTH, offset=1) -> str:
        """
        Return the header, which should use the same header as all calls to reportrow. This will create a table
        where all values line up with a certain column.

        Assumes the first column will be titles (rather than values), and prints a blank cell first. To start
        printing columns with header values immediately, set offest to 0

        :param offset: Number of blank columns to print before printing header values. Default 1
        """

        header_fmt =  f'|{"|".join([name.center(cell_width) for name in ([""] * offset) + list(header)])}|'
        footer_fmt = f'+{"+".join(["".center(cell_width, "-") for _ in range(len(header) + offset)])}+'

        return f'{header_fmt}\n{footer_fmt}'

    def reportrow(self, header: Iterable[str] = None, cell_width=CELL_WIDTH) -> str:
        if header is None:
            header = self.tasks.keys()
        result = [self.title.center(cell_width)] if self.title else []
        for task in header:
            if task not in self.tasks:
                result.append(''.center(cell_width))
            else:
                result.append(f'{self[task].percent}%'.center(cell_width))
        return f'|{"|".join(result)}|'

    def reporttotals(self, header: Union[List[str], Set[str]], cell_width=CELL_WIDTH, offset=1, bottom_boarder=True) -> str:
        """
        Arranges totals a row divided by cells. Intended to be added to the bottom of a report where at least
        reportheaders has been called (probably followed by reportrow), because reporttotals will not print the
        task names from the passed headers itself
        """
        # breakpoint()
        totals = f"|{self.title.center(cell_width)}" if self.title else ''
        totals += f"{'|'.join(([''] * offset) + [(str(self[task].percent) + '%').center(cell_width)for task in header])}|"
        totals += f"\n+{'+'.join([''.center(cell_width, '-') for _ in range(len(header) + offset)])}|" if bottom_boarder else ''
        return totals


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
        day_tasks = None
        total_task_times = CollectiveTasks('TOTAL')
        for task, start, end in self.rows:
            if day_tasks is None:
                day_tasks = CollectiveTasks(f'{WEEKDAY_LETTERS[start.weekday()]} {start.month}/{start.day}')
            task_header.add(task)
            # TODO: this does not account for the edge case of a task that spans 2+ days
            if start.day != current_date.day:
                result.append(day_tasks)
                # breakpoint()
                day_tasks = CollectiveTasks(f'{WEEKDAY_LETTERS[start.weekday()]} {start.month}/{start.day}')
                current_date = start
            task_length = end - start

            # If a task has some time logged, add to it. Else add the task and set time logged to current time spent.
            day_tasks[task] = day_tasks[task].time + task_length if task in day_tasks else task_length
            total_task_times[task] = total_task_times[task].time + task_length if task in total_task_times else task_length

        result.append(day_tasks)
        print(CollectiveTasks.reportheader(task_header))
        print('\n'.join([r.reportrow(task_header) for r in result]))
        print(total_task_times.reporttotals(task_header))



"""
the timeline (already there):
the total on each day, in time and percentage.

{
    totals: { task: 
"""