import os
import sqlalchemy as sa
import sqlalchemy.orm as orm
from data.modelbase import SqlAlchemyBase
from sqlalchemy.orm import Session

__factory = None

def global_init(db_file: str = None):
    global __factory
    if __factory:
        return

    # Use DATABASE_URL (for Render PostgreSQL)
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        # Render sometimes gives a URL starting with "postgres://"
        # SQLAlchemy expects "postgresql://"
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        conn_str = db_url
        print(f"Connecting to Postgres at {conn_str}")
    else:
        # fallback to local SQLite for local testing
        if not db_file or not db_file.strip():
            raise Exception("You must specify a db file or set DATABASE_URL.")
        conn_str = 'sqlite:///' + db_file.strip()
        print(f"Connecting to local SQLite at {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    import data.__all_models
    SqlAlchemyBase.metadata.create_all(engine)

def create_session() -> Session:
    global __factory
    session: Session = __factory()
    session.expire_on_commit = False
    return session