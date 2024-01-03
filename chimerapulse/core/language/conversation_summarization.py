"""Module that contains raw call to Azure language service

List of supported languages for conversation summarization:
    https://learn.microsoft.com/en-us/azure/ai-services/language-service/summarization/language-support?tabs=conversation-summarization

Example:
    python -m chimerapulse.core.language summarizeconversation -p <args>
    chi language summarizeconversation -p
"""
import ast
import json
import os
from tkinter import filedialog

import click
from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient

# Import helper fxns
from chimerapulse.helpers import summarization as summarizationHelper

# Load env vars
load_dotenv()


def __authenticate_client():
    """Authenticate service

    Returns:
        (TextTranslationClient): Authenticated client
    """
    # Get Configuration Settings
    languageendpoint = os.getenv('TRANSLATOR_SERVICE_ENDPOINT')
    languagekey = os.getenv('TRANSLATOR_SERVICE_KEY')

    credential = AzureKeyCredential(languagekey)
    conversational_analysis_client = ConversationAnalysisClient(
            endpoint=languageendpoint, 
            credential=credential)
    return conversational_analysis_client


"""
Validation fxns
"""
def get_conversation_file_path(conversation_items, conversation_file_path):
    """Retrieves document. If document is provided, it takes precedence than retrieving from document file path.

    Args:
        conversation_items (str): Conversation items
        conversation_file_path (str): Path to conversation file

    Return:
        (str): Document
    """
    if not conversation_items and not conversation_file_path:
        raise ValueError('Neither -c/--conversation-items or -p/--conversation-file-path values were provided. Exiting...')

    # Takes precedence than retrieving document from file path
    if conversation_items:
        return conversation_items

    if conversation_file_path == 'flag':
        filepath = filedialog.askopenfilename()
    else:
        filepath = os.path.relpath(conversation_file_path, os.getcwd())

    # Validate file path if value is provided
    if not os.path.isfile(filepath):
        raise ValueError(f'ERROR: Cannot find document file at: {conversation_file_path}. Exiting...')

    file_contents = open(filepath, 'r')

    return file_contents.read()


@click.command()
@click.option('-t', '--tasks', default='all', help='Task context')
@click.option('-c', '--conversation-items', default=None, help='Conversation Items')
@click.option('-p', '--conversation-file-path', flag_value='flag', is_flag=False, default=None, help='Path to conversation items file')
def summarizeconversation(tasks, conversation_items, conversation_file_path):
    """Main command function called when calling conversation summarization as a package

    Args:
        tasks (str): Document context
        conversation_items (obj): Conversation items
        conversation_file_path (str): Path to conversation items file
    """
    task_document_contents = get_conversation_file_path(conversation_items, conversation_file_path)
    # language_summarizeconversation(tasks, json.loads(task_document_contents))
    language_summarizeconversation(tasks, task_document_contents)


def language_summarizeconversation(tasks, task_document_contents):
    client = __authenticate_client()
    tasks_obj = summarizationHelper.create_tasks(tasks)

    with client:
        poller = client.begin_conversation_analysis(
            task = {
                "displayName": "Analyze conversations from xxx",
                "analysisInput": {
                    "conversations": [{
                        "conversationItems": json.loads(task_document_contents),
                        "modality": "text",
                        "id": "conversation1",
                        "language": "en"
                    }],
                },
                "tasks": tasks_obj
            }
        )

        # view result
        result = poller.result()
        task_results = result["tasks"]["items"]
        for task in task_results:
            print(f"\n{task['taskName']} status: {task['status']}")
            task_result = task["results"]
            if task_result["errors"]:
                print("... errors occurred ...")
                for error in task_result["errors"]:
                    print(error)
            else:
                conversation_result = task_result["conversations"][0]
                if conversation_result["warnings"]:
                    print("... view warnings ...")
                    for warning in conversation_result["warnings"]:
                        print(warning)
                else:
                    summaries = conversation_result["summaries"]
                    for summary in summaries:
                        print(f"{summary['aspect']}: {summary['text']}")
