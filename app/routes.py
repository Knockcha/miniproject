from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from .db import init_db # 실제로는 app.extensions['db_engine'] 사용

main_blueprint = Blueprint("main", __name__)

@main_blueprint.get("/")
def index():
    # 로그인 세션 확인
    if "user_id" not in session:
        return redirect(url_for("main.login"))
    return render_template("index.html")

@main_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mbr_name = request.form.get("username")
        mbr_pwd = request.form.get("password")
        
        from flask import current_app
        engine = current_app.extensions["db_engine"]
        
        with engine.connect() as conn:
            # 회원 정보 조회
            result = conn.execute(
                text("SELECT mbr_id, mbr_name, mbr_pwd FROM tb_cs_members WHERE mbr_name = :name"),
                {"name": mbr_name}
            ).fetchone()
            
            if result and check_password_hash(result[2], mbr_pwd):
                # 로그인 성공
                session["user_id"] = result[0]
                session["username"] = result[1]
                return redirect(url_for("main.index"))
            else:
                flash("아이디 또는 비밀번호가 일치하지 않습니다.", "error")
                
    return render_template("login.html")

@main_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        mbr_name = request.form.get("username")
        mbr_pwd = request.form.get("password")
        mbr_email = request.form.get("email")
        
        # 비밀번호 해싱
        hashed_pwd = generate_password_hash(mbr_pwd)
        
        from flask import current_app
        engine = current_app.extensions["db_engine"]
        
        try:
            with engine.begin() as conn:
                # 중복 체크
                existing = conn.execute(
                    text("SELECT 1 FROM tb_cs_members WHERE mbr_name = :name"),
                    {"name": mbr_name}
                ).fetchone()
                
                if existing:
                    flash("이미 존재하는 아이디입니다.", "error")
                else:
                    # 회원 가입 처리 (Postgres 전용 문법 사용)
                    conn.execute(
                        text("""
                            INSERT INTO tb_cs_members (mbr_name, mbr_pwd, mbr_email, mbr_status)
                            VALUES (:name, :pwd, :email, 'active')
                        """),
                        {"name": mbr_name, "pwd": hashed_pwd, "email": mbr_email}
                    )
                    flash("회원가입이 완료되었습니다! 로그인해주세요.", "success")
                    return redirect(url_for("main.login"))
        except Exception as e:
            flash(f"가입 중 오류가 발생했습니다: {e}", "error")
            
    return render_template("signup.html")

@main_blueprint.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))
