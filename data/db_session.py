import os
import sqlalchemy as sa
import sqlalchemy.orm as orm
from data.modelbase import SqlAlchemyBase
from sqlalchemy.orm import Session
from contextlib import contextmanager

__factory = None


def global_init(db_file: str = None):
    """
    Initialize the database connection, creating all models if needed.
    Supports both SQLite (local) and PostgreSQL (Render) via DATABASE_URL.
    """
    global __factory
    if __factory:
        return

    db_url = os.getenv("DATABASE_URL")

    if db_url:
        # Ensure compatibility for SQLAlchemy connection string
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        conn_str = db_url
        print(f"Connecting to Postgres at {conn_str}")
    else:
        if not db_file or not db_file.strip():
            raise Exception("You must specify a db file or set DATABASE_URL.")
        conn_str = 'sqlite:///' + db_file.strip()
        print(f"Connecting to local SQLite at {conn_str}")

    engine = sa.create_engine(
        conn_str,
        echo=False,
        pool_size=5,
        max_overflow=2,
        pool_recycle=1800,
        pool_pre_ping=True
    )

    __factory = orm.sessionmaker(bind=engine)

    import data.__all_models  # make sure models are imported
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    if not __factory:
        raise Exception("You must call global_init() before using the DB.")
    session: Session = __factory()
    session.expire_on_commit = False
    return session


@contextmanager
def get_session():
    """
    Safely open, commit/rollback, and close sessions.
    Use like:
        with get_session() as session:
            session.query(...)
    """
    session = create_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()