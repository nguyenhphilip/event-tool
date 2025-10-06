import datetime
import sqlalchemy as sa
import sqlalchemy.orm as orm
from data.modelbase import SqlAlchemyBase


class Event(SqlAlchemyBase):

    # the name for the database that shows up in the sql database
    __tablename__ = 'events'

    # define the database schema in sqlaalchemy and the type of the column in python simultaneously
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
    # create admin object from Admin table
    user = orm.relationship("User", back_populates="events")
    attendees = orm.relationship("Attendee", back_populates="event", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Event: {self.id}>'