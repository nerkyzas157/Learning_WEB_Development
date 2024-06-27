from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.common.keys import Keys  # type: ignore
from dotenv import dotenv_values  # type: ignore
from selenium.common.exceptions import NoSuchElementException  # type: ignore
import time

config = dotenv_values(".env")
LINKEDIN_EMAIL = config["LINKEDIN_EMAIL"]
LINKEDIN_PASSWORD = config["LINKEDIN_PASSWORD"]
LINKEDIN_PHONE = config["LINKEDIN_PHONE"]
URL = "https://www.linkedin.com/feed/"

job_keys = ["python", "data science", "data intern"]
job_key_index = 0

chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option("detach", True)

# Launched the browser
driver = webdriver.Chrome(options=chrome_option)
driver.get(URL)
driver.maximize_window()

email_field = driver.find_element(By.ID, value="username")
email_field.send_keys(LINKEDIN_EMAIL)
password_field = driver.find_element(By.ID, value="password")
password_field.send_keys(LINKEDIN_PASSWORD)
signin_button = driver.find_element(By.CLASS_NAME, value="btn__primary--large")
signin_button.click()

# Manual security check
time.sleep(15)

while True:
    search = driver.find_element(By.CLASS_NAME, value="search-global-typeahead__input")
    search.send_keys(job_keys[job_key_index], Keys.ENTER)

    time.sleep(5)

    jobs_button = driver.find_element(
        By.XPATH, value='//*[@id="search-reusables__filters-bar"]/ul/li[1]'
    )
    jobs_button.click()

    time.sleep(5)

    easy_apply = driver.find_element(
        By.XPATH,
        value='//*[@id="search-reusables__filters-bar"]/ul/li[8]/div/button',
    )
    easy_apply.click()

    time.sleep(3)

    try:
        apply = driver.find_element(
            By.XPATH,
            value='//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[5]/div/div/div/button',
        )
        apply.click()

    except NoSuchElementException:
        job_key_index += 1
        driver.get(URL)
        if job_key_index == len(job_keys):
            break
    else:
        time.sleep(3)

        phone = driver.find_element(By.CLASS_NAME, value="artdeco-text-input--input")
        phone.send_keys(LINKEDIN_PHONE)

        next_button = driver.find_element(
            By.CSS_SELECTOR, '[aria-label="Continue to next step"]'
        )
        next_button.click()

        time.sleep(3)

        try:
            review_button = driver.find_element(
                By.CSS_SELECTOR, value='[aria-label="Review your application"]'
            )
            review_button.click()

        except NoSuchElementException:
            job_key_index += 1
            driver.get(URL)
            if job_key_index == len(job_keys):
                break

        else:
            time.sleep(3)
            submit_button = driver.find_element(
                By.CSS_SELECTOR, value='[aria-label="Submit application"]'
            )
            submit_button.click()
            time.sleep(2)
            driver.get(URL)
