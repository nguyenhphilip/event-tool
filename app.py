import os
import datetime
import flask
from apscheduler.schedulers.background import BackgroundScheduler
import data.db_session as db_session
from data.event import Event
from data.attendee import Attendee

app = flask.Flask(__name__)


def main():
    setup_db()
    register_blueprints()
    start_scheduler()
    app.run(debug=False)


def setup_db():
    db_file = os.path.join(os.path.dirname(__file__), 'db', 'events.sqlite')
    print(f"DB file path: {db_file}")
    db_session.global_init(db_file)


def register_blueprints():
    from views import home_views, event_views, user_views
    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(event_views.blueprint)
    app.register_blueprint(user_views.blueprint)


def cleanup_old_attendees():
    """Delete attendees for events older than 5 days."""
    from data.db_session import get_session

    cutoff = datetime.datetime.now() - datetime.timedelta(days=5)
    with get_session() as session:
        old_events = session.query(Event).filter(Event.event_datetime < cutoff).all()
        for event in old_events:
            session.query(Attendee).filter(Attendee.event_id == event.id).delete()


def start_scheduler():
    """
    Starts the cleanup scheduler, but ensures it's only launched once
    (avoids duplicate jobs in multi-worker environments like Render).
    """
    if os.environ.get("RUN_MAIN") == "true":  # ensures only main process starts it
        scheduler = BackgroundScheduler(daemon=True)
        scheduler.add_job(func=cleanup_old_attendees, trigger="interval", hours=24)
        scheduler.start()
        print("Background scheduler started.")
    else:
        print("Scheduler not started in this process (RUN_MAIN != true).")


def create_app():
    setup_db()
    register_blueprints()
    start_scheduler()
    return app


app = create_app()

if __name__ == "__main__":
    main()