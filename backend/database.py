# database.py
# DB에 "어떻게 연결할지"만 담당하는 파일이에요.
# 지금은 SQLite(파일 하나짜리 DB)를 쓰고, 나중에 실전 배포할 땐
# 이 파일의 DATABASE_URL 한 줄만 PostgreSQL 주소로 바꾸면 됩니다.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ikki.db 라는 파일이 프로젝트 폴더에 자동으로 생성돼요.
DATABASE_URL = "sqlite:///./ikki.db"

# SQLite는 기본적으로 하나의 스레드에서만 접근 가능하다고 가정하는데,
# FastAPI는 여러 요청을 동시에 처리할 수 있어서 이 옵션이 필요해요.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# DB와 대화할 때 쓰는 "세션"을 만들어주는 팩토리예요.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 아래에서 만들 모델(테이블)들이 상속받을 기본 클래스예요.
Base = declarative_base()


# API가 요청 하나를 처리할 때마다 DB 세션을 열고,
# 끝나면 자동으로 닫아주는 함수예요. FastAPI의 Depends()에서 사용됩니다.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
