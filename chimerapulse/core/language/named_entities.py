"""Module that calls Azure Named Entity Recognition
https://learn.microsoft.com/en-us/azure/ai-services/language-service/named-entity-recognition/overview

Example:
    python -m chimerapulse.core.language namedentites -d 'I had a wonderful trip to Paris last week.'
    chi language namedentites <args>
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
entities = []
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
def namedentites(document, document_file_path, verbose_print):
    global verbose
    
    verbose = verbose_print    
    
    document_contents = get_document_file_path(document, document_file_path)
    language_namedentites(document_contents)


def language_namedentites(text):
    global verbose
    global entities
    
    client = __authenticate_client()
    namedentities_result = client.recognize_entities(documents=[text])[0]
    
    # Currently a bug in Azure API. Using a set to work around duplicate value issue
    entity_set = set()

    # Duplicate text with different categories will be skipped with this solution.
    # The first category will be the one that is printed.
    __vprint("Named Entities:")
    for entity in namedentities_result.entities:
        # Check if current entity already exists in the set
        if not(entity.text in entity_set):
            __vprint(f'"Text:" {entity.text}')
            __vprint(f'"Category:" {entity.category}')
            __vprint(f'"Subcategory:" {entity.subcategory}')
            __vprint('\n')
            entities.append({
                "text": entity.text,
                "category": entity.category,
                "subcategory": entity.subcategory
            })
        entity_set.add(entity.text)
        
    if not verbose:
        return entities