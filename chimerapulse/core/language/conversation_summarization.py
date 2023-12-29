"""Module that contains raw call to Azure language service

List of supported languages for conversation summarization:
    https://learn.microsoft.com/en-us/azure/ai-services/language-service/summarization/language-support?tabs=conversation-summarization

Example:
    python -m chimerapulse.core.language summarizeconversation -p <args>
    chi language summarizeconversation -p
"""
import os
from tkinter import filedialog

import click
from dotenv import load_dotenv


@click.command()
def summarizeconversation():
    print('document summarization')
