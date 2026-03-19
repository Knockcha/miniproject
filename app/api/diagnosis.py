"""진단 API 엔드포인트

POST /api/diagnosis
  - multipart/form-data 로 image 필드에 사진 첨부
  - 퍼스널컬러 + 피부 상태 분석 + 실제 제품 추천을 JSON 으로 반환
  - 웹 프론트엔드 & 모바일 APK 앱 모두 이 API 를 사용
"""

import uuid

from flask import current_app, request
from sqlalchemy import text

from . import api_blueprint
from ..services.external_api import ExternalSkinAPI
from ..services.naver_shopping import NaverShoppingAPI
from ..services.personal_color import PersonalColorAnalyzer
from ..services.skin_analysis import SkinAnalyzer

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def _allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@api_blueprint.post("/diagnosis")
def run_diagnosis():
    """사진을 업로드하여 퍼스널컬러 + 피부 상태 진단 + 제품 추천"""

    # ── 입력 검증 ──
    if "image" not in request.files:
        return {"success": False, "error": "이미지가 첨부되지 않았습니다."}, 400

    file = request.files["image"]
    if file.filename == "":
        return {"success": False, "error": "파일이 선택되지 않았습니다."}, 400

    if not _allowed(file.filename):
        return {
            "success": False,
            "error": "지원하지 않는 파일 형식입니다. (PNG, JPG, JPEG, WebP 만 가능)",
        }, 400

    image_bytes = file.read()
    if not image_bytes:
        return {"success": False, "error": "빈 파일입니다."}, 400

    # ── 1. 퍼스널컬러 분석 ──
    color_result = PersonalColorAnalyzer().analyze(image_bytes)

    # ── 2. 피부 상태 분석 (외부 DL API 우선 → 로컬 fallback) ──
    ext_api = ExternalSkinAPI(
        base_url=current_app.config.get("SKIN_API_URL", ""),
        api_key=current_app.config.get("SKIN_API_KEY", ""),
        timeout=current_app.config.get("SKIN_API_TIMEOUT", 30),
    )
    skin_result = ext_api.analyze(image_bytes)

    if skin_result is None:
        skin_result = SkinAnalyzer().analyze(image_bytes)

    # ── 3. 네이버 쇼핑 API로 실제 제품 검색 ──
    naver = NaverShoppingAPI(
        client_id=current_app.config.get("NAVER_CLIENT_ID", ""),
        client_secret=current_app.config.get("NAVER_CLIENT_SECRET", ""),
    )

    color_products = []
    skin_products = []

    if naver.is_available:
        # 퍼스널컬러에 어울리는 화장품
        if color_result.get("success"):
            color_products = naver.search_color_products(
                color_result.get("season_key", "")
            )

        # 피부 상태에 맞는 스킨케어 제품
        if skin_result.get("success"):
            skin_products = naver.search_skin_products(
                skin_result.get("conditions", {})
            )

    # ── 4. 진단 결과 DB 저장 (실패해도 결과는 반환) ──
    session_id = str(uuid.uuid4())
    try:
        engine = current_app.extensions.get("db_engine")
        if engine:
            with engine.connect() as conn:
                conn.execute(
                    text(
                        "INSERT INTO diagnosis_results "
                        "(session_id, personal_color_season, skin_type, "
                        " overall_score, analysis_method) "
                        "VALUES (:sid, :season, :skin_type, :score, :method)"
                    ),
                    {
                        "sid": session_id,
                        "season": color_result.get("season_key", ""),
                        "skin_type": skin_result.get("skin_type", {}).get("name", ""),
                        "score": skin_result.get("overall_score", 0),
                        "method": skin_result.get("analysis_method", "unknown"),
                    },
                )
                conn.commit()
    except Exception:
        pass  # DB 저장 실패 시에도 분석 결과는 반환

    return {
        "success": True,
        "session_id": session_id,
        "personal_color": color_result,
        "skin_analysis": skin_result,
        "color_products": color_products,
        "skin_products": skin_products,
    }
