# from crawler import DormCrawler
# from image_splitter import ImageSplitter
# from ai_parser import AiParser
# import os
# import json
# import time
#
# def main():
#     print("🚀 캠퍼스 밀타임 기숙사 크롤러 시작 (안전한 Rate Limit 방어 모드)")
#
#     crawler = DormCrawler()
#     pdf_path = crawler.download_latest_pdf()
#     if not pdf_path:
#         return
#
#     splitter = ImageSplitter()
#     image_dir = './gishiks/images'
#     full_img_path = splitter.convert_pdf_to_image(pdf_path, image_dir)
#     split_image_paths = splitter.crop_and_compose(full_img_path, image_dir)
#
#     parser = AiParser()
#     all_meals_flat = []
#
#     day_names = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
#
#     print("📦 구글 API 무료 제한을 피하기 위해 1장씩 천천히 분석합니다...")
#
#     for img_path, day in zip(split_image_paths, day_names):
#         # 1. 한 장씩 파싱 (AiParser.py의 parse_image_to_json 사용)
#         parsed_data = parser.parse_image_to_json(img_path, day)
#
#         # 2. 결과 출력 및 가공
#         if parsed_data and "schools" in parsed_data:
#             print(f"✅ {day}요일 파싱 성공!")
#             try:
#                 date_val = parsed_data.get("date", "")
#                 if parsed_data["schools"]:
#                     school_val = parsed_data["schools"][0].get("schoolName", "인하대학교")
#                     if parsed_data["schools"][0].get("cafeterias"):
#                         cafeteria_val = parsed_data["schools"][0]["cafeterias"][0].get("name", "생활관 식당")
#                         meals_dict = parsed_data["schools"][0]["cafeterias"][0].get("meals", {})
#
#                         for meal_time_key, menu_list in meals_dict.items():
#                             for item in menu_list:
#                                 flat_meal = {
#                                     "date": date_val,
#                                     "school": school_val,
#                                     "cafeteria_name": cafeteria_val,
#                                     "meal_time": meal_time_key.upper(),
#                                     "course": item.get("course", "A"),
#                                     "main_menu": item.get("mainMenu", ""),
#                                     "price": item.get("price", 5800)
#                                 }
#                                 all_meals_flat.append(flat_meal)
#             except Exception as e:
#                 print(f"⚠️ JSON 가공 실패 ({day}): {e}")
#         else:
#             print(f"❌ {day}요일 파싱 실패 또는 빈 데이터")
#
#         # 🌟 밥무의 핵심 처방: 무료 티어의 15 RPM(분당 15회) 제한을 완벽히 피하는 마법의 숫자
#         if day != "sun": # 마지막 일요일은 쉬지 않아도 됨
#             print("⏳ API 제한(429 에러) 방어 중... 15초만 숨 고르기 🧘‍♂️")
#             time.sleep(15)
#
#     print("\n" + "="*50)
#     print("📊 [최종 결과물] DB INSERT용 가공 데이터 확인")
#     print("="*50)
#     if all_meals_flat:
#         print(json.dumps(all_meals_flat, indent=2, ensure_ascii=False))
#         print(f"\n✅ 총 {len(all_meals_flat)}개의 메뉴 데이터가 준비되었습니다.")
#     else:
#         print("⚠️ 준비된 데이터가 없습니다.")
#
# if __name__ == "__main__":
#     main()

from crawler import DormCrawler
from image_splitter import ImageSplitter
from ai_parser import AiParser
from db_manager import MealDatabaseManager # 🚨 DB 매니저 임포트 잊지 마!
import os
import json
import time

def main():
    print("🚀 캠퍼스 밀타임 기숙사 크롤러 시작 (실제 DB 연동 모드)")

    crawler = DormCrawler()
    pdf_path = crawler.download_latest_pdf()
    if not pdf_path:
        return

    splitter = ImageSplitter()
    image_dir = './gishiks/images'
    full_img_path = splitter.convert_pdf_to_image(pdf_path, image_dir)
    split_image_paths = splitter.crop_and_compose(full_img_path, image_dir)

    parser = AiParser()
    all_meals_flat = []

    day_names = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

    print("📦 구글 API 무료 제한을 피하기 위해 1장씩 천천히 분석합니다...")

    for img_path, day in zip(split_image_paths, day_names):
        parsed_data = parser.parse_image_to_json(img_path, day)

        if parsed_data and "schools" in parsed_data:
            print(f"✅ {day}요일 파싱 성공!")
            try:
                date_val = parsed_data.get("date", "")
                if parsed_data["schools"]:
                    school_val = parsed_data["schools"][0].get("schoolName", "인하대학교")
                    if parsed_data["schools"][0].get("cafeterias"):
                        cafeteria_val = parsed_data["schools"][0]["cafeterias"][0].get("name", "생활관 식당")
                        meals_dict = parsed_data["schools"][0]["cafeterias"][0].get("meals", {})

                        for meal_time_key, menu_list in meals_dict.items():
                            for item in menu_list:
                                flat_meal = {
                                    "date": date_val,
                                    "school": school_val,
                                    "cafeteria_name": cafeteria_val,
                                    "meal_time": meal_time_key.upper(),
                                    "course": item.get("course", "A"),
                                    "main_menu": item.get("mainMenu", ""),
                                    "price": item.get("price", 5800)
                                }
                                all_meals_flat.append(flat_meal)
            except Exception as e:
                print(f"⚠️ JSON 가공 실패 ({day}): {e}")
        else:
            print(f"❌ {day}요일 파싱 실패 또는 빈 데이터")

        if day != "sun":
            print("⏳ API 제한(429 에러) 방어 중... 15초만 숨 고르기 🧘‍♂️")
            time.sleep(15)

    # 🌟 [추가된 DB 저장 로직]
    print("\n" + "="*50)
    print(f"💾 총 {len(all_meals_flat)}개의 메뉴를 DB에 저장합니다...")
    print("="*50)

    if all_meals_flat:
        try:
            db = MealDatabaseManager() # DB 매니저 인스턴스 생성
            for meal in all_meals_flat:
                # 🚨 주의: db_manager.py의 insert_meal 함수가 받는 파라미터가
                # 정확히 아래 7개여야 해! 안 맞으면 여기서 에러가 날 거야.
                db.insert_meal(
                    date=meal['date'],
                    school=meal['school'],
                    cafeteria_name=meal['cafeteria_name'],
                    meal_time=meal['meal_time'],
                    course=meal['course'],
                    main_menu=meal['main_menu'],
                    price=meal['price']
                )
            db.close()
            print("🎉 [파이프라인 완료] DB 저장이 완벽하게 끝났습니다!")
        except Exception as e:
            print(f"❌ DB 저장 중 치명적 오류 발생: {e}")
    else:
        print("⚠️ 저장할 데이터가 없어 DB 작업을 건너뜁니다.")

if __name__ == "__main__":
    main()