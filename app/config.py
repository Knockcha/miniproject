import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"

    DB_HOST = os.getenv("DB_HOST", "db")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_NAME = os.getenv("DB_NAME", "app_db")
    DB_USER = os.getenv("DB_USER", "app_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "app_password")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # ── 외부 딥러닝 피부 분석 API (팀원 모델) ──
    SKIN_API_URL = os.getenv("SKIN_API_URL", "")
    SKIN_API_KEY = os.getenv("SKIN_API_KEY", "")
    SKIN_API_TIMEOUT = int(os.getenv("SKIN_API_TIMEOUT", "30"))

    # ── 네이버 쇼핑 API (실제 제품 추천) ──
    NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", "")
    NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "")

    # ── 업로드 설정 ──
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
