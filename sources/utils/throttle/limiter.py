from fastapi import Depends, HTTPException, Request, Response
from fastapi_limiter.depends import RateLimiter


async def callback(request: Request, response: Response, pexpire: int):  # noqa
    raise HTTPException(status_code=429, detail="Too many requests")


def limit(times: int, seconds: int = 0, minutes: int = 0, hours: int = 0):
    return Depends(RateLimiter(
        times=times,
        seconds=seconds,
        minutes=minutes,
        hours=hours,
        callback=callback
    ))


__all__ = ["limit"]
