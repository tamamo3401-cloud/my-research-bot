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
    chrome_options.add_argument('--headless=new') # 최신 헤드리스 모드 사용
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080') # 화면 크기 고정
    
    # 봇 감지 우회를 위한 핵심 설정
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # 실행 시 로봇 속성 제거 스크립트
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })

    try:
        print("퍼플렉시티 접속 시도...")
        driver.get("https://www.perplexity.ai")
        
        # 페이지가 완전히 로드될 때까지 충분히 대기
        time.sleep(10)
        
        # 검색창 대기 및 찾기
        wait = WebDriverWait(driver, 30)
        try:
            # tag_name 대신 더 구체적인 CSS 선택자 사용
            search_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[placeholder*='Anything']")))
            print("검색창 발견!")
        except Exception as e:
            print(f"검색창 찾기 실패: {e}")
            driver.save_screenshot("error_capture.png") # 실패 시 화면 캡처
            return

        # 타이핑 시뮬레이션
        query = "running, shoe, insole, midsole, outsole, walking, Footwear 관련 최신 논문 5개 요약해줘"
        search_box.send_keys(query)
        time.sleep(2)
        search_box.send_keys(Keys.ENTER)

        print("답변 대기 중 (60초)...")
        time.sleep(60)

        # 결과 추출
        try:
            # 답변 영역이 생성될 때까지 대기
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".prose")))
            results = driver.find_elements(By.CSS_SELECTOR, ".prose")
            result_text = results[-1].text # 가장 최근 답변 가져오기
            Path("today_research.md").write_text(result_text, encoding="utf-8")
            print("오늘의 논문 저장 완료!")
        except:
            print("답변을 찾을 수 없습니다.")
            driver.save_screenshot("no_answer.png")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    get_research_daily()
