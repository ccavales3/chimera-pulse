"""Module that calls Azure Sentiment Analysis
https://learn.microsoft.com/en-us/azure/ai-services/language-service/sentiment-opinion-mining/overview?tabs=prebuilt

Example:
    python -m chimerapulse.core.language analyzesentiment <args>
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
def analyzesentiment(text):
    language_analyzesentiment(text)
    
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

def language_analyzesentiment(text):
    client = __authenticate_client()
    sentiment_result = client.analyze_sentiment(documents=[text])
    doc_result = [doc for doc in sentiment_result if not doc.is_error]
    
    for document in doc_result:
        print("Overall Sentiment: {}".format(document.sentiment))

        for sentence in document.sentences:
            print("Sentence: {}".format(sentence.text))
            print("Sentence sentiment: {}".format(sentence.sentiment))
        
        print('\n')