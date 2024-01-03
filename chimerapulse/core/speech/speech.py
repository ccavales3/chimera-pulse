"""Entry point for chimerapulse.core.speech module

Example:
    python -m chimerapulse.core.speech <submodule> <args>
    chi speech <submodule> <args>
"""
import click

from chimerapulse.core.speech import diarization
from chimerapulse.core.speech import language_identification


@click.group()
def speech():
    """Collection of CLI submodule commands available for running Azure Speech Service capabilities
    """
    pass  # pylint: disable=unnecessary-pass


speech.add_command(diarization.diarization)
speech.add_command(language_identification.identifylanguage)
