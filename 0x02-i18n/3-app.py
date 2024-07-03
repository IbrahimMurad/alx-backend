#!/usr/bin/env python3
""" This is a basic Flask app that says Hello and uses Babel for i18n """
from flask import Flask, render_template, request
from flask_babel import Babel, _
from typing import Any


class Config:
    """ Config class that sets up app configuration"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """ Get locale to specify language translation """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def basic():
    """ Basic app that says Hello """
    return render_template('3-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
