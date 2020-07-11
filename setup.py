"""Packaging settings."""
from os.path import abspath, dirname, join
from setuptools import find_packages, setup
from trackr import __version__

this_dir = abspath(dirname(__file__))

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()


setup(
    name='trackr',
    version=__version__,
    description='python cli for keeping track of what you\'re working on in csv.',
    long_description='',
    url='https://github.com/nickpalenchar/trackr',
    author='Nick Palenchar',
    author_email='nickpal@nickpalenchar.com',
    license='MIT',
    classifiers=[

    ],
    keywords='cli',
    packages=find_packages(exclude=['docs', 'tests*', 'venv']), # prevents irrelevent files from being added to package
    package_data={'': ['*.sh', '*.bash']},
    install_requires=required,
    extras_require={
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points={
        'console_scripts': [
            'trackr=trackr.cli:main',
        ],
    }
)
