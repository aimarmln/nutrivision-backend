from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session, MappedAsDataclass, DeclarativeBase
from app.config import Config

# Base class for all models
class Base(MappedAsDataclass, DeclarativeBase):
    pass

# Create engine
engine = create_engine(
    Config.DATABASE_URL,
    echo=False
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


# Scoped session: 1 session per request
db_session = scoped_session(SessionLocal)