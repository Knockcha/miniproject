"""네이버 쇼핑 검색 API 연동 서비스

.env 에 아래 변수를 설정하면 활성화됩니다.
  NAVER_CLIENT_ID=<앱 등록 후 발급>
  NAVER_CLIENT_SECRET=<앱 등록 후 발급>

네이버 개발자센터 → 앱 등록 → 검색 API 선택
https://developers.naver.com
"""

import logging
import re

import requests

logger = logging.getLogger(__name__)


class NaverShoppingAPI:

    BASE_URL = "https://openapi.naver.com/v1/search/shop.json"

    # 퍼스널컬러 시즌별 검색 키워드
    COLOR_KEYWORDS = {
        "spring_warm": [
            "봄웜톤 코랄 립스틱",
            "피치 블러셔 봄웜",
            "웜톤 아이섀도우 팔레트 코랄",
        ],
        "summer_cool": [
            "여름쿨톤 로즈 립스틱",
            "쿨톤 핑크 블러셔",
            "쿨톤 아이섀도우 팔레트 라벤더",
        ],
        "autumn_warm": [
            "가을웜톤 브릭 립스틱",
            "테라코타 블러셔 웜톤",
            "가을 브라운 아이섀도우 팔레트",
        ],
        "winter_cool": [
            "겨울쿨톤 레드 립스틱",
            "쿨톤 플럼 블러셔",
            "겨울쿨톤 버건디 아이섀도우",
        ],
    }

    # 피부 상태별 검색 키워드 (key, 검색어, 임계점수)
    SKIN_KEYWORDS = [
        ("moisture",   "히알루론산 보습 크림",      60),
        ("redness",    "시카 진정 크림 민감성",      60),
        ("brightness", "비타민C 세럼 브라이트닝",    60),
        ("texture",    "AHA BHA 필링 각질",         60),
        ("oiliness",   "지성피부 유분조절 토너",     60),
    ]

    # ------------------------------------------------------------------ #
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    @property
    def is_available(self) -> bool:
        return bool(self.client_id and self.client_secret)

    # ------------------------------------------------------------------ #
    #  저수준 검색                                                        #
    # ------------------------------------------------------------------ #
    def search(self, query: str, display: int = 4, sort: str = "sim") -> list[dict]:
        """네이버 쇼핑 검색 API 호출"""
        if not self.is_available:
            return []

        try:
            resp = requests.get(
                self.BASE_URL,
                params={"query": query, "display": display, "sort": sort},
                headers={
                    "X-Naver-Client-Id": self.client_id,
                    "X-Naver-Client-Secret": self.client_secret,
                },
                timeout=5,
            )
            resp.raise_for_status()

            items = []
            for item in resp.json().get("items", []):
                title = re.sub(r"</?b>", "", item.get("title", ""))
                items.append({
                    "title": title,
                    "link": item.get("link", ""),
                    "image": item.get("image", ""),
                    "price": item.get("lprice", "0"),
                    "brand": item.get("brand", ""),
                    "mall": item.get("mallName", ""),
                    "category": item.get("category3", ""),
                })
            return items

        except Exception as e:
            logger.warning("네이버 쇼핑 API 호출 실패: %s", e)
            return []

    # ------------------------------------------------------------------ #
    #  퍼스널컬러 화장품 검색                                              #
    # ------------------------------------------------------------------ #
    def search_color_products(self, season_key: str) -> list[dict]:
        """퍼스널컬러 시즌에 어울리는 화장품 검색"""
        keywords = self.COLOR_KEYWORDS.get(season_key, [])
        results = []
        for kw in keywords:
            results.extend(self.search(kw, display=2))
        return results

    # ------------------------------------------------------------------ #
    #  피부 상태 스킨케어 검색                                             #
    # ------------------------------------------------------------------ #
    def search_skin_products(self, conditions: dict) -> list[dict]:
        """피부 분석 결과에 맞는 스킨케어 제품 검색"""
        results = []
        for key, query, threshold in self.SKIN_KEYWORDS:
            cond = conditions.get(key, {})
            if cond.get("score", 100) < threshold:
                results.extend(self.search(query, display=2))

        # 모든 항목이 양호하면 베스트셀러 추천
        if not results:
            results = self.search("스킨케어 베스트셀러", display=4)

        return results
