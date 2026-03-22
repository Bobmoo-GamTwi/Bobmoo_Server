import pymysql
import os
from dotenv import load_dotenv

class MealDatabaseManager:
    def __init__(self):
        load_dotenv()
        self.conn = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            db=os.getenv('DB_NAME'),
            charset='utf8mb4'
        )

    # 파라미터 7개로 확장!
    def insert_meal(self, date, school, cafeteria_name, meal_time, course, main_menu, price):
        try:
            with self.conn.cursor() as cursor:
                # 네가 알려준 완벽한 INSERT 쿼리문 적용!
                sql = """
                INSERT INTO meal (date, school, cafeteria_name, meal_time, course, main_menu, price)
                VALUES (%s, %s, %s, %s, %s, %s, %s) 
                """
                cursor.execute(sql, (date, school, cafeteria_name, meal_time, course, main_menu, price))
            self.conn.commit()
            print(f"✅ DB 삽입 완료: {date} [{meal_time}] {course}코스")

        except Exception as e:
            print(f"❌ DB 삽입 실패: {e}")
            self.conn.rollback()

    def close(self):
        self.conn.close()