import json
from typing import Any, Optional

from redis.asyncio import Redis

from core import config


class RedisManager:
    redis_client = Redis.from_url(config.REDIS_URL, decode_responses=True)

    @classmethod
    def construct_key(cls, *args: str) -> str:
        return ":".join(args)

    @classmethod
    async def store_value(cls, key: str, value: Any, expiration: int = 300) -> bool:
        serialized_value = value if isinstance(value, str) else json.dumps(value)
        return await cls.redis_client.set(key, serialized_value, ex=expiration)

    @classmethod
    async def get_value(cls, key: str) -> Optional[Any]:
        value = await cls.redis_client.get(key)

        if not value:
            return None
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value

    @classmethod
    async def delete_value(cls, key: str) -> bool:
        return (await cls.redis_client.delete(key)) == 1
