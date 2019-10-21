from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import argparse

import api

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite/messages.db'

db = SQLAlchemy(app)

if __name__ == '__main__':
    api.ApiView.register(app)

    parsed_argument = argparse.ArgumentParser()
    parsed_argument.add_argument('--port', type=int)
    parsed_argument = parsed_argument.parse_args()

    app.run(port=parsed_argument.port)
