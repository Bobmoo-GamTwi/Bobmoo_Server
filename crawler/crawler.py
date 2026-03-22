import os
import requests
from bs4 import BeautifulSoup
from datetime import date

class DormCrawler:
    def __init__(self):
        self.base_url = 'https://dorm.inha.ac.kr'
        self.board_url = f'{self.base_url}/bbs/dorm/2533/artclList.do'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
        }

    def download_latest_pdf(self) -> str:
        save_dir = './gishiks'
        os.makedirs(save_dir, exist_ok=True)

        try:
            # 1. 목록 페이지 접속
            html = requests.get(self.board_url, headers=self.headers).content
            soup = BeautifulSoup(html, "html.parser")
            this_week_page = soup.find('a', class_='artclLinkView')

            if not this_week_page:
                print("🚨 최신 식단글을 찾을 수 없습니다.")
                return None

            # 2. 상세 페이지 접속
            article_url = f"{self.base_url}{this_week_page['href']}"
            detail_html = requests.get(article_url, headers=self.headers).content
            soup_detail = BeautifulSoup(detail_html, "html.parser")

            # 3. PDF 다운로드
            # pdf_link_tag = soup_detail.select_one('a[href*="download.do"]')
            # if not pdf_link_tag:
            #     print("🚨 첨부된 PDF 파일을 찾을 수 없습니다.")
            #     return None
            #
            # download_url = f"{self.base_url}{pdf_link_tag['href']}"
            # file_name = f'gishik_{date.today().strftime("%Y-%m-%d")}.pdf'
            # path_to_save = os.path.join(save_dir, file_name)
            #
            # response = requests.get(download_url, headers=self.headers)
            # with open(path_to_save, 'wb') as file:
            #     file.write(response.content)
            #
            # print(f"✅ PDF 다운로드 완료: {path_to_save}")
            # return path_to_save

            # 3. PDF 다운로드
            # select_one 대신 select를 써서 조건에 맞는 모든 a 태그를 가져옴
            pdf_link_tags = soup_detail.select('a[href*="download.do"]')

            if not pdf_link_tags:
                print("🚨 첨부된 PDF 파일을 찾을 수 없습니다.")
                return None

            target_pdf_tag = None

            # 🌟 밥무의 팁: 가져온 링크들을 하나씩 검사해서 "(영문)"이 없는 것만 픽!
            for tag in pdf_link_tags:
                file_name_text = tag.text.strip() # " 0309(영문).pdf " 같은 문자열
                if "(영문)" not in file_name_text:
                    target_pdf_tag = tag
                    break # 찾았으면 반복문 즉시 종료

            # 만약 한글 PDF를 끝내 못 찾았다면? 방어 로직!
            if not target_pdf_tag:
                print("🚨 한글 식단표 PDF를 찾을 수 없습니다.")
                return None

            # 찾은 태그의 href로 다운로드 URL 생성
            download_url = f"{self.base_url}{target_pdf_tag['href']}"
            file_name = f'gishik_{date.today().strftime("%Y-%m-%d")}.pdf'
            path_to_save = os.path.join(save_dir, file_name)

            response = requests.get(download_url, headers=self.headers)
            with open(path_to_save, 'wb') as file:
                file.write(response.content)

            print(f"✅ PDF 다운로드 완료: {path_to_save}")
            return path_to_save

        except Exception as e:
            print(f"❌ 다운로드 에러: {e}")
            return None