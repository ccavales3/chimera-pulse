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
from chimerapulse.core.speech import diarization
from chimerapulse.core.speech import language_identification
from chimerapulse.core.translator import text_translator

# TODO: create fxn to run post call processing per chunk of transcription received


@click.command()
@click.option('-p', '--file-path', callback=language_identification.get_audio_file_path, flag_value='flag', is_flag=False, default=None, help='Path to audio file')
def translatespeech(file_path: str):
    # Identify language from list and transcribe audio
    [source_language, result] = language_identification.speech_identifylanguage(file_path)

    # Translate text
    text_translator.translator_translatetext(source_language, 'fil', result.text)
    
    # Analyze Sentiment
    print(sentiment_analysis.language_analyzesentiment(result.text))
    
    # Extract Key Phrases
    print(key_phrases.language_keyphrases(result.text))
    
    # Named Entity Recognition
    print(named_entities.language_namedentites(result.text))
    
    print('\n')

    print('--fin--')


@click.command()
@click.option('-p', '--file-path', callback=diarization.get_conversation_file_path, flag_value='flag', is_flag=False, default=None, help='Path to audio file')
def convosummarization(file_path):
    """Diarize audio with mono channel and summarize conversation

    Args:
        file_path (str): Path to conversation audio file
    """
    diarization_result = diarization.speech_diarization(file_path)
    conversation_summarization.language_summarizeconversation('all', diarization_result)

    # print(diarization_result)

    print('--fin--')


@click.command()
@click.option('-p', '--file-path', flag_value='flag', is_flag=False, default=None, help='Path to audio file')
def docsummarization(file_path):
    """TEMP entry point: Document summarization

    Args:
        file_path (str): Path to conversation audio file
    """
    document_contents = document_summarization.get_document_file_path(None, file_path)
    document_summarization.language_summarizedocument(document_contents)

    print('--fin--')

# if __name__ == '__main__':
#     main()
