"""This file contains logic for ChimeraPulse entry point(chimerapulse). Business logic is split into this file so it can be called through both CLI and REST API
"""
from chimerapulse.core.language import document_summarization


def summarization_helper(file_path):
    document_contents = document_summarization.get_document_file_path(None, file_path)
    return document_summarization.language_summarizedocument(document_contents)

