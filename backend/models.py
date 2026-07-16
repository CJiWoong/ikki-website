# models.py
# 실제 DB "테이블"의 모양을 파이썬 클래스로 정의하는 파일이에요.
# 이 클래스 하나가 곧 테이블 하나가 됩니다.

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    # 서버(DB)가 알아서 현재 시각을 채워줘요. 프론트에서 안 보내도 됨.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
