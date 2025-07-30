from sqlalchemy import text
from initdb import async_session
from models import User, VPNLink
from datetime import datetime
from bot import bot

async def request_db(request):
    async with async_session() as session:
        result = await session.execute(text(request))
        result = result.mappings().all()
        return result
    
async def load_users_db(user_id, user_nickname, db, link=None, is_active=False):
    async with async_session() as session:
        if db == 1:
            db_user = User(
                user_id=user_id,
                nickname=user_nickname
                )
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
        elif db == 2:
            db_link = VPNLink(
                local_user_id=user_id,
                nickname=user_nickname,
                link=link,
                is_active=is_active
                )
            session.add(db_link)
            await session.commit()
            await session.refresh(db_link)

async def get_user_info(message):
    user_nickname = message.from_user.username or 'Гость'
    user_id = str(message.from_user.id)
    user = {'user_id': user_id, 'user_nickname': user_nickname}
    return user

async def notify_upcoming():
    request = 'select local_user_id, expire_on, nickname, is_active from vpn_links'
    users = await request_db(request)
    for user in users:
        user_id = user['local_user_id']
        nickname = user['nickname']
        is_active = user['is_active']
        expire_on = user['expire_on']
        if not is_active:
            return
        today = datetime.now().date()
        due_date = expire_on.date()
        if (due_date - today).days == 2:
            await bot.send_message(user_id,
                             f"{nickname}, до продления аренды сервера осталось 2 дня ({due_date}).")
        elif (due_date - today).days == 1:
            await bot.send_message(user_id,
                             f"{nickname}, до продления аренды сервера остались сутки ({due_date}).")
