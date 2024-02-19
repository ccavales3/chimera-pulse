import os
from flask import Flask

# Import helper fxns
from chimerapulse.helpers import chimerapulse_helper

# TODO: Move this to a common util
from chimerapulse.core.speech import language_identification

app = Flask(__name__)
print(__name__)

#TODO: Add help for '/' route

@app.route('/health')
def health():
    return 'Server is up!'


@app.route('/v1/summarization')
def summarization():
    # TODO: Temp value
    temp_file_path = "/Users/caesarcavales/Documents/Developer/chimera-pulse/sample docs/Toyotas New Engine.txt"
    file_path = os.path.relpath(temp_file_path, os.getcwd())
    return chimerapulse_helper.summarization_helper(file_path)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
