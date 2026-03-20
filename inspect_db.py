from sqlalchemy import text
from app import create_app

def check_columns(table_name):
    app = create_app()
    with app.extensions['db_engine'].connect() as conn:
        # 컬럼 이름과 데이터 타입 조회
        res = conn.execute(text(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'"))
        cols = {r[0]: r[1] for r in res}
        print(f"COLUMNS_{table_name.upper()}:{cols}")

if __name__ == "__main__":
    check_columns('tb_cs_members')
