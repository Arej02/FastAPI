from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1) Database URL: tells SQLAlchemy where the database is (here: a local SQLite file)
SQLALCHEMY_ADDRESS="sqlite:///./test.db"

# 2) Engine: the connection manager (it knows how to talk to the DB and manages connections)
engine=create_engine(SQLALCHEMY_ADDRESS,connect_args={"check_same_thread": False})

# 3) Session factory: a "session maker" (creates a new Session when you call it)
# You use a Session to run queries and to commit/rollback changes.
session=sessionmaker(engine,autoflush=False,autocommit=False)

# 4) Base class for ORM models: your table classes will inherit from Base
Base=declarative_base()

## For MYSQL

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/mydb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()