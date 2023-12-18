"""
This file calls module command function in src.template file

Example:
    python -m cpc.template
"""
from src.template import template

if __name__ == '__main__':
    template.template()  # pylint: disable=no-value-for-parameter
