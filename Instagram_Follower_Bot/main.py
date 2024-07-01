from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.common.keys import Keys  # type: ignore
from dotenv import dotenv_values  # type: ignore
from selenium.common.exceptions import NoSuchElementException  # type: ignore
import time


config = dotenv_values(".env")
IG_EMAIL = config["IG_EMAIL"]
IG_PASS = config["IG_PASS"]
IG_USERNAME = config["IG_USERNAME"]

TARGET_USERNAME = "ThePrimeagen"
# TEST_USERNAME = "nerkyzas"

INSTAGRAM_URL = "https://www.instagram.com"


class Instagram_Follower_Bot:
    def __init__(self):
        self.chrome_option = webdriver.ChromeOptions()
        self.chrome_option.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.chrome_option)
        self.driver.maximize_window()

    def log_in(self):
        self.driver.get(INSTAGRAM_URL)
        time.sleep(5)
        try:
            accept_cookies = self.driver.find_element(
                By.XPATH,
                value="/html/body/div[4]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]",
            )
            accept_cookies.click()

        except NoSuchElementException:
            accept_cookies = self.driver.find_element(
                By.XPATH,
                value="/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]",
            )
            accept_cookies.click()
        time.sleep(2)

        enter_email = self.driver.find_element(
            By.CSS_SELECTOR, value='[aria-label="Phone number, username, or email"]'
        )
        enter_email.send_keys(IG_EMAIL)
        enter_pass = self.driver.find_element(
            By.CSS_SELECTOR, value='[aria-label="Password"]'
        )
        enter_pass.send_keys(IG_PASS)
        login = self.driver.find_element(
            By.XPATH,
            value='//*[@id="loginForm"]/div/div[3]/button',
        )
        login.click()
        time.sleep(10)

    def search(self):
        notification1 = self.driver.find_element(
            By.CSS_SELECTOR,
            value=".x78zum5.xdt5ytf.x1e56ztr",
        )
        notification1.click()
        time.sleep(2)

        notification2 = self.driver.find_element(
            By.CSS_SELECTOR,
            value="._a9--._ap36._a9_1",
        )
        notification2.click()
        time.sleep(2)

        search_button = self.driver.find_element(
            By.LINK_TEXT,
            value="Search",
        )
        search_button.click()
        time.sleep(2)

        enter_username = self.driver.find_element(
            By.CSS_SELECTOR, value='[aria-label="Search input"]'
        )
        enter_username.send_keys(TARGET_USERNAME)
        time.sleep(2)

        ig_user = self.driver.find_element(
            By.CSS_SELECTOR,
            value="span .x1lliihq.x193iq5w.x6ikm8r.x10wlt62.xlyipyv.xuxw1ft",
        )
        ig_user.click()
        time.sleep(3)

    def follow_users(self):
        followers = self.driver.find_element(
            By.XPATH,
            value='//a[contains(text(), " followers")]',
        )
        followers.click()
        time.sleep(3)
        i = 1
        # Created a while loop to go over user database
        while True:
            try:
                i += 1
                follow = self.driver.find_element(
                    By.XPATH,
                    value=f"/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[{i}]/div/div/div/div[3]/div/button",
                )
                follow.click()
                time.sleep(1)
            except NoSuchElementException:
                break
            # Set a rule to load more users
            else:
                if i % 10 == 0:
                    time.sleep(2)


test = Instagram_Follower_Bot()
test.log_in()
test.search()
test.follow_users()
