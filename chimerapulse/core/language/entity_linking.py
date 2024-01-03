"""Module that calls Azure Entity Linking
https://learn.microsoft.com/en-us/azure/ai-services/language-service/entity-linking/overview

Example:
    python -m chimerapulse.core.language entitylinking -d 'Microsoft was founded by Bill Gates and Paul Allen.'
    chi language entitylinking <args>
"""

import os
from tkinter import filedialog

import click
from dotenv import load_dotenv

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Load env vars
load_dotenv()

# Declare global variables
links = []
verbose = False

"""
Private fxns
"""
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


def __vprint(text):
    global verbose

    if (verbose):
        print(text)


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
@click.option('-v', '--verbose-print', is_flag=True, flag_value=True, default=False, help='Prints response instead of returning as JSON object')
def entitylinking(document, document_file_path, verbose_print):
    global verbose
    
    verbose = verbose_print
    
    document_contents = get_document_file_path(document, document_file_path)
    language_entitylinking(document_contents)


def language_entitylinking(text):
    global verbose
    global links
    
    client = __authenticate_client()
    entitylinking_result = client.recognize_linked_entities(documents=[text])[0]

    __vprint("Linked Entities:")
    for entity in entitylinking_result.entities:
        __vprint(f'"Name:" {entity.name}')
        __vprint(f'"Id:" {entity.data_source_entity_id}')
        __vprint(f'"Url:" {entity.url}')
        __vprint(f'"Data Source:" {entity.data_source}')
        __vprint("Matches:")
        for match in entity.matches:
            __vprint(f'"Text:" {match.text}')
            __vprint('\n')
        __vprint('\n')
        links.append({
            "name": entity.name,
            "id": entity.data_source_entity_id,
            "url": entity.url,
            "data_source": entity.data_source,
            "matches": match.text
        })
    
    if not verbose:
        return links