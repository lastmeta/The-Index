'''
install project in development mode:
/index_credit> python setup.py develop
'''

import os
from setuptools import setup, find_packages  # , findall

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

NAME = 'index_credit'
VERSION = '0.0.1'

setup(
    name=NAME,
    version=VERSION,
    description='index_credit is sound money of money',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=[f'{NAME}.{p}' for p in find_packages(where=NAME)] + [NAME],
    package_data={'': ['*.yaml'],},
    install_requires=[
        'jupyter',
        'notebook',
        'click',
        'PyYaml',
    ],
    # python_requires='>=3.5.2',
    # author="",
    # author_email="@wcf.com",
    # url="https://bitbucket.wcf.com/index_credit",
    # classifiers=[
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: Apache Software License",
    #     "Operating System :: OS Independent",
    # ],
    # scripts=[f for f in findall(dir='pm3/bin') if f.endswith('.py')],

    # to make it a command line utility uncomment:
    entry_points={
        "console_scripts": [
            "index_credit = index_credit.cli.index_credit:main",
        ]
    },
)
