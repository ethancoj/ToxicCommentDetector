# twitter_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def login_twitter(driver, username, password):
    driver.get("https://twitter.com/login")
    time.sleep(5)

    username_input = driver.find_element(By.NAME, "text")
    username_input.send_keys(username)
    driver.find_element(By.XPATH, '//span[text()="Next"]').click()
    time.sleep(3)

    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(password)
    driver.find_element(By.XPATH, '//span[text()="Log in"]').click()
    time.sleep(5)

def scrape_replies(tweet_url, username, password, max_scrolls=5):
    options = Options()
    # options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    login_twitter(driver, username, password)
    
    driver.get(tweet_url)
    time.sleep(5)

    replies = set()
    for _ in range(max_scrolls):
        elements = driver.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')
        for el in elements:
            text = el.text.strip()
            if text:
                replies.add(text)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    driver.quit()
    return list(replies)
