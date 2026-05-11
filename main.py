import os
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_research_daily():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # 봇 감지 회피를 위한 위장 설정
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # 1. 접속
        driver.get("https://www.perplexity.ai")
        
        # 2. 검색창이 나타날 때까지 최대 20초 대기 (핵심 수정 사항)
        wait = WebDriverWait(driver, 20)
        try:
            # 여러 타입의 검색창 요소를 시도
            search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea")))
        except:
            # 에러 발생 시 현재 화면 캡처 (GitHub Actions Artifacts에서 확인 가능)
            driver.save_screenshot("debug_screen.png")
            print("검색창을 찾을 수 없습니다. debug_screen.png 확인이 필요합니다.")
            return

        # 3. 검색어 입력 (한 글자씩 타이핑하는 느낌으로)
        query = "running, shoe, insole, midsole, outsole, walking, Footwear 관련 최신 논문 5개 요약해줘"
        search_box.send_keys(query)
        time.sleep(2)
        search_box.send_keys(Keys.ENTER)

        # 4. 답변 생성 대기 (여유 있게 60초)
        print("답변 생성 대기 중...")
        time.sleep(60)

        # 5. 결과 추출
        results = driver.find_elements(By.CSS_SELECTOR, ".prose")
        if results:
            result_text = results[0].text
            Path("today_research.md").write_text(result_text, encoding="utf-8")
            print("저장 완료!")
        else:
            print("답변 텍스트 영역을 찾지 못했습니다.")
            driver.save_screenshot("no_result_screen.png")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    get_research_daily()
