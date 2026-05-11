import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager # 드라이버 자동 관리
import time

def get_research_daily():
    chrome_options = Options()
    chrome_options.add_argument('--headless') # 창 없는 모드 필수
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # 로봇으로 인식되지 않게 하는 설정 추가
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')

    # 드라이버 설치 자동화
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get("https://www.perplexity.ai")
        time.sleep(15) # 페이지 로딩 대기 시간 증가
        
        # 검색창 찾기 (더 유연한 방식)
        search_box = driver.find_element(By.CSS_SELECTOR, "textarea")
        search_box.send_keys("running, shoe, insole, midsole, outsole, walking, Footwear 관련 최신 논문 5개 요약해줘")
        search_box.send_keys(Keys.ENTER)

        time.sleep(60) # AI 답변 생성 대기 시간 대폭 증가

        # 결과 추출 (클래스명이 바뀔 수 있으므로 시도 후 실패 시 예외처리)
        try:
            result = driver.find_element(By.CSS_SELECTOR, ".prose").text
            with open("today_research.md", "w", encoding="utf-8") as f:
                f.write(result)
            print("성공적으로 저장되었습니다.")
        except:
            print("결과 창을 찾지 못했습니다. 화면 구조가 변경되었을 수 있습니다.")
            # 실패 시 현재 화면을 저장해서 나중에 확인 가능 (디버깅용)
            driver.save_screenshot("error_screenshot.png")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    get_research_daily()
