from typing import Optional, List
from data.event import Event
from data.attendee import Attendee
from data.db_session import get_session
from sqlalchemy.orm import joinedload, selectinload
import re


def add_attendee(event_id: int, name: str) -> Attendee:
    with get_session() as session:
        attendee = Attendee(name=name, event_id=event_id)
        session.add(attendee)
        return attendee


def get_all_events() -> List[Event]:
    """
    Returns all events with related user and attendees preloaded.
    Prevents DetachedInstanceError by eager-loading relationships.
    """
    with get_session() as session:
        return (
            session.query(Event)
            .options(
                joinedload(Event.user),       # eager-load event.host (User)
                selectinload(Event.attendees) # prefetch attendees efficiently
            )
            .order_by(Event.event_datetime.desc())
            .all()
        )


def get_latest_events(limit: int = 5) -> List[Event]:
    """
    Returns the N most recent events, with user and attendees loaded.
    """
    with get_session() as session:
        return (
            session.query(Event)
            .options(
                joinedload(Event.user),
                selectinload(Event.attendees)
            )
            .order_by(Event.event_datetime.desc())
            .limit(limit)
            .all()
        )


def find_event_by_slug(event_slug: str) -> Optional[Event]:
    """
    Finds a single event by its slug and loads all relationships eagerly.
    """
    with get_session() as session:
        return (
            session.query(Event)
            .options(
                joinedload(Event.user),
                selectinload(Event.attendees)
            )
            .filter(Event.event_slug == event_slug)
            .first()
        )


def create_event(eventname: str, location: str, event_datetime, description: str, user_id: int) -> Optional[Event]:
    """
    Creates a new event and returns it (already stored in DB).
    """
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
