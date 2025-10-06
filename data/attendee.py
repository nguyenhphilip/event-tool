
import sqlalchemy as sa
import sqlalchemy.orm as orm
from data.modelbase import SqlAlchemyBase

class Attendee(SqlAlchemyBase):
    __tablename__ = 'attendees'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, nullable=False)
    event_id = sa.Column(sa.Integer, sa.ForeignKey("events.id"), nullable=False)
    event = orm.relationship("Event", back_populates="attendees")