"""This file is the entry point for the ChimeraPulse package

Example:
    python -m <module_dir_path> <args>
    chi <module> <args>
"""
import click

# Import ChimeraPulse modules
from chimerapulse.core.speech import language_identification
from chimerapulse.core.translator import text_translator
from chimerapulse.core.language import sentiment_analysis
from chimerapulse.core.language import key_phrases
from chimerapulse.core.language import named_entities


@click.command()
@click.option('-p', '--audio-file-path', callback=language_identification.get_audio_file_path, flag_value='flag', is_flag=False, default=None, help='Path to audio file')
def main(audio_file_path: str):
    # Identify language from list and transcribe audio
    [source_language, result] = language_identification.speech_identifylanguage(audio_file_path)

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


if __name__ == '__main__':
    main()
