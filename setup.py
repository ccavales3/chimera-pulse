"""Project ChimeraPulse

    Example:
        python setup.py install
"""
from setuptools import find_packages
from setuptools import setup

# Only install package dependencies in install_requires
setup(
    name='chimerapulse',
    version='0.0.1',
    description='A conversation analytics and congnitive tool',
    entry_points={
        'console_scripts': [
            'chi = chimerapulse.commands:commands',
            'chimerapulse = chimerapulse.commands:commands'
        ]
    },
    url='https://github.com/ccavales3/chimera-pulse',
    author='Caesar Cavales',
    author_email='c.cavales3@gmail.com',
    packages=find_packages(),
    install_requires=[
        'azure-ai-textanalytics==5.3.0',            # https://learn.microsoft.com/en-us/azure/ai-services/language-service/summarization/quickstart?pivots=programming-language-python&tabs=document-summarization%2Cmacos
        'azure-ai-translation-text==1.0.0b1',       # https://learn.microsoft.com/en-us/azure/ai-services/translator/text-sdk-overview?tabs=python
        'azure-cognitiveservices-speech==1.30.0',   # https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-sdk
        'azure-core==1.29.5',                       # https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/core/azure-core
        'click==8.1.7',                             # https://github.com/pallets/click
        'playsound==1.3.0',                         # https://github.com/TaylorSMarks/playsound
        'python-dotenv==1.0.0',
        'PyObjC==10.1',
    ],
    zip_safe=False
)
