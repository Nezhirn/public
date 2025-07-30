import redis.asyncio as redis

from config import r_url, r_port, r_pass


r_links = redis.Redis(host=r_url, port=r_port, db=0, password=r_pass, decode_responses=True)

r_prem = redis.Redis(host=r_url, port=r_port, db=2, password=r_pass, decode_responses=True)

