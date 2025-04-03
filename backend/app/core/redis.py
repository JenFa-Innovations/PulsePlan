from fastapi import HTTPException

def initialize_redis(redis_instance):
    """Initialize the global redis client."""
    global redis_client
    redis_client = redis_instance

def add_to_blacklist(username: str, duration: int = 3600):
    """Add a user to the blacklist for a specific duration."""
    if redis_client is None:
        raise HTTPException(status_code=500, detail="Redis client is not initialized")
    
    redis_client.setex(f"blacklist:{username}", duration, "blocked")

def is_blacklisted(username: str) -> bool:
    """Check if a user is blacklisted."""
    if redis_client is None:
        raise HTTPException(status_code=500, detail="Redis client is not initialized")
    
    return redis_client.exists(f"blacklist:{username}")

