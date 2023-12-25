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

# from chimerapulse.chimerapulse import chimerapulse
from chimerapulse import chimerapulse

@click.group()
def commands():
    pass

commands.add_command(chimerapulse.main)
