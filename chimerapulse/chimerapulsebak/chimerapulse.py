"""
This file is the entry point for the create-py-cli package

Example:
    python -m chimerapulse <args>
    chi <module> <args>
"""
from dotenv import load_dotenv
from tkinter import filedialog
import os
from playsound import playsound

import click

# Import TextTranslation packages
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError

# Import namespaces
import azure.cognitiveservices.speech as speech_sdk

@click.command()
@click.option('-p', '--audio-file-path', help='Path to audio file')
def main(audio_file_path: str):
    print('here in main')
    print(f'audio file path: {audio_file_path}')

def main_bak(audio_file_path):
    try:
        global audio_config
        global speech_config
        global translation_config
        global cog_endpoint
        global cog_key
        global cog_region      

        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        cog_key = os.getenv('COG_SERVICE_KEY')
        cog_region = os.getenv('COG_SERVICE_REGION')


        # Configure speech
        speech_config = speech_sdk.SpeechConfig(cog_key, cog_region)
        speech_config.set_property(speech_sdk.PropertyId.Speech_LogFilename, './chimera_pulse_logs.txt')

        # Configure Audio
        ## Recognize from microphone
        # audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
        ## Recognize from file
        # audioFile = os.path.expanduser("~/Downloads/testMic.wav")
        audioFile = filedialog.askopenfilename()

        if not os.path.isfile(audioFile):
            raise ValueError(f"Cannot find audiofile at: {audioFile}")

        audio_config = speech_sdk.audio.AudioConfig(filename=audioFile)

        # Get user input
        targetLanguageArray = ["en", "es", "fil", "fr", "hi", "ko", "ms"]
        targetLanguage = input("Enter a target language\n"
        "en = English\n"
        "es = Spanish\n"
        "fil = Filipino\n"
        "fr = French\n"
        "hi = Hindi\n"
        "ko = Korean\n"
        "ms = Malaysia\n"
        "Enter anything else to stop\n").lower()

        if targetLanguage in targetLanguageArray:
            inputOpt = ""
            while inputOpt != "exit":
                # Detect Language
                [sourceLanguage, result] = DetectLanguage()
                Translate(sourceLanguage, targetLanguage, result.text)

                inputOpt = input("Press any key to continue. Otherwise, type 'exit' to quit application.\n")
    except Exception as ex:
        print(ex)

def DetectLanguage(): 
    auto_detect_source_language_config = \
        speech_sdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["en-US", "fr-FR", "id-ID", "es-ES"])
    speech_recognizer = speech_sdk.SpeechRecognizer(
            speech_config=speech_config, 
            auto_detect_source_language_config=auto_detect_source_language_config, 
            audio_config=audio_config)
    print("Speak now...\n")
    result = speech_recognizer.recognize_once()

    # Throw if not transcribed correctly. Might be an issue with the microphone.
    if not result.text:
        raise ValueError("Result empty. Check if microphone is enabled.")

    print(f"Transcription: {result.text}");
    auto_detect_source_language_result = speech_sdk.AutoDetectSourceLanguageResult(result)
    detected_language = auto_detect_source_language_result.language
    print(f"Detected language: {detected_language}\n")

    return [detected_language, result]

def Translate(sourceLanguage, targetLanguage, text):
    credential = TranslatorCredential(cog_key, cog_region)
    text_translator = TextTranslationClient(endpoint=cog_endpoint, credential=credential)
    print(f"Translating from {sourceLanguage}")

    try:
        input_text_elements = [ InputTextItem(text = text) ]

        response = text_translator.translate(content = input_text_elements, to = [targetLanguage], from_parameter = sourceLanguage)
        translation = response[0] if response else None

        # Only one translation object per utterance
        translatedObj = translation.translations[0]
        print(f"Text was translated to: '{translatedObj.to}'.")
        print(f"Result: {translatedObj.text}\n")
        _SynthesizeText(targetLanguage, translatedObj)

    except HttpResponseError as exception:
        print(f"Error Code: {exception.error.code}")
        print(f"Message: {exception.error.message}")

def _SynthesizeText(targetLanguage, translatedObj):
    print("Synthesizing text...\n")
    # Synthesize translation
    voices = {
            "en": "en-US-SaraNeural",
            "es": "es-ES-ElviraNeural",
            "fil": "fil-PH-BlessicaNeural",
            # "fr": "fr-FR-HenriNeural",
            "fr": "fr-FR-CoralieNeural",
            "hi": "hi-IN-MadhurNeural",
            "ko": "ko-KR-SunHiNeural",
            "ms": "ms-MY-YasminNeural"

    }
    speech_config.speech_synthesis_voice_name = voices.get(targetLanguage)
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
    speak = speech_synthesizer.speak_text_async(translatedObj.text).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)

if __name__ == "__main__":
    main()
