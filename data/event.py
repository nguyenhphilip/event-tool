import datetime
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy import event as sqla_event
import re
from data.modelbase import SqlAlchemyBase


class Event(SqlAlchemyBase):
    __tablename__ = 'events'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=False)
    event_slug = sa.Column(sa.String, nullable=False)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    event_datetime = sa.Column(sa.DateTime, nullable=False, index=True)
    location = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=True)
    fu_notes = sa.Column(sa.String, nullable=True)
    event_url = sa.Column(sa.String)
    host_name = sa.Column(sa.String, index=True)

    user_id = sa.Column(sa.Integer, sa.ForeignKey("user.id"))

    # relationships
    user = orm.relationship(
        "User",
        back_populates="events",
        lazy="joined"          # 👈 always eager-load user when querying Event
    )

    attendees = orm.relationship(
        "Attendee",
        back_populates="event",
        cascade="all, delete-orphan",
        lazy="selectin"        # 👈 loads attendees efficiently when accessed
    )

    def __repr__(self):
        return f'<Event: {self.id}>'
    

# --- SLUG GENERATION LOGIC ---
@sqla_event.listens_for(Event, "before_insert")
def generate_slug(mapper, connection, target):
    """Automatically generate a unique slug before inserting an event."""
    base_slug = target.title.lower().strip().replace("'", "")
    base_slug = re.sub(r"\s+", "-", base_slug)
    base_slug = re.sub(r"[^a-z0-9-]", "", base_slug)

    # Append event date
    if target.event_datetime:
        date_str = target.event_datetime.strftime("%Y-%m-%d")
        slug_candidate = f"{base_slug}-{date_str}"
    else:
        slug_candidate = base_slug

    # Ensure uniqueness by checking for conflicts in the DB
    existing_slugs = connection.execute(
        sa.text("SELECT event_slug FROM events WHERE event_slug LIKE :slug_prefix"),
        {"slug_prefix": f"{slug_candidate}%"},
    ).fetchall()

    existing_slugs = [row[0] for row in existing_slugs]
    if slug_candidate in existing_slugs:
        # Append a numeric suffix if needed
        counter = 1
        while f"{slug_candidate}-{counter}" in existing_slugs:
            counter += 1
        slug_candidate = f"{slug_candidate}-{counter}"

    target.event_slug = slug_candidate