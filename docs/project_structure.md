# 프로젝트 구조
```
backend-feed/
│
├── app/
│   ├── __init__.py                # 패키지 초기화 파일
│   ├── main.py                    # FastAPI 애플리케이션 시작 파일
│   │
│   ├── models/                    # 데이터베이스 모델
│   │
│   ├── routers/                   # 라우터
│   │
│   ├── services/                  # 비즈니스 로직
│   │
│   ├── database/                  # 데이터베이스 관련 코드
│   │   ├── init.py
│   │   └── db.py                  # 데이터베이스 연결 및 초기화
│   │
│   ├── schemas/                   # Pydantic 스키마 모델
│   │
│   └── utils/                     # 유틸리티 함수
│
├── tests/                         # 테스트 코드
│
├── requirements.txt               # 의존성 목록
└── README.md                      # 프로젝트 설명 파일
```