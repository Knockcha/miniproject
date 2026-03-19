"""퍼스널컬러 분석 서비스

이미지에서 피부 톤을 추출하고 퍼스널컬러 시즌(봄/여름/가을/겨울)을 분류합니다.
기본적인 색상 분석을 제공하며, 추후 딥러닝 모델로 교체·보강할 수 있습니다.
"""

from io import BytesIO

import numpy as np
from PIL import Image


class PersonalColorAnalyzer:

    SEASONS = {
        "spring_warm": {
            "name": "봄 웜톤",
            "emoji": "🌸",
            "subtitle": "밝고 화사한 봄의 따뜻함",
            "description": (
                "따뜻하고 밝은 톤이 특징인 봄 웜톤은 "
                "살구색, 코랄, 아이보리처럼 부드럽고 화사한 색상이 잘 어울립니다. "
                "피부가 맑고 투명한 느낌을 줄 때 가장 빛나는 타입입니다."
            ),
            "best_colors": [
                "코랄 핑크", "살구색", "아이보리",
                "워밍 골드", "라이트 오렌지", "피치",
            ],
            "worst_colors": ["블랙", "다크 네이비", "차가운 회색", "버건디"],
            "worst_color_codes": ["#1a1a1a", "#1b2540", "#8e9aaf", "#800020"],
            "color_codes": [
                "#FF7F7F", "#FFDAB9", "#FFFFF0",
                "#FFD700", "#FFA07A", "#FFCBA4",
            ],
            "makeup_tip": (
                "코랄, 피치 계열의 블러셔와 립을 활용하면 "
                "혈색 있고 생기 넘치는 메이크업이 완성됩니다."
            ),
            "fashion_tip": (
                "밝은 베이지, 크림색 등 따뜻한 라이트 톤의 의상이 "
                "얼굴을 환하게 밝혀줍니다."
            ),
        },
        "summer_cool": {
            "name": "여름 쿨톤",
            "emoji": "🌊",
            "subtitle": "부드럽고 우아한 여름의 시원함",
            "description": (
                "차갑고 부드러운 톤이 특징인 여름 쿨톤은 "
                "라벤더, 로즈핑크, 스카이블루처럼 쿨하면서도 경쾌한 색상이 잘 어울립니다. "
                "은은하고 우아한 분위기를 연출할 때 가장 매력적인 타입입니다."
            ),
            "best_colors": [
                "라벤더", "로즈 핑크", "스카이 블루",
                "소프트 화이트", "라일락", "베이비 핑크",
            ],
            "worst_colors": ["오렌지", "머스타드", "카키", "다크 브라운"],
            "worst_color_codes": ["#FF8C00", "#E1AD01", "#6B6B3D", "#3E2723"],
            "color_codes": [
                "#B57EDC", "#FF007F", "#87CEEB",
                "#F5F5F5", "#C8A2C8", "#FFB6C1",
            ],
            "makeup_tip": (
                "로즈, 핑크 계열의 립과 블러셔로 "
                "자연스럽고 우아한 메이크업을 연출해보세요."
            ),
            "fashion_tip": (
                "파스텔 톤의 블루, 핑크, 라벤더 의상이 "
                "피부를 맑고 깨끗하게 보이게 합니다."
            ),
        },
        "autumn_warm": {
            "name": "가을 웜톤",
            "emoji": "🍂",
            "subtitle": "깊고 풍성한 가을의 따뜻함",
            "description": (
                "따뜻하고 깊은 톤이 특징인 가을 웜톤은 "
                "테라코타, 올리브, 머스타드처럼 자연에서 온 풍성한 색상이 잘 어울립니다. "
                "고급스럽고 세련된 분위기를 연출할 때 가장 돋보이는 타입입니다."
            ),
            "best_colors": [
                "테라코타", "올리브 그린", "머스타드",
                "버건디", "카멜", "브라운",
            ],
            "worst_colors": ["파스텔 핑크", "네온 컬러", "차가운 회색", "로얄 블루"],
            "worst_color_codes": ["#FFB6C1", "#39FF14", "#8e9aaf", "#4169E1"],
            "color_codes": [
                "#CC4E3C", "#808000", "#FFDB58",
                "#800020", "#C19A6B", "#8B4513",
            ],
            "makeup_tip": (
                "브라운, 테라코타 계열의 아이섀도우와 브릭 레드 립으로 "
                "깊이감 있는 메이크업을 완성하세요."
            ),
            "fashion_tip": (
                "카키, 올리브, 브라운 등 어스 톤 의상이 "
                "고급스럽고 세련된 분위기를 연출합니다."
            ),
        },
        "winter_cool": {
            "name": "겨울 쿨톤",
            "emoji": "❄️",
            "subtitle": "선명하고 강렬한 겨울의 시원함",
            "description": (
                "차갑고 선명한 톤이 특징인 겨울 쿨톤은 "
                "블랙, 화이트, 레드, 로얄 블루처럼 강렬하고 대비가 뚜렷한 색상이 잘 어울립니다. "
                "시크하고 모던한 분위기를 연출할 때 가장 매력적인 타입입니다."
            ),
            "best_colors": [
                "퓨어 화이트", "블랙", "로얄 블루",
                "와인 레드", "에메랄드", "핫 핑크",
            ],
            "worst_colors": ["베이지", "살구색", "카키", "머스타드"],
            "worst_color_codes": ["#D2B48C", "#FFDAB9", "#6B6B3D", "#E1AD01"],
            "color_codes": [
                "#FFFFFF", "#000000", "#4169E1",
                "#722F37", "#50C878", "#FF69B4",
            ],
            "makeup_tip": (
                "레드, 와인 계열의 립과 블랙 아이라인으로 "
                "시크하고 강렬한 메이크업이 잘 어울립니다."
            ),
            "fashion_tip": (
                "블랙 & 화이트 대비, 선명한 컬러의 의상이 "
                "세련되고 모던한 이미지를 만들어줍니다."
            ),
        },
    }

    # ------------------------------------------------------------------ #
    #  공개 API                                                           #
    # ------------------------------------------------------------------ #
    def analyze(self, image_bytes: bytes) -> dict:
        """이미지를 분석하여 퍼스널컬러 결과를 반환합니다."""
        try:
            img = Image.open(BytesIO(image_bytes)).convert("RGB")
            img = img.resize((300, 300))

            # 중앙 영역 크롭 (피부 영역 근사)
            w, h = img.size
            skin_region = img.crop((
                int(w * 0.2), int(h * 0.15),
                int(w * 0.8), int(h * 0.75),
            ))

            pixels = np.array(skin_region).reshape(-1, 3).astype(float)

            # 극단적으로 어둡거나 밝은 픽셀 제외
            brightness = pixels.mean(axis=1)
            mask = (brightness > 40) & (brightness < 240)
            skin_pixels = pixels[mask] if mask.sum() > 100 else pixels

            avg_r, avg_g, avg_b = skin_pixels.mean(axis=0)

            # ── 언더톤 판별 (Warm vs Cool) ──
            warmth = (avg_r * 0.6 + avg_g * 0.3) - (avg_b * 0.8 + avg_g * 0.1)
            is_warm = warmth > 15

            # ── 명도 판별 (Light vs Deep) ──
            lightness = (avg_r + avg_g + avg_b) / 3
            is_light = lightness > 140

            # ── 채도 판별 (Bright vs Muted) ──
            max_c = max(avg_r, avg_g, avg_b)
            min_c = min(avg_r, avg_g, avg_b)
            saturation = (max_c - min_c) / max_c if max_c > 0 else 0
            is_bright = saturation > 0.15

            # ── 시즌 분류 ──
            if is_warm and is_light:
                season_key = "spring_warm"
            elif not is_warm and is_light:
                season_key = "summer_cool"
            elif is_warm and not is_light:
                season_key = "autumn_warm"
            else:
                season_key = "winter_cool"

            season = self.SEASONS[season_key]

            # ── 판단 근거 ──
            undertone_text = "따뜻한 (웜)" if is_warm else "차가운 (쿨)"
            depth_text = "밝은 (라이트)" if is_light else "깊은 (딥)"
            clarity_text = "선명한 (브라이트)" if is_bright else "부드러운 (뮤트)"

            reasoning = [
                {
                    "factor": "언더톤",
                    "value": undertone_text,
                    "detail": (
                        "피부의 붉은기와 푸른기 비율을 분석한 결과, "
                        + ("따뜻한 황색 기반의 언더톤" if is_warm
                           else "차가운 청색 기반의 언더톤")
                        + "이 감지되었습니다."
                    ),
                },
                {
                    "factor": "명도",
                    "value": depth_text,
                    "detail": (
                        "피부의 전체적인 밝기를 측정한 결과, "
                        + ("밝고 환한 톤" if is_light else "깊고 차분한 톤")
                        + "으로 분류되었습니다."
                    ),
                },
                {
                    "factor": "채도",
                    "value": clarity_text,
                    "detail": (
                        "피부 색상의 선명도를 분석한 결과, "
                        + ("또렷하고 맑은 느낌" if is_bright
                           else "부드럽고 은은한 느낌")
                        + "의 피부톤입니다."
                    ),
                },
            ]

            return {
                "success": True,
                "season_key": season_key,
                "season": season["name"],
                "emoji": season["emoji"],
                "subtitle": season["subtitle"],
                "description": season["description"],
                "best_colors": season["best_colors"],
                "worst_colors": season["worst_colors"],
                "color_codes": season["color_codes"],
                "worst_color_codes": season["worst_color_codes"],
                "makeup_tip": season["makeup_tip"],
                "fashion_tip": season["fashion_tip"],
                "reasoning": reasoning,
                "skin_tone_rgb": [int(avg_r), int(avg_g), int(avg_b)],
                "analysis_method": "basic_color_analysis",
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"퍼스널컬러 분석 중 오류가 발생했습니다: {e}",
            }
