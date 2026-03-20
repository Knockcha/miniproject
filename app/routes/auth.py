from flask import Blueprint, request, session, redirect, url_for, flash, current_app, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
import requests
import secrets

auth_bp = Blueprint('auth', __name__)

# --- [백엔드 담당 구역] 소셜 로그인 설정 ---
NAVER_AUTH_URL = "https://nid.naver.com/oauth2.0/authorize"
NAVER_TOKEN_URL = "https://nid.naver.com/oauth2.0/token"
NAVER_USERINFO_URL = "https://openapi.naver.com/v1/nid/me"

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mbr_name, mbr_pwd = request.form.get("username"), request.form.get("password")
        engine = current_app.extensions["db_engine"]
        with engine.begin() as conn:
            user = conn.execute(text("SELECT mbr_id, mbr_name, mbr_pwd, mbr_email FROM tb_cs_members WHERE mbr_name = :name"), {"name": mbr_name}).fetchone()
            if user and check_password_hash(user[2], mbr_pwd):
                session.update({"user_id": user[0], "username": user[1], "user_email": user[3]})
                return redirect(url_for("main.index"))
            flash("아이디 또는 비밀번호가 틀렸습니다.", "error")
    return render_template("login.html")

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # (회원가입 로직 구현...)
        pass
    return render_template("signup.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))

# (네이버/구글/카카오 콜백 라우트들 이리로 이동...)
