from setuptools import setup, find_packages

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
)
