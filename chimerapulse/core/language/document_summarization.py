"""Module that contains raw call to Azure language service

List of supported languages for document summarization:
    https://learn.microsoft.com/en-us/azure/ai-services/language-service/summarization/language-support?tabs=conversation-summarization

Example:
    python -m chimerapulse.core.language summarizedocument -p <args>
    chi language summarizedocument -p
"""
import os
from tkinter import filedialog

import click
from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import AbstractiveSummaryAction, ExtractiveSummaryAction, TextAnalyticsClient


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
@click.option('-d', '--document', default=None, help='Document context')
@click.option('-p', '--document-file-path', flag_value='flag', is_flag=False, default=None, help='Path to document file')
def summarizedocument(document, document_file_path):
    """Main command function called when calling document summarization as a package

    Args:
        document (str): Document context
        document_file_path (str): Path to document file
    """
    document_contents = get_document_file_path(document, document_file_path)
    language_summarizedocument(document_contents)


def language_summarizedocument(document):
    client = __authenticate_client()

    poller = client.begin_analyze_actions(
        documents=[document],
        actions=[
            AbstractiveSummaryAction(),
            ExtractiveSummaryAction()
        ],
    )

    document_results = poller.result()

    for document in document_results:
        for result in document:
            if result.kind == 'AbstractiveSummarization':
                print('Abstractive Summary:\n')
                [print(f'{summary.text}\n') for summary in result.summaries]
            elif result.kind == 'ExtractiveSummarization':
                print('Extractive Summary:\n')
                [print(f'-{sentence.text}') for sentence in result.sentences]
