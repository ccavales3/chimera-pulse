"""
This file unittests the template.py file
"""
from click.testing import CliRunner
from src.template import template


def test_template_default():
    """
    Should print out default values
    """
    runner = CliRunner()
    result = runner.invoke(template.template)

    print(f'result: {result.output}')
    assert result.output == 'value: John Doe\nHello John Doe. Your input value is False\n'


def test_template_params():
    """
    Should print out text with passed params
    """
    runner = CliRunner()
    result = runner.invoke(template.template, ['--name', 'Caesar was here', '--choose'])

    print(f'result: {result.output}')
    assert result.output == ('value: Caesar was here\n'
                             'Hello Caesar was here. Your input value is True\n')
