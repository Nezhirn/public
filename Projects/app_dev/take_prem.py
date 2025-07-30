from redis_client import r_prem
import asyncio

# Бессрочный премиум
async def grant_premium(user_id: int):
    await r_prem.set(f"premium:{user_id}", 1)

user_id = ''
# Временный премиум
async def grant_premium_timed(user_id):
    #date = str(datetime.now() + relativedelta(months=1))
    #expires_at = str(date)
    #await r_prem.set(f"premium_expires:{user_id}", expires_at)
    await r_prem.setex(f"premium:{user_id}", 30 * 24 * 60 * 60, 1)

asyncio.run(grant_premium_timed(user_id))