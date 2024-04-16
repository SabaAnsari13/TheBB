import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
db_name="db"

DATABASE_URL = f"postgresql://postgres:pOst31@host.docker.internal:5432/postgres"

<<<<<<< HEAD
=======
DATABASE_URL = f"postgresql://admin:sabzWork1305@host.docker.internal:5432/postgres"
>>>>>>> c21823793f5cfd68c5f86413599045b7659b47ea
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
