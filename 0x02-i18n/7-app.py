#!/usr/bin/env python3
""" Basic Flask app """
from flask import (
    Flask,
    render_template,
    request,
    g,
)
from flask_babel import Babel, _
from typing import Any
from pytz import timezone
from pytz.exceptions import UnknownTimeZoneError


users = {
    1: {
        "name": "Balou",
        "locale": "fr",
        "timezone": "Europe/Paris"
        },
    2: {
        "name": "Beyonce",
        "locale": "en",
        "timezone": "US/Central"
        },
    3: {
        "name": "Spock",
        "locale": "kg",
        "timezone": "Vulcan"
        },
    4: {
        "name": "Teletubby",
        "locale": None,
        "timezone": "Europe/London"
        },
}


def get_user(id: (int | None)) -> (dict | None):
    """ Get user from users (the db mock) """
    if id in users:
        return users[id]
    return None


class Config:
    """ Config class to set up app configuration """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@app.before_request
def before_request() -> None:
    """ Get user and set it as a global on g.user """
    user_id = request.args.get('login_as', None)
    if user_id:
        user_id = int(user_id)
    setattr(g, 'user', get_user(user_id))


@babel.localeselector
def get_locale() -> (str | None):
    """ Get locale to specify language translation """
    if request.args.get('locale') in app.config['LANGUAGES']:
        return request.args.get('locale')
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user.get('locale')
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> (str | None):
    """ Get timezone to specify time translation """
    if request.args.get('timezone', None):
        userTimezone = request.args.get('timezone')
    if g.user:
        userTimezone = g.user.get('timezone')
    try:
        timezone(userTimezone)
        return userTimezone
    except UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/', strict_slashes=False)
def basic() -> Any:
    """ Basic app that says Hello """
    username = None
    if g.user:
        username = g.user.get('name')
    return render_template('6-index.html', username=username)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
