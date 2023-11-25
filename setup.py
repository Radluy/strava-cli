from setuptools import setup, find_packages

setup(
    name='strava_cli',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'rich'
    ],
    entry_points={
        'console_scripts': [
            'strava_cli=src.parse:main',
        ],
    },
)
