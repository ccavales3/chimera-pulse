"""Entry point for chimerapulse.core.translator module

Example:
    python -m chimerapulse.core.translator text_translation <args>
    chi translator <submodule> <args>
"""
import click

from chimerapulse.core.translator import text_translator


@click.group()
def translator():
    """
    Method called code module when calling command in cli for running quality checks and sonar scanner
    """
    pass  # pylint: disable=unnecessary-pass


translator.add_command(text_translator.translatetext)
