"""Module that calls Azure Sentiment Analysis
https://learn.microsoft.com/en-us/azure/ai-services/language-service/key-phrase-extraction/overview

Example:
    python -m chimerapulse.core.language keyphrases <args>
"""

import os

import click
from dotenv import load_dotenv

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Load env vars
load_dotenv()

# TODO: Add click parameters
@click.command()
def keyphrases(text):
    language_keyphrases(text)
    
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

def language_keyphrases(text):
    client = __authenticate_client()
    keyphrase_result = client.extract_key_phrases(documents=[text])[0]

    print("Key Phrases:")
    for phrase in keyphrase_result.key_phrases:
        print(phrase)
    
    print('\n')