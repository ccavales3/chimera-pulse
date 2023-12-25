"""This file calls module command function in chimerapulse.core.translator file

Example:
    python -m chimerapulse.core.translator <submodule>
    chi chimerapulse core translator <submodule>
"""
from chimerapulse.core.translator import translator

if __name__ == '__main__':
    translator.translator()  # pylint: disable=no-value-for-parameter
