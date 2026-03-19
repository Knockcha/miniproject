"""피부 상태 분석 서비스

기본적인 이미지 분석(밝기·균일도·붉은기·피부결·수분도·유분)으로
피부 상태를 진단합니다.
외부 딥러닝 API 결과가 있으면 해당 결과를 우선 사용하고,
없을 때 로컬 분석으로 fallback 합니다.
"""

from io import BytesIO

import numpy as np
from PIL import Image, ImageFilter


class SkinAnalyzer:

    # ------------------------------------------------------------------ #
    #  공개 API                                                           #
    # ------------------------------------------------------------------ #
    def analyze(self, image_bytes: bytes) -> dict:
        """이미지를 분석하여 피부 상태 결과를 반환합니다."""
        try:
            img = Image.open(BytesIO(image_bytes)).convert("RGB")
            img = img.resize((300, 300))

            w, h = img.size
            skin_region = img.crop((
                int(w * 0.2), int(h * 0.15),
                int(w * 0.8), int(h * 0.75),
            ))
            pixels = np.array(skin_region).astype(float)

            # 1) 밝기
            brightness_raw = pixels.mean() / 255 * 100
            brightness_score = self._clamp(int(brightness_raw * 1.2))

            # 2) 균일도
            std_avg = pixels.std(axis=(0, 1)).mean()
            evenness_score = self._clamp(int(100 - std_avg * 1.5))

            # 3) 붉은기
            r, g, b = (pixels[:, :, i].mean() for i in range(3))
            redness_ratio = (r - (g + b) / 2) / 255 * 100
            redness_score = self._clamp(int(100 - redness_ratio * 3))

            # 4) 피부결 (에지 강도 기반)
            gray = skin_region.convert("L")
            edge_mean = np.array(gray.filter(ImageFilter.FIND_EDGES)).mean()
            texture_score = self._clamp(int(100 - edge_mean * 2))

            # 5) 수분도 추정
            moisture_score = self._clamp(int(
                evenness_score * 0.5
                + brightness_score * 0.3
                + texture_score * 0.2
            ))

            # 6) 유분 균형 추정
            highlight_ratio = (pixels > 200).mean() * 100
            oiliness_score = self._clamp(int(100 - highlight_ratio * 2))

            # 종합 점수
            overall_score = int(
                brightness_score * 0.15
                + evenness_score * 0.25
                + redness_score * 0.20
                + texture_score * 0.20
                + moisture_score * 0.10
                + oiliness_score * 0.10
            )

            conditions = {
                "brightness": self._build_item(
                    "피부 밝기", brightness_score, self._brightness_detail
                ),
                "evenness": self._build_item(
                    "피부 균일도", evenness_score, self._evenness_detail
                ),
                "redness": self._build_item(
                    "붉은기", redness_score, self._redness_detail
                ),
                "texture": self._build_item(
                    "피부결", texture_score, self._texture_detail
                ),
                "moisture": self._build_item(
                    "수분도", moisture_score, self._moisture_detail
                ),
                "oiliness": self._build_item(
                    "유분 균형", oiliness_score, self._oiliness_detail
                ),
            }

            skin_type = self._determine_skin_type(conditions)
            recommendations = self._generate_recommendations(conditions)

            return {
                "success": True,
                "overall_score": overall_score,
                "skin_type": skin_type,
                "conditions": conditions,
                "recommendations": recommendations,
                "analysis_method": "basic_image_analysis",
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"피부 상태 분석 중 오류가 발생했습니다: {e}",
            }

    # ------------------------------------------------------------------ #
    #  내부 헬퍼                                                          #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _clamp(v: int, lo: int = 0, hi: int = 100) -> int:
        return max(lo, min(hi, v))

    def _build_item(self, label, score, detail_fn):
        return {
            "label": label,
            "score": score,
            "status": self._status(score),
            "detail": detail_fn(score),
        }

    @staticmethod
    def _status(score):
        if score >= 80:
            return "excellent"
        if score >= 60:
            return "good"
        if score >= 40:
            return "average"
        return "needs_attention"

    # ── 상세 설명 ──────────────────────────────────────────────────── #
    @staticmethod
    def _brightness_detail(s):
        if s >= 70:
            return "피부가 전체적으로 밝고 화사한 상태입니다. 현재 스킨케어를 잘 유지하고 계세요."
        if s >= 50:
            return "피부 밝기가 보통 수준입니다. 비타민C 세럼이나 나이아신아마이드 제품으로 톤업 관리를 추천합니다."
        return "피부 톤이 다소 어두운 편입니다. 자외선 차단과 미백 기능성 제품 사용을 고려해보세요."

    @staticmethod
    def _evenness_detail(s):
        if s >= 70:
            return "피부톤이 균일하고 고르게 유지되고 있습니다."
        if s >= 50:
            return "부분적으로 색소 침착이나 톤 차이가 관찰됩니다. 꾸준한 각질 관리가 도움이 됩니다."
        return "피부톤의 편차가 큰 편입니다. 색소 침착 개선을 위한 전문 관리를 권장합니다."

    @staticmethod
    def _redness_detail(s):
        if s >= 70:
            return "붉은기가 적정 수준으로 건강한 혈색을 보이고 있습니다."
        if s >= 50:
            return "약간의 붉은기가 감지됩니다. 진정 효과가 있는 시카(CICA) 제품이 도움이 될 수 있습니다."
        return "붉은기가 다소 강한 편입니다. 민감성 피부 전용 제품과 진정 케어를 추천합니다."

    @staticmethod
    def _texture_detail(s):
        if s >= 70:
            return "피부결이 매끄럽고 건강한 상태입니다."
        if s >= 50:
            return "약간의 피부결 불균형이 있습니다. 부드러운 각질 제거와 보습 관리를 추천합니다."
        return "피부결이 거친 편입니다. AHA/BHA 제품으로 부드러운 각질 관리를 시작해보세요."

    @staticmethod
    def _moisture_detail(s):
        if s >= 70:
            return "피부 수분 상태가 양호합니다. 보습 관리를 잘 하고 계시네요."
        if s >= 50:
            return "수분감이 보통 수준입니다. 히알루론산이 함유된 보습제로 수분을 보충해주세요."
        return "피부가 건조한 상태로 보입니다. 속보습 제품과 수분크림으로 집중 보습을 추천합니다."

    @staticmethod
    def _oiliness_detail(s):
        if s >= 70:
            return "유수분 밸런스가 잘 유지되고 있습니다."
        if s >= 50:
            return "약간의 유분기가 감지됩니다. 가벼운 수분 제품으로 밸런스를 맞춰주세요."
        return "유분기가 많은 편입니다. 논코메도제닉 제품과 가벼운 수분 케어를 추천합니다."

    # ── 피부 타입 판별 ─────────────────────────────────────────────── #
    @staticmethod
    def _determine_skin_type(cond):
        moisture = cond["moisture"]["score"]
        oiliness = cond["oiliness"]["score"]
        redness = cond["redness"]["score"]

        if redness < 50:
            return {"name": "민감성 피부", "emoji": "🌿",
                    "description": "외부 자극에 민감하게 반응하는 피부 타입입니다."}
        if oiliness < 50:
            return {"name": "지성 피부", "emoji": "💧",
                    "description": "피지 분비가 활발한 피부 타입입니다."}
        if moisture < 50:
            return {"name": "건성 피부", "emoji": "🏜️",
                    "description": "수분이 부족하여 건조해지기 쉬운 피부 타입입니다."}
        if oiliness < 65 and moisture < 65:
            return {"name": "복합성 피부", "emoji": "⚖️",
                    "description": "T존은 유분기가 많고 U존은 건조한 피부 타입입니다."}
        return {"name": "중성 피부", "emoji": "✨",
                "description": "유수분 밸런스가 잘 잡혀 있는 건강한 피부 타입입니다."}

    # ── 스킨케어 추천 ──────────────────────────────────────────────── #
    @staticmethod
    def _generate_recommendations(cond):
        recs = []

        if cond["moisture"]["score"] < 60:
            recs.append({
                "category": "보습", "icon": "💧",
                "tip": "히알루론산, 세라마이드 성분의 보습 제품을 아침저녁으로 사용해주세요.",
            })
        if cond["redness"]["score"] < 60:
            recs.append({
                "category": "진정", "icon": "🌿",
                "tip": "시카(CICA), 판테놀 성분의 진정 제품으로 피부 장벽을 강화해주세요.",
            })
        if cond["brightness"]["score"] < 60:
            recs.append({
                "category": "톤업", "icon": "✨",
                "tip": "비타민C 세럼과 자외선 차단제를 꾸준히 사용하면 피부톤 개선에 도움이 됩니다.",
            })
        if cond["texture"]["score"] < 60:
            recs.append({
                "category": "각질 관리", "icon": "🧴",
                "tip": "주 1-2회 부드러운 AHA/BHA 각질 제거제를 사용해 피부결을 개선해보세요.",
            })
        if cond["oiliness"]["score"] < 60:
            recs.append({
                "category": "유분 조절", "icon": "🍃",
                "tip": "논코메도제닉 제품을 선택하고, 클레이 마스크로 주기적 모공 관리를 해주세요.",
            })

        if not recs:
            recs.append({
                "category": "유지 관리", "icon": "💎",
                "tip": "현재 피부 상태가 좋습니다! 기존 스킨케어 루틴을 꾸준히 유지해주세요.",
            })

        recs.append({
            "category": "자외선 차단", "icon": "☀️",
            "tip": "SPF 50+ PA++++ 자외선 차단제를 매일 사용하는 것이 모든 피부 관리의 기본입니다.",
        })
        return recs
