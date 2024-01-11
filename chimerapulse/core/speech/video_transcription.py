"""Module containing external library to extract audio out of a video and uses 'language identification' logic call to Azure speech service

Prerequisite:
    Needs ffmpeg. Install if it doesn't exist in your system
    brew install ffmpeg

Reference:
    https://medium.com/nerd-for-tech/transcribe-audio-from-video-with-azure-cognitive-services-a4589a12d74f
    https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-identification?tabs=once&pivots=programming-language-python

List of supported language for language identification:
    https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=language-identification

Example:
    python -m chimerapulse.core.speech transcribevideo <args>
    chi speech transcribevideo -p
"""
import os
from tkinter import filedialog

import click
from dotenv import load_dotenv

# Import Azure speech SDK
# import azure.cognitiveservices.speech as speechsdk

# Import external packages
# from moviepy import VideoFileClip
from moviepy.editor import VideoFileClip

# Import 'core'
from chimerapulse.core.speech import language_identification

# Load env vars
load_dotenv()


"""
Validation fxns
"""
def get_video_file_path(ctx, param, value):
    """Retrieves audoi file path

    Args:
        ctx (obj): Context
        param (str): Parameter
        value (Any): Value

    Return:
        (str): File path
    """
    filepath = ''
    print('Extracting audio...')

    # Do nothing if option is not specified
    if value == None:
        return None

    # Open file dialog if path is empty
    if value == 'flag':
        filepath = filedialog.askopenfilename()
    else:
        filepath = os.path.relpath(value, os.getcwd())


    # TODO: Verify file is a video file here
    # Validate file path if value is provided
    if not os.path.isfile(filepath):
        raise ValueError(f'ERROR: Cannot find video file at: {filepath}. Exiting...')

    print(f'Video file path: {filepath}')
    return filepath


@click.command()
@click.option('-p', '--video-file-path', callback=get_video_file_path, flag_value='flag', is_flag=False, default=None, help='Path to video file')
@click.option('-d', '--detect-language', flag_value=True, is_flag=True, default=False, help='Detect language')
def videotranscription(video_file_path, detect_language):
    """Main command fxn called when transcribing audio extracted from a video

    Args:
        video_file_path (str): Path to audio file
    """
    speech_videotranscription(video_file_path, detect_language)


def speech_videotranscription(video_file_path, detect_language):
    """
    """
    transcribed_audio_file_path = 'temp_transcribed_vid.wav'
    # video = VideoFileClip("your_video.mp4")
    video = VideoFileClip(video_file_path)
    audio = video.audio
    audio.write_audiofile(transcribed_audio_file_path, ffmpeg_params=['-ac', '1'])

    audio_filepath = f'{os.getcwd()}/{transcribed_audio_file_path}'

    print(f'detect_language: {detect_language}')
    source_language='en-US'
    if detect_language:
        [source_language] = language_identification.speech_identifylanguage(audio_filepath)
    # TODO: Delete file here

    return [audio_filepath, source_language]
