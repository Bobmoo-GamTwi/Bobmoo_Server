import os
import json
import time  # 🚨 추가됨: 재시도 대기를 위해 필요해!
from google import genai
from dotenv import load_dotenv

class AiParser:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('AI_API_KEY')
        if not self.api_key:
            raise ValueError("🚨 AI_API_KEY가 .env 파일에 없습니다!")

        # 🚨 새로운 방식의 Client 초기화
        self.client = genai.Client(api_key=self.api_key)

    def parse_image_to_json(self, image_path: str, day_name: str) -> dict:
        print(f"🤖 최신 Gemini API(google-genai)로 파싱 요청 중... ({day_name})")

        prompt = """
        이 이미지는 대학교 기숙사 식단표 중 특정 요일의 메뉴를 자른 이미지입니다.
        이 이미지에서 식사 시간대별 메뉴를 추출하여, 반드시 아래 형태의 순수 JSON 포맷으로만 응답하세요.
        마크다운 코드 블록(```json 등)이나 부연 설명은 절대 금지합니다.

        {
          "date": "2026-MM-DD",
          "schools": [
            {
              "schoolName": "인하대학교",
              "cafeterias": [
                {
                  "name": "생활관식당",
                  "hours": {
                    "breakfast": "07:30-09:00",
                    "lunch": "11:30-13:30",
                    "dinner": "17:30-19:30"
                  },
                  "meals": {
                    "breakfast": [
                      { "course": "A", "mainMenu": "소시지 오므라이스", "price": 5800 }
                    ],
                    "lunch": [
                      { "course": "A", "mainMenu": "치킨마요 덮밥, 맑은국", "price": 5800 },
                      { "course": "B", "mainMenu": "토마토 리조또", "price": 5800 }
                    ],
                    "dinner": [
                        { "course": "A", "mainMenu": "순두부찌개와 제육", "price": 5800 },
                        { "course": "B", "mainMenu": "크림파스타", "price": 5800 }
                    ]
                  }
                }
              ]
            }
          ]
        }
        
        [데이터 정제 필수 규칙]
        1. 날짜(date): 이미지를 보고 해당 요일의 월, 일을 논리적으로 파악하여 작성하세요. 연도는 (2026)
        2. 메뉴(mainMenu): 메뉴가 여러 개일 경우 줄바꿈 대신 콤마(,)로 연결하세요.
        3. 코스(course): 같은 식사 시간(예: lunch)에 메뉴가 2개 이상 나뉘어 있다면, 위에서부터 "A", "B", "C" 순서로 증가시키며 객체를 여러 개 만드세요.
        4. 필터링(중요): '쌀밥', '잡곡밥', '추가밥', '배추김치', '깍두기', '단무지' 같이 단순한 기본 밥과 김치류는 mainMenu에서 제외하세요.
        5. 필터링 예외(중요): 단, '볶음밥', '덮밥', '비빔밥', '콩나물밥'처럼 밥 자체가 메인 요리인 경우는 절대 제외하지 말고 포함하세요.
        6. 빈 데이터: 해당 시간대가 '미운영'이거나 메뉴가 비어있으면 해당 meals 배열을 빈 배열([])로 남겨두세요.
        7. 가격: 기숙사 식당의 price는 5800원으로 고정하세요.
        8. 간편식은 메뉴에 포함시키지 마세요.
        9. 비빔코너 메뉴에 포함시키지 마세요.
        """

        max_retries = 3  # 🌟 최대 재시도 횟수

        for attempt in range(max_retries):
            image_file = None
            try:
                # 🚨 1. 파일 업로드
                image_file = self.client.files.upload(file=image_path)

                # 🚨 2. 모델 호출
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[image_file, prompt]
                )

                # 3. 마크다운이나 불필요한 공백 제거
                result_text = response.text.strip()
                if result_text.startswith("```json"):
                    result_text = result_text[7:]
                if result_text.endswith("```"):
                    result_text = result_text[:-3]

                result_text = result_text.strip()

                # 4. 순수 JSON 파싱
                parsed_data = json.loads(result_text)

                # 🚨 5. 파일 삭제
                self.client.files.delete(name=image_file.name)

                return parsed_data # 성공하면 즉시 함수 탈출!

            except json.JSONDecodeError as e:
                print(f"❌ AI가 JSON 형태로 대답하지 않았습니다 ({day_name}):\n원본응답: {result_text}\n에러: {e}")
                # 파일 찌꺼기 청소
                if image_file:
                    try: self.client.files.delete(name=image_file.name)
                    except: pass
                return {} # 형식이 깨진 건 재시도해도 답이 없을 확률이 높아서 바로 포기

            except Exception as e:
                error_msg = str(e)
                # 파일 찌꺼기 청소
                if image_file:
                    try: self.client.files.delete(name=image_file.name)
                    except: pass

                # 🌟 여기가 재시도 로직의 핵심이야! 503(서버 폭주)이나 429(속도 제한)일 때만 작동
                if "503" in error_msg or "UNAVAILABLE" in error_msg or "429" in error_msg:
                    print(f"⚠️ 구글 서버 혼잡 감지 ({attempt + 1}/{max_retries}번째 실패). 10초 후 다시 시도합니다...")
                    time.sleep(10)
                    continue # 다음 반복(재시도)으로 넘어감
                else:
                    # 다른 예상치 못한 에러면 그냥 포기
                    print(f"❌ Gemini 파싱 치명적 에러 ({day_name}): {e}")
                    return {}

        # 3번 다 실패했을 때 최후의 메시지
        print(f"❌ {max_retries}번 재시도했지만 구글 서버가 응답하지 않습니다. ({day_name})")
        return {}