from pathlib import Path
from setuptools import setup, find_packages

import pysteamgear as psg

try:
    with open(Path('requirements.txt'), 'r', encoding='utf-8') as f:
        required = f.read().splitlines()
except FileNotFoundError as e:
    print(str(e))
    required = []

setup(
    name=psg.__title__,
    version=psg.__version__,
    url=psg.__url__,
    packages=find_packages(),
    project_urls={
        'Github': psg.__url__,
        'Documentation': 'https://pysteamgear.readthedocs.io/',
        'Bug Reports': f'{psg.__url__}/issues',
    },
)
