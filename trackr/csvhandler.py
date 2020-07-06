import csv
from collections import namedtuple

CSVFile = namedtuple('CSVFile', ['reader', 'writer'])


class CSVHandler:

    file = None

    def __init__(self, filepath, fieldnames=None, mode='a', **kwargs):
        self.filepath = filepath
        self.fieldnames = fieldnames
        self.mode = mode
        self.kwargs = kwargs

    def __enter__(self):
        # breakpoint()
        self.file = open(self.filepath, self.mode, newline='', **self.kwargs)
        if self.mode == 'r':
            return csv.DictReader(self.file, self.fieldnames)
        else:
            return csv.DictWriter(self.file, self.fieldnames)
        # ch = CSVFile(
        #     writer=csv.DictWriter(self.file, self.fieldnames),
        #     reader=csv.DictReader(self.file, self.fieldnames)
        # )
        # return ch

    def __exit__(self, exec_type, exec_val, exec_tb):
        self.file.close()
