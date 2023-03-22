from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./backend.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# autocommit이 True이면 잘못저장했을때 문제가 발생할 수 있다. 항상 주의할 것 
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata =MetaData(naming_convention = naming_convention)


# depends를 사용하려면, depends안에 기능이 이미 있기떄문에 중복을 막고자 주석을 달았다. 
#@contextlib.contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()
