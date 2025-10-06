import flask
from flask import jsonify
import infrastructure.cookie_auth as cookie_auth
# load data from event_services. later we'll use a database that certain people can update
import services.event_service as event_service
from data.event import Event

blueprint = flask.Blueprint('home', __name__, template_folder='templates')


@blueprint.route("/")
def index():
    """route for handling requests to root/home page"""
    # flask method 'render_template' automatically looks in templates folder for templates
    # events = we define an object 'events' so that this route can access and do stuff with our events data
    return flask.render_template('home/index.html', 
                                 events = event_service.get_latest_events(),
                                 user_id = cookie_auth.get_user_id_via_auth_cookie(flask.request))


@blueprint.route("/about")
def about():

    return flask.render_template('home/about.html',
                                 user_id = cookie_auth.get_user_id_via_auth_cookie(flask.request))
