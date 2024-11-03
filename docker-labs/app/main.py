import os
import time
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from redis import Redis
import json
from . import models, database
from pydantic import BaseModel

app = FastAPI()

# Get Redis host from environment variable
REDIS_HOST = os.getenv('REDIS_HOST', 'redis-container')
print(f"Connecting to Redis at: {REDIS_HOST}")

# Initialize Redis with retry logic
def get_redis():
    retries = 5
    while retries > 0:
        try:
            redis_client = Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)
            redis_client.ping()  # Test the connection
            print("Successfully connected to Redis")
            return redis_client
        except Exception as e:
            print(f"Redis connection failed: {str(e)}")
            retries -= 1
            if retries == 0:
                raise HTTPException(status_code=500, detail="Redis connection failed")
            time.sleep(5)

redis_client = get_redis()

# Initialize database with retry logic
@app.on_event("startup")
async def startup():
    retries = 5
    while retries > 0:
        try:
            # Test database connection
            database.engine.connect()
            # Create tables
            models.Base.metadata.create_all(bind=database.engine)
            print("Successfully connected to MySQL and created tables")
            break
        except Exception as e:
            print(f"Database connection failed: {str(e)}")
            retries -= 1
            if retries == 0:
                raise Exception("Failed to connect to database")
            time.sleep(5)

class UserCreate(BaseModel):
    name: str
    address: str
    occupation: str

class UserResponse(BaseModel):
    id: int
    name: str
    address: str
    occupation: str

    class Config:
        from_attributes = True

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(database.get_db)):
    try:
        # Create user in database
        db_user = models.User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/", response_model=list[UserResponse])
def get_users(db: Session = Depends(database.get_db)):
    try:
        # Try to get from Redis first
        cached_users = redis_client.get('all_users')
        
        if cached_users:
            print("Fetching from Redis cache")
            return json.loads(cached_users)
        
        # If not in Redis, get from database
        print("Fetching from Database")
        users = db.query(models.User).all()
        users_data = [
            {
                "id": user.id,
                "name": user.name,
                "address": user.address,
                "occupation": user.occupation
            }
            for user in users
        ]
        
        # Store in Redis with 1 hour expiration
        redis_client.setex('all_users', 3600, json.dumps(users_data))
        
        return users_data
    except Exception as e:
        print(f"Error getting users: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))