# schemas.py
# models.py가 "DB 안에서의 모양"이라면,
# schemas.py는 "API로 주고받을 때의 모양"이에요. 이 둘을 분리하는 게 관례입니다.
#
# 예를 들어 ContactCreate는 사용자가 "보낼 때" 필요한 필드만 있고,
# ContactOut은 "받을 때"(id, 생성시각 포함) 필드가 더 있어요.

from pydantic import BaseModel, EmailStr
from datetime import datetime


# 프론트엔드가 문의 폼을 보낼 때 이 형태여야 해요.
class ContactCreate(BaseModel):
    name: str
    email: EmailStr  # 이메일 형식이 아니면 FastAPI가 자동으로 400 에러를 내줘요.
    message: str


# 저장된 문의를 조회할 때(관리자용) 이 형태로 응답해요.
class ContactOut(BaseModel):
    id: int
    name: str
    email: str
    message: str
    created_at: datetime

    class Config:
        # SQLAlchemy 모델 객체를 그대로 Pydantic으로 변환할 수 있게 해주는 옵션이에요.
        from_attributes = True
