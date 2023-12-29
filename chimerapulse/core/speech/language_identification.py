"""Module that contains raw calls to Azure speech service
https://learn.microsoft.com/en-us/azure/ai-services/speech-service/

Reference:
    https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-identification?tabs=once&pivots=programming-language-python

List of supported language for language identification:
    https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=language-identification

Example:
    python -m chimerapulse.core.speech identifylanguage <args>
    chi speech identifylanguage -p
"""
import os
from tkinter import filedialog

import click
from dotenv import load_dotenv

# Import Azure speech SDK
import azure.cognitiveservices.speech as speechsdk

# Load env vars
load_dotenv()


"""
Private fxns
"""
def __identify_language(audio_config, languages):
    """Retrieves and processes language of audio

    Args:
        audio_config (AudioConfig): Speeck SDK AudioConfig object
        languages ([str]): Array of strings containing languages to detect

    Return:
        [detected_language(str), result(obj)]: Detected language and result object
    """
    speech_config = __authenticate_client()
    speech_config.set_property(speechsdk.PropertyId.Speech_LogFilename, './chimera_pulse_logs.txt')
    auto_detect_source_language_config = \
        speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=languages)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, 
        auto_detect_source_language_config=auto_detect_source_language_config, 
        audio_config=audio_config)

    print("Speak now...\n")
    result = speech_recognizer.recognize_once()

    # Throw if not transcribed correctly. Might be an issue with the microphone.
    if not result.text:
        raise ValueError("Result empty. Check if microphone is enabled.")

    print(f"Transcription: {result.text}");
    auto_detect_source_language_result = speechsdk.AutoDetectSourceLanguageResult(result)
    detected_language = auto_detect_source_language_result.language
    print(f"Detected language: {detected_language}\n")

    return [detected_language, result]


def __authenticate_client():
    """Authenticates speech client

    Return:
        (SpeechConfig): Speech client
    """
    # Get Configuration Settings
    speechkey = os.getenv('SPEECH_SERVICE_KEY')
    speechregion = os.getenv('SPEECH_SERVICE_REGION')

    # Connect to Azure Language Service
    return speechsdk.SpeechConfig(speechkey, speechregion)


"""
Validation fxns
"""
def get_audio_file_path(ctx, param, value):
    """Retrieves audoi file path

    Args:
        ctx (obj): Context
        param (str): Parameter
        value (Any): Value

    Return:
        (str): File path
    """
    filepath = ''
    print('Collecting audio...')

    # Do nothing if option is not specified
    if value == None:
        return None
        # filepath = value

    # Open file dialog if path is empty
    if value == 'flag':
        filepath = filedialog.askopenfilename()
    else:
        filepath = os.path.relpath(value, os.getcwd())


    # TODO: Verify file is an audio file here
    # Validate file path if value is provided
    if not os.path.isfile(filepath):
        raise ValueError(f'ERROR: Cannot find audio file at: {filepath}. Exiting...')

    print(f'Audio file path: {filepath}')
    return filepath


@click.command()
@click.option('-p', '--audio-file-path', callback=get_audio_file_path, flag_value='flag', is_flag=False, default=None, help='Path to audio file')
def identifylanguage(audio_file_path: str|None=None):
    """Main command function called when calling language identification as a package

    Args:
        audio_file_path (str): Path to audio file
    """
    speech_identifylanguage(audio_file_path=audio_file_path)


# Named using <module>_<methodname>
def speech_identifylanguage(audio_file_path: str|None=None):
    """Detects spoken language

    Args:
        audio_file_path (str): Path to audio file
    """
    # TODO: Will parameterized through CLI
    languages=['en-US', 'fr-FR', 'id-ID', 'es-ES']

    if audio_file_path:
        print('Audio file path verified...')
        # Configure audio with filename if -p option is provided
        audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
    else:
        print('Audio file not provided.')
        print('Retrieving audio from microphone')
        # Recognize from microphone if -p option is not provided
        audio_config = speechsdk.AudioConfig(use_default_microphone=True)

    print('Initiating language detection...')

    [source_language, result] = __identify_language(audio_config, languages)

    return [source_language, result]
