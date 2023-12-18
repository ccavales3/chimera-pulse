"""
This file is the entry point for the create-py-cli package

Example:
    1) python -m <module_dir_path> <args>
    2) cpc <module> <args>
"""
import click

from src.template import template


@click.group()
def entry_point():  # pragma: no cover
    """
    Method called when calling `cpc` command in the cli
    """
    pass  # pylint: disable=unnecessary-pass


entry_point.add_command(template.template)
