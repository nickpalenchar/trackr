"""Packaging settings."""
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from trackr import __version__


this_dir = abspath(dirname(__file__))


with open('requirements.txt') as f:
            required = f.read().splitlines()

with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()


setup(
    name = 'trackr',
    version = __version__,
    description = 'Programatic',
    long_description = long_description,
    url = 'https://github.com/nickpalenchar/repobot',
    author = 'Nick Palenchar',
    author_email = 'nickpal@nickpalenchar.com',
    license = 'MIT',
    classifiers = [
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    keywords = 'cli',
    packages = find_packages(exclude=['docs', 'tests*']), # prevents irrelevent files from being added to package
    package_data = {'': ['*.sh', '*.bash']},
    install_requires = required,
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'rbot=repobot.cli:main',
            'repobot=repobot.cli:main'
        ],
    }
)
