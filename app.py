import os
import datetime
import flask
import logging
from apscheduler.schedulers.background import BackgroundScheduler
import data.db_session as db_session
from data.event import Event
from data.attendee import Attendee

app = flask.Flask(__name__)


# ------------------------------------------------------------
# Logging setup for Render
# ------------------------------------------------------------
# This ensures logs from the scheduler show up in Render's dashboard


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("event_tool_scheduler")


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

        total_deleted = 0
        for event in old_events:
            count = (
                session.query(Attendee)
                .filter(Attendee.event_id == event.id)
                .delete(synchronize_session=False)
            )
            total_deleted += count

        logger.info(
            f"[Scheduler] Cleanup ran at {datetime.datetime.now():%Y-%m-%d %H:%M:%S}, "
            f"removed {total_deleted} old attendees."
        )


def start_scheduler():
    """
    Starts the cleanup scheduler (once per deployment).
    """
    if os.environ.get("RUN_MAIN") == "true":  # ensures only one instance runs
        scheduler = BackgroundScheduler(daemon=True)
        scheduler.add_job(func=cleanup_old_attendees, trigger="interval", hours=24)
        scheduler.start()
        logger.info("[Scheduler] Background cleanup job started.")
    else:
        logger.info("[Scheduler] Skipped startup for non-main process.")


def create_app():
    setup_db()
    register_blueprints()
    start_scheduler()
    return app

# Ensure blueprints are registered even when imported by Gunicorn
create_app()

if __name__ == "__main__":
    app.run(debug=False)