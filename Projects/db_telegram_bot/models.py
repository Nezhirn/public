from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, BigInteger, Text, INT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import uuid

from datetime import datetime
from dateutil.relativedelta import relativedelta



Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Text, unique=True, index=True)
    nickname = Column(String, unique=False, index=True, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now())
    is_admin = Column(Boolean, default=False)

class VPNLink(Base):
    __tablename__ = "vpn_links"

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    local_user_id = Column(Text, ForeignKey("users.user_id"), index=True)
    nickname = Column(String, unique=False, index=True, nullable=True)
    is_active = Column(Boolean, default=False)
    link = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now())
    expire_on = Column(DateTime, default=lambda: datetime.now() + relativedelta(months=1), nullable=True)
