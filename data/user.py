import sqlalchemy as sa
import datetime
import sqlalchemy.orm as orm
from data.event import Event
from data.modelbase import SqlAlchemyBase

class User(SqlAlchemyBase):

    # the name for the database
    __tablename__ = 'user'

    # define the database schema in sqlaalchemy and the type of the column in python simultaneously
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, index=True, nullable=True)
    email = sa.Column(sa.String, nullable=False)
    hashed_password = sa.Column(sa.String, nullable=True, index=True)
    is_admin = sa.Column(sa.Boolean)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)

    # event relationships: each admin presumably has events that are associated with them
    events = orm.relationship("Event", order_by=[
        Event.event_datetime.desc(),
        Event.created_date.desc(),
        ], back_populates='user')

    def __repr__(self):
        return f'<User: {self.id}>'