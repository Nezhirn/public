# bot.py
import uuid
import os
import redis.asyncio as redis
from redis_client import r_links
from datetime import datetime

# Файл и Tailscale Funnel URL
FUNNEL_URL = ""


async def generate_token(final_file):
    if not os.path.exists(final_file):
        print("Файл не найден.")
        return

    token = str(uuid.uuid4())
    key = f"link:{token}"
    date = str(datetime.now())

    await r_links.hset(key, mapping={
        "path": final_file,
        "used": 'false',
        "created_at": date
    })
    await r_links.expire(key, 60 * 15)  # 15 минут TTL

    link = f"{FUNNEL_URL}/download/{token}"
    return link




