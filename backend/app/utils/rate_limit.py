from collections import defaultdict
from time import time

from fastapi import HTTPException, Request, status


class SimpleRateLimiter:
    """Lightweight in-memory limiter for architecture baseline.

    Replace with Redis-backed limiter for multi-instance production.
    """

    def __init__(self, limit: int = 60, window_seconds: int = 60):
        self.limit = limit
        self.window_seconds = window_seconds
        self.store: dict[str, list[float]] = defaultdict(list)

    def check(self, key: str):
        now = time()
        window_start = now - self.window_seconds
        timestamps = [ts for ts in self.store[key] if ts >= window_start]

        if len(timestamps) >= self.limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later.",
            )

        timestamps.append(now)
        self.store[key] = timestamps


limiter = SimpleRateLimiter(limit=120, window_seconds=60)


def enforce_rate_limit(request: Request):
    client_host = request.client.host if request.client else "unknown"
    limiter.check(client_host)
