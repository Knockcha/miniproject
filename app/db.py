from flask import Flask
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


def init_db(app: Flask) -> None:
    engine = create_engine(
        app.config["SQLALCHEMY_DATABASE_URI"],
        pool_pre_ping=True,
        future=True,
    )
    app.extensions["db_engine"] = engine
    
    # [개선] 기존 sample_items, diagnosis_results 자동 생성 제거
    # → Supabase에 DB 담당자가 만든 tb_sk_diagnosis 테이블 사용
    uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    is_postgres = "postgres" in uri.lower()

    # DB 연결 확인
    try:
        with engine.begin() as conn:
            conn.execute(text("SELECT 1"))
            print("[DB] 연결 확인 완료 (Supabase)" if is_postgres else "[DB] 연결 확인 완료 (MySQL)")
    except SQLAlchemyError as e:
        print(f"[DB Error] 연결 실패: {e}")

    @app.get("/health")
    def healthcheck():
        try:
            with app.extensions["db_engine"].connect() as connection:
                connection.execute(text("SELECT 1"))
            return {"status": "ok", "database": "connected"}, 200
        except SQLAlchemyError:
            return {"status": "degraded", "database": "disconnected"}, 503
