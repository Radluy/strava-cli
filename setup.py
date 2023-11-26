from src import ROOT_DIR, ACTIVITIES_DIR, CONFIG_PATH

import os
import shutil
from distutils.command.install import install
from setuptools import setup, find_packages


class SetupConfig(install):
    def run(self):
        install.run(self)
        os.mkdir(ROOT_DIR)
        os.mkdir(ACTIVITIES_DIR)
        shutil.copy('config.json', CONFIG_PATH)


setup(
    name='strava-cli',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'rich'
    ],
    entry_points={
        'console_scripts': [
            'strava-cli=src.parse:main',
        ],
    },

    cmdclass={'install': SetupConfig}
)
