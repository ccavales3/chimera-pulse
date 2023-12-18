"""
This file is the entry point for the create-py-cli package

Example:
    cpc template --name 'Caesar' --choose
"""
import click


def validate_options(ctx, param, value):
    """
    Calidate quality parameters

    Args:
        Default click.option callback parameters

    Return:
        value (str): value of validated option
    """
    print(f'value: {value}')

    return value


@click.command()
@click.option('--name', callback=validate_options, default='John Doe')
@click.option('--choose/--no-choose', default=False)
def template(name: str, choose: bool):
    """
    Prints out your name and your choice value

    Args:
        name (str): Name
        choose (bool): Choice value
    """
    print(f'Hello {name}. Your input value is {choose}')
