"""Module that calls Azure Key Phrase Extraction
https://learn.microsoft.com/en-us/azure/ai-services/language-service/key-phrase-extraction/overview

Example:
    python -m chimerapulse.core.language keyphrases -d 'Dr. Smith has a very modern medical office, and she has great staff.'
    chi language keyphrases <args>
"""

import os
from tkinter import filedialog

import click
from dotenv import load_dotenv

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Load env vars
load_dotenv()


def __authenticate_client():
    """Authenticate service

    Returns:
        (TextTranslationClient): Authenticated client
    """
    # Get Configuration Settings
    languageendpoint = os.getenv('TRANSLATOR_SERVICE_ENDPOINT')
    languagekey = os.getenv('TRANSLATOR_SERVICE_KEY')

    credential = AzureKeyCredential(languagekey)
    text_analytics_client = TextAnalyticsClient(
            endpoint=languageendpoint, 
            credential=credential)
    return text_analytics_client


"""
Validation fxns
"""
def get_document_file_path(document, document_file_path):
    """Retrieves document. If document is provided, it takes precedence than retrieving from document file path.

    Args:
        document (str): Document context
        document_file_path (str): Path to document file

    Return:
        (str): Document
    """
    if not document and not document_file_path:
        raise ValueError('Neither -d/--document or -p/--document-file-path values were provided. Exiting...')

    # Takes precedence than retrieving document from file path
    if document:
        return document

    if document_file_path == 'flag':
        filepath = filedialog.askopenfilename()
    else:
        filepath = os.path.relpath(document_file_path, os.getcwd())

    # Validate file path if value is provided
    if not os.path.isfile(filepath):
        raise ValueError(f'ERROR: Cannot find document file at: {document_file_path}. Exiting...')

    file_contents = open(filepath, 'r')

    return file_contents.read()


@click.command()
@click.option('-d', '--document', help='Text to analyze')
@click.option('-p', '--document-file-path', flag_value='flag', is_flag=False, default=None, help='Path to document file')
def keyphrases(document, document_file_path):
    document_contents = get_document_file_path(document, document_file_path)
    language_keyphrases(document_contents)


def language_keyphrases(text):
    client = __authenticate_client()
    keyphrase_result = client.extract_key_phrases(documents=[text])[0]

    print("Key Phrases:")
    for phrase in keyphrase_result.key_phrases:
        print(phrase)
    
    print('\n')