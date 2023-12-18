from setuptools import find_packages
from setuptools import setup

# Only install package dependencies in install_requires
setup(
    name='create-py-cli',
    version='1.0.0',
    description='Blueprint for python CLI tool',
    entry_points={
        'console_scripts': [
            'cpc = src.main:entry_point'
        ]
    },
    url='https://github.com/ccavales3/create-py-cli',
    author='Caesar Cavales',
    author_email='c.cavales3@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=[
            'click==8.0.1'      # https://github.com/pallets/click
    ],
    zip_safe=False
)
