#from redis_client import redis_client
from datetime import datetime
from dateutil.relativedelta import relativedelta
from redis_client import r_prem

async def has_premium(user_id) -> bool:
    prem = await r_prem.exists(f"premium:{user_id}")
    return bool(prem)