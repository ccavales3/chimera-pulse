"""This file is the entry point for the ChimeraPulse package

Example:
    python -m <module_dir_path> <args>
    chi <module> <args>
"""
import click

# Import ChimeraPulse modules
from chimerapulse.core.language import conversation_summarization
from chimerapulse.core.language import document_summarization
from chimerapulse.core.language import key_phrases
from chimerapulse.core.language import named_entities
from chimerapulse.core.language import sentiment_analysis
from chimerapulse.core.language import entity_linking
from chimerapulse.core.speech import diarization
from chimerapulse.core.speech import language_identification
from chimerapulse.core.speech import video_transcription
from chimerapulse.core.translator import text_translator

# TODO: create fxn to run post call processing per chunk of transcription received


@click.command()
@click.option('-p', '--file-path', callback=language_identification.get_audio_file_path, flag_value='flag', is_flag=False, default=None, help='Path to audio file')
def translatespeech(file_path: str):
    targetLanguage = input("Enter a target language\n"
        "en = English\n"
        "es = Spanish\n"
        "fil = Filipino\n"
        "fr = French\n"
        "hi = Hindi\n"
        "ko = Korean\n"
        "ms = Malaysia\n").lower()
    
    print('\n')
      
    # Identify language from list and transcribe audio
    [source_language, result] = language_identification.speech_identifylanguage(file_path)

    # Translate text
    text_translator.translator_translatetext(source_language, targetLanguage, result.text)
    
    # Analyze Sentiment
    print(sentiment_analysis.language_analyzesentiment(result.text))
    
    # Extract Key Phrases
    print(key_phrases.language_keyphrases(result.text))
    
    # Named Entity Recognition
    print(named_entities.language_namedentites(result.text))
    
    # Entity Linking
    print(entity_linking.language_entitylinking(result.text))
    
    print('\n')

    print('--fin--')


# TODO: change callback validation. See translatespeech fxn
@click.command()
@click.option('-p', '--file-path', callback=language_identification.get_audio_file_path, flag_value='flag', is_flag=False, default=None, help='Path to audio file')
def convosummarization(file_path):
    """Diarize audio with mono channel and summarize conversation

    Args:
        file_path (str): Path to conversation audio file
    """
    diarization_result = diarization.speech_diarization(file_path)
    conversation_summarization.language_summarizeconversation('all', diarization_result)

    print('--fin--')


# TODO: change callback validation. See translatespeech fxn
@click.command()
@click.option('-p', '--file-path', callback=language_identification.get_audio_file_path, flag_value='flag', is_flag=False, default=None, help='Path to audio file')
def docsummarization(file_path):
    """TEMP entry point: Document summarization

    Args:
        file_path (str): Path to conversation audio file
    """
    document_contents = document_summarization.get_document_file_path(None, file_path)
    document_summarization.language_summarizedocument(document_contents)

    print('--fin--')


@click.command()
@click.option('-p', '--file-path', callback=video_transcription.get_video_file_path, flag_value='flag', is_flag=False, default=None, help='Path to video file')
@click.option('-d', '--detect-language', flag_value=True, is_flag=True, default=False, help='Detect language')
def summarizevideoconvo(file_path, detect_language):
    """Video convo summarization

    Args:
        file_path (str): Path to conversation audio file
    """
    [audio_filepath, source_language] = video_transcription.speech_videotranscription(file_path, detect_language)
    diarization_result = diarization.speech_diarization(audio_filepath, source_language)
    conversation_summarization.language_summarizeconversation('all', diarization_result)

    print('--fin--')
