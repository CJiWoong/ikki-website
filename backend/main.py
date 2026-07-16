# main.py
# 실제로 "요청이 오면 뭘 할지"를 정의하는 파일이에요.
# 터미널에서 `uvicorn main:app --reload` 로 실행합니다.

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

# 서버가 켜질 때, models.py에 정의된 테이블이 DB에 없으면 자동으로 만들어줘요.
# (이미 있으면 아무 일도 안 일어남 - 안전합니다)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ikki API", description="ikki 웹사이트 백엔드 공부용 서버")


# --- CORS 설정 -----------------------------------------------------
# 브라우저는 기본적으로 "다른 주소(origin)"로 보내는 요청을 막아요.
# index.html은 GitHub Pages(예: https://cjiwoong.github.io) 에서 열리고,
# 이 서버는 다른 주소(로컬이면 localhost, 배포하면 render.com 등)에서 돌아가니
# 명시적으로 "이 주소들은 허용해줘"라고 등록해야 합니다.
origins = [
    "http://localhost",
    "http://localhost:5500",       # VSCode Live Server 등으로 index.html 열 때
    "http://127.0.0.1:5500",
    "https://cjiwoong.github.io",  # 실제 배포된 GitHub Pages 주소
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- 엔드포인트 -------------------------------------------------------

@app.get("/")
def root():
    # 서버가 살아있는지 확인용. 브라우저로 http://127.0.0.1:8000 접속하면 이게 뜸.
    return {"message": "ikki API가 잘 작동 중이에요."}


@app.post("/api/contact", response_model=schemas.ContactOut)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    """
    문의 폼 데이터를 받아서 DB에 저장해요.
    프론트엔드의 fetch(POST) 요청이 여기로 들어옵니다.
    """
    new_contact = models.Contact(
        name=contact.name,
        email=contact.email,
        message=contact.message,
    )
    db.add(new_contact)      # DB에 추가할 준비
    db.commit()               # 실제로 저장
    db.refresh(new_contact)   # DB가 채워준 id, created_at을 다시 읽어옴
    return new_contact


@app.get("/api/contact", response_model=List[schemas.ContactOut])
def list_contacts(db: Session = Depends(get_db)):
    """
    저장된 문의 목록을 최신순으로 보여줘요.
    지금은 누구나 볼 수 있는 상태라, 나중에 로그인 기능을 배우면
    관리자만 볼 수 있게 잠그는 걸 다음 단계로 해보면 좋아요.
    """
    contacts = db.query(models.Contact).order_by(models.Contact.id.desc()).all()
    return contacts


@app.get("/api/contact/{contact_id}", response_model=schemas.ContactOut)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="해당 문의를 찾을 수 없어요.")
    return contact
