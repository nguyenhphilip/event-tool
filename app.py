import flask
import os
import data.db_session as db_session
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from data.event import Event
from data.attendee import Attendee


app = flask.Flask(__name__)


def main():
    register_blueprints()
    setup_db()
    start_scheduler(app)
    app.run(debug=True)


def setup_db():
    # directory we're working in
    db_file = os.path.join(
        os.path.dirname(__file__),
        'db',
        'events.sqlite'
    )
    print(f"DB file path: {db_file}")
    db_session.global_init(db_file)


def register_blueprints():
    
    """
    Blueprints are another way of mapping URLs to the actions we want the app to perform.
    If our views live in another file (e.g. the views folder) we need to import and register them
    since the app is run here, in this file "app.py"
    """

    from views import home_views
    from views import event_views
    from views import user_views

    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(event_views.blueprint)
    app.register_blueprint(user_views.blueprint)


def cleanup_old_attendees():
    session = db_session.create_session()
    cutoff = datetime.datetime.now() - datetime.timedelta(days=5)
    old_events = session.query(Event).filter(Event.event_datetime < cutoff).all()
    
    for event in old_events:
        session.query(Attendee).filter(Attendee.event_id == event.id).delete()
    
    session.commit()


def start_scheduler(app):
    if os.environ.get("RUN_MAIN") == "true":  # ensures only one worker starts it
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=cleanup_old_attendees, trigger="interval", hours=24)
        scheduler.start()


def create_app():
    setup_db()
    register_blueprints()
    start_scheduler(app)
    return app


app = create_app()


if __name__ == "__main__":
    app.run()