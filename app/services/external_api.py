"""팀원의 딥러닝 피부 분석 API 연동 클라이언트

.env 에 아래 변수를 설정하면 활성화됩니다.
  SKIN_API_URL=http://<팀원서버>:<포트>
  SKIN_API_KEY=<optional>
  SKIN_API_TIMEOUT=30

API가 설정되어 있지 않거나 연결에 실패하면 None을 반환하고,
호출부(diagnosis.py)에서 로컬 SkinAnalyzer로 fallback 합니다.

────────────────────────────────────────────
팀원과 합의가 필요한 API 응답 스펙 (예시):

POST  /analyze
Content-Type: multipart/form-data
  - image: 파일 바이너리

Response (200 OK):
{
    "success": true,
    "skin_type": "oily",
    "overall_score": 73,
    "conditions": {
        "acne":         { "score": 75, "label": "여드름" },
        "wrinkle":      { "score": 85, "label": "주름" },
        "pigmentation": { "score": 60, "label": "색소침착" },
        ...
    }
}
────────────────────────────────────────────
"""

import logging

import requests

logger = logging.getLogger(__name__)


class ExternalSkinAPI:

    def __init__(self, base_url: str, api_key: str = "", timeout: int = 30):
        self.base_url = base_url.rstrip("/") if base_url else ""
        self.api_key = api_key
        self.timeout = timeout

    # ------------------------------------------------------------------ #
    @property
    def is_available(self) -> bool:
        """외부 API 엔드포인트가 설정되어 있는지 확인"""
        return bool(self.base_url)

    # ------------------------------------------------------------------ #
    def analyze(self, image_bytes: bytes) -> dict | None:
        """외부 딥러닝 API 로 피부 분석을 요청합니다.

        Returns
        -------
        dict  : 분석 결과 (성공 시)
        None  : API 미설정, 연결 실패, 타임아웃 등 → 로컬 fallback 유도
        """
        if not self.is_available:
            logger.info("외부 피부 분석 API가 설정되지 않았습니다. 로컬 분석을 사용합니다.")
            return None

        try:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            files = {"image": ("photo.jpg", image_bytes, "image/jpeg")}

            resp = requests.post(
                f"{self.base_url}/analyze",
                files=files,
                headers=headers,
                timeout=self.timeout,
            )
            resp.raise_for_status()

            result = resp.json()
            if result.get("success"):
                logger.info("외부 API 분석 완료")
                result["analysis_method"] = "deep_learning_api"
                return result

            logger.warning("외부 API 분석 실패: %s", result.get("error", "unknown"))
            return None

        except requests.exceptions.ConnectionError:
            logger.warning("외부 API 연결 실패: %s", self.base_url)
            return None
        except requests.exceptions.Timeout:
            logger.warning("외부 API 타임아웃: %d초 초과", self.timeout)
            return None
        except Exception as e:
            logger.warning("외부 API 호출 중 오류: %s", e)
            return None
