from fastapi import HTTPException
import redis
from app.config import settings

# Create a Redis client instance
redis_client = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, decode_responses=True)


def add_emails_to_whitelist(email):
    redis_client.sadd("whitelisted_emails", email)


def check_whitelist_with_redis(email_to_check):
    """
    Checks if the given email is in the whitelist stored in Redis.

    :param email_to_check: The email address to check against the whitelist.
    :return: True if the email is whitelisted, False otherwise.
    """
    is_whitelisted = redis_client.sismember("whitelisted_emails", email_to_check)
    return is_whitelisted


def remove_email_from_whitelist(email):
    """
    Remove an email from the whitelist stored in Redis.

    :param email: The email address to be removed from the whitelist.
    """
    result = redis_client.srem("whitelisted_emails", email)
    if result == 1:
        print(f"Email {email} was removed from the whitelist.")
    else:
        print(f"Email {email} was not found in the whitelist.")


def get_whitelisted_emails():
    """
    Fetches all whitelisted emails from the Redis Set.

    :return: A set of all whitelisted emails.
    """
    return redis_client.smembers("whitelisted_emails")


def rate_limit(identifier: str, limit: int, period: int):
    """
    Simple rate limiter using Redis.

    :param identifier: Unique identifier for the user or IP.
    :param limit: Number of allowed requests in the period.
    :param period: Time window in seconds.
    """
    requests = redis_client.get(identifier)
    if requests and int(requests) >= limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    else:
        pipeline = redis_client.pipeline()
        pipeline.incr(identifier, 1)
        pipeline.expire(identifier, period)
        pipeline.execute()
