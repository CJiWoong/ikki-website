# ikki backend (공부용)

문의 폼 데이터를 SQLite DB에 저장하는 아주 작은 FastAPI 서버입니다.

## 실행 방법

```bash
# 1. 이 폴더로 이동
cd backend

# 2. 가상환경 생성 (한 번만)
python -m venv venv

# 3. 가상환경 켜기
source venv/bin/activate      # 맥/리눅스
venv\Scripts\activate         # 윈도우

# 4. 패키지 설치
pip install -r requirements.txt

# 5. 서버 실행
uvicorn main:app --reload
```

서버가 켜지면:
- http://127.0.0.1:8000 → 살아있는지 확인
- http://127.0.0.1:8000/docs → 자동 생성된 API 문서 (여기서 직접 테스트 가능)

## 확인해볼 것

1. `/docs` 페이지에서 `POST /api/contact`를 열고 "Try it out" → 아무 값이나 넣고 Execute
2. 같은 폴더에 `ikki.db` 파일이 생긴 걸 확인 (이게 SQLite DB 파일)
3. `GET /api/contact`로 방금 넣은 데이터가 저장됐는지 확인

## 프론트엔드와 연결

`index.html`을 그냥 더블클릭해서 열면 `file://` 주소라서 CORS 때문에 요청이 막힐 수 있어요.
VSCode의 "Live Server" 확장 프로그램으로 열거나, 아래처럼 간단히 로컬 서버로 띄워서 테스트하세요.

```bash
# index.html이 있는 폴더에서
python -m http.server 5500
```

그 다음 브라우저로 http://127.0.0.1:5500 접속해서 문의 폼을 테스트해보면 됩니다.
