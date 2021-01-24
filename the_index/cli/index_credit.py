''' commandline interface entry point for the index_credit project '''

import click
from index_credit import config


@click.group()
def main():
    ''' display help '''


@main.command()
@click.argument('arg', type=str, required=False)
def run(arg: str = None):
    ''' placeholder '''
    print('Not yet not implemented.')
