from dotenv import load_dotenv

load_dotenv()  # .env를 Config import 전에 로드해야 환경변수가 반영됨

from app import create_app

app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])
