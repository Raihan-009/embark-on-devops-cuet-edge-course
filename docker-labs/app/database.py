import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get MySQL host from environment variable
MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql-container')
MYSQL_URL = f"mysql+pymysql://myuser:mypassword@{MYSQL_HOST}:3306/userdb"

print(f"Connecting to MySQL at: {MYSQL_URL}")

engine = create_engine(
    MYSQL_URL,
    pool_pre_ping=True,  # Add connection health check
    pool_recycle=3600    # Recycle connections after an hour
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()