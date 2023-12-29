"""Entry point for chimerapulse.core.language module

Reference:
    Service limits for Azure AI Language
        https://learn.microsoft.com/en-us/azure/ai-services/language-service/concepts/data-limits

Example:
    python -m chimerapulse.core.language <submodule> <args>
    chi language <submodule> <args>
"""
import click

from chimerapulse.core.language import document_summarization
from chimerapulse.core.language import conversation_summarization
from chimerapulse.core.language import sentiment_analysis
from chimerapulse.core.language import key_phrases


@click.group()
def language():
    """Collection of CLI submodule commands available for running Azure Language Service capabilities
    """
    pass

language.add_command(document_summarization.summarizedocument)
language.add_command(conversation_summarization.summarizeconversation)
language.add_command(sentiment_analysis.analyzesentiment)
language.add_command(key_phrases.keyphrases)