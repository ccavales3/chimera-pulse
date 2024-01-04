"""This is a helper file for core.translator.text_translator capability
"""
import os

# Import namespaces
import azure.cognitiveservices.speech as speech_sdk

# Globals
global speech_config


def __authenticate_client():
    """Authenticate service

    Returns:
        (TextTranslationClient): Authenticated client
    """
    global speech_config
    
    # Get Configuration Settings
    translatorkey = os.getenv('TRANSLATOR_SERVICE_KEY')
    translatorregion = os.getenv('TRANSLATOR_SERVICE_REGION')

    # Connect to Speech Config
    speech_config = speech_sdk.SpeechConfig(translatorkey, translatorregion)


def synthesizeText(targetLanguage, translatedObj):
    global speech_config
    
    __authenticate_client()
    
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
