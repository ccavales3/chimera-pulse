"""This file calls module command function in chimerapulse.core.language file

Example:
    python -m chimerapulse.core.language <submodule>
    chi chimerapulse core language <submodule>
"""
from chimerapulse.core.language import language


if __name__ == '__main__':
    language.language()  # pylint: disable=no-value-for-parameter
