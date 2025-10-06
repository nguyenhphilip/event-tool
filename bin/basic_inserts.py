import os
import data.db_session as db_session
from data.event import Event

def main():
    init_db()
    while True:
        insert_event()


def init_db():
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    rel_file = os.path.join('db', 'events.sqlite')
    db_file = os.path.abspath(os.path.join(parent_dir, rel_file))

    db_session.global_init(db_file)
    

def insert_event():

    e = Event()

    e.id = input("Event name: ").strip().lower()
    e.event_datetime = input("Event date/time (YYYY-MM-DD 24:00): ")
    e.location = input("Location: ").strip().lower()
    e.desc = input("Event description: ")
    e.host_name = input("Host name(s): ")
    
    
    session = db_session.create_session()
    session.add(e)
    session.commit()


if __name__ == "__main__":
    main()