"""Module that contains raw calls to Azure AI Translator
https://learn.microsoft.com/en-us/azure/ai-services/translator/

Reference:
    Documentation: https://learn.microsoft.com/en-us/azure/ai-services/translator/reference/v3-0-translate

    List of supported output languages - https://api.cognitive.microsofttranslator.com/languages?api-version=3.0&scope=translation

Example:
    chi translator translatetext -s en-US -t fil -c 'Hello, goodmorning'
"""
import os

import click
from dotenv import load_dotenv

# Import TextTranslation packages
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError

# Import helpers
from chimerapulse.core.speech import text_to_speech

# Load env vars
load_dotenv()


def __authenticate_client():
    """Authenticate service

    Returns:
        (TextTranslationClient): Authenticated client
    """
        
    # Get Configuration Settings
    translatorendpoint = os.getenv('TRANSLATOR_SERVICE_ENDPOINT')
    translatorkey = os.getenv('TRANSLATOR_SERVICE_KEY')
    translatorregion = os.getenv('TRANSLATOR_SERVICE_REGION')

    # Connect to Azure Translator Service
    credential = TranslatorCredential(translatorkey, translatorregion)

    return TextTranslationClient(endpoint=translatorendpoint, credential=credential)


# TODO: Modify -c to accept path to document
@click.command()
@click.option('-s', '--source-language', required=True, help='Source language')
@click.option('-t', '--target-language', required=True, help='Target language')
@click.option('-c', '--content', required=True, help='Content to be translated')
def translatetext(source_language, target_language, content):
    """Main command function called when calling text translator as a package
    """
    translator_translatetext(source_language, target_language, content)


def translator_translatetext(source_language, target_language, content):
    """Translate contect from source to target language

    Args:
        source_language (str): Source language
        target_language (str): Language to translate to
        content (str): Text to be translated
    """
    print(f"Translating from {source_language}")
    text_translator = __authenticate_client()

    try:
        input_text_elements = [InputTextItem(text=content)]

        response = text_translator.translate(content=input_text_elements, to=[target_language], from_parameter=source_language)
        translation = response[0] if response else None

        # Only one translation object per utterance
        translatedobj = translation.translations[0]
        print(f"Content was translated to: '{translatedobj.to}'.")
        print(f"Result: {translatedobj.text}\n")
        text_to_speech.synthesizeText(target_language, translatedobj.text)

    except HttpResponseError as exception:
        print(f"Error Code: {exception.error.code}")
        print(f"Message: {exception.error.message}")