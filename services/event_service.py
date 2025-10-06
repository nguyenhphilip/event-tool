from typing import Optional, List
from data.event import Event
from data.attendee import Attendee
from data.db_session import get_session
import re


def add_attendee(event_id: int, name: str) -> Attendee:
    with get_session() as session:
        attendee = Attendee(name=name, event_id=event_id)
        session.add(attendee)
        return attendee


def get_all_events() -> List[Event]:
    with get_session() as session:
        return session.query(Event).order_by(Event.event_datetime.desc()).all()


def get_latest_events(limit: int = 5) -> List[Event]:
    with get_session() as session:
        return (
            session.query(Event)
            .order_by(Event.event_datetime.desc())
            .limit(limit)
            .all()
        )


def find_event_by_slug(event_slug: str) -> Optional[Event]:
    with get_session() as session:
        return session.query(Event).filter(Event.event_slug == event_slug).first()


def create_event(eventname: str, location: str, event_datetime, description: str, user_id: int) -> Optional[Event]:
    event = Event()
    event.title = eventname
    event.location = location
    event.description = description
    event.event_datetime = event_datetime
    event.user_id = user_id

    # generate slug
    event_slug = eventname.lower().strip().replace("'", "")
    event_slug = re.sub(r"\s+", "-", event_slug)
    event_slug = re.sub(r"[^a-z0-9-]", "", event_slug)
    event.event_slug = event_slug

    with get_session() as session:
        session.add(event)
        return event