"""This file serves as the entry point for the chimerapulse package

Example:
    # Running project modules
    python -m chimerapulse.<module_name> <args>

    # Running project as a library
    chi <args>
    chimerapulse <args>

    # Running project modules as a library
    chi <module> <args>
    chimerapulse <module> <args>
"""    
import click

from chimerapulse import chimerapulse
from chimerapulse.core.language import language
from chimerapulse.core.speech import speech
from chimerapulse.core.translator import translator

@click.group()
def commands():
    pass

# TODO: Change "main" to more appropriate name
# ChimeraPulse main commands
commands.add_command(chimerapulse.case1)
commands.add_command(chimerapulse.case2)
commands.add_command(chimerapulse.case3)

# ChimeraPulse core capabilities
commands.add_command(language.language)
commands.add_command(speech.speech)
commands.add_command(translator.translator)
