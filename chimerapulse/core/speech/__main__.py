"""This file calls module command function in chimerapulse.core.speech file

Example:
    python -m chimerapulse.core.speech <submodule>
    chi chimerapulse core speech <submodule>
"""
from chimerapulse.core.speech import speech

if __name__ == '__main__':
    speech.speech()  # pylint: disable=no-value-for-parameter
