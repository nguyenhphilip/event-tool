import sqlalchemy as sa
import sqlalchemy.orm as orm
from data.modelbase import SqlAlchemyBase
from sqlalchemy.orm import Session


__factory = None


def global_init(db_file: str):
    global __factory

    if __factory:
        return
    
    if not db_file or not db_file.strip():
        raise Exception("You must specify a db file.")

    conn_str = 'sqlite:///' + db_file.strip()
    print(f"Connecting to DB with: {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    # create models db knows about from classes, e.g. Events
    import data.__all_models
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory

    session: Session = __factory()
    session.expire_on_commit = False

    return session