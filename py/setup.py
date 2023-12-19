"""
Project ChimeraPulse
"""
from setuptools import setup

# Only install package dependencies in install_requires
setup(
    name='chimerapulse',
    version='0.0.1',
    description='A conversation analytics and congnitive tool',
    url='https://github.com/ccavales3/chimera-pulse',
    author='Caesar Cavales',
    author_email='c.cavales3@gmail.com',
    install_requires=[
        'azure-ai-translation-text==1.0.0b1',       # https://learn.microsoft.com/en-us/azure/ai-services/translator/text-sdk-overview?tabs=python
        'azure-cognitiveservices-speech==1.30.0',   # https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-sdk
        'azure-core==1.29.5',                       # https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/core/azure-core
        'playsound==1.3.0',                         # https://github.com/TaylorSMarks/playsound
        'python-dotenv==1.0.0',
        'PyObjC==10.1'
    ]
)
