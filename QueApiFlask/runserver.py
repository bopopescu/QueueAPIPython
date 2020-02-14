"""
This script runs the QueApiFlask application using a development server.
"""

from os import environ
from QueApiFlask import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    app.run(host='0.0.0.0', port='9000')
