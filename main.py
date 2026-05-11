import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from pathlib import Path

def get_research_daily():
    # 1. 헤드리스 크롬 설정 (온라인 서버용 필수 설정)
    chrome_options = Options()
    chrome_options.add_argument('--headless') # 창 안띄움
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://www.perplexity.ai")
        time.sleep(10) # 서버 속도를 고려해 대기 시간 연장
        
        # 검색어 입력
        search_box = driver.find_element(By.TAG_NAME, "textarea")
        query = "running, shoe, insole, midsole, outsole, walking, Footwear 관련 최신 논문 5개 요약해줘"
        search_box.send_keys(query)
        search_box.send_keys(Keys.ENTER)

        time.sleep(40) # AI 답변 대기

        # 결과 추출
        result = driver.find_element(By.CLASS_NAME, "prose").text
        
        # 파일 저장
        output_path = Path("today_research.md")
        output_path.write_text(result, encoding="utf-8")
        print("논문 요약 완료!")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    get_research_daily()