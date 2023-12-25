"""Entry point for chimerapulse.core.language module

Example:
    python -m chimerapulse.core.language <submodule> <args>
"""
import click

from chimerapulse.core.language import document_summarization
from chimerapulse.core.language import conversation_summarization


@click.group()
def language():
    """Collection of CLI submodule commands available for running Azure Language Service capabilities
    """
    pass

language.add_command(document_summarization.summarizedocument)
language.add_command(conversation_summarization.summarizeconversation)
