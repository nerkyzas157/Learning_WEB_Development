from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.common.keys import Keys  # type: ignore
from dotenv import dotenv_values  # type: ignore
from selenium.common.exceptions import NoSuchElementException  # type: ignore
import time


config = dotenv_values(".env")
X_EMAIL = config["X_EMAIL"]
X_PASS = config["X_PASS"]
X_USERNAME = config["X_USERNAME"]

SPEEDTEST_URL = "https://www.speedtest.net"
X_URL = "https://x.com/"


class InternetSpeedTwitterBot:
    def __init__(self):
        self.chrome_option = webdriver.ChromeOptions()
        self.chrome_option.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.chrome_option)
        self.driver.maximize_window()
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        self.driver.get(SPEEDTEST_URL)
        time.sleep(3)
        speedtest = self.driver.find_element(
            By.XPATH,
            value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a/span[4]',
        )
        speedtest.click()
        time.sleep(60)
        self.down = float(
            (self.driver.find_element(By.CLASS_NAME, value="download-speed")).text
        )
        self.up = float(
            (self.driver.find_element(By.CLASS_NAME, value="upload-speed")).text
        )

    def tweet_at_provider(self):
        if self.down < 150 or self.up < 10:
            self.driver.get(X_URL)
            time.sleep(5)
            # Accept cookies
            cookies = self.driver.find_element(
                By.XPATH,
                value='//*[@id="layers"]/div/div[1]/div/div/div/div[2]/button[1]',
            )
            cookies.click()
            time.sleep(1)

            # Close welcoming
            welcoming = self.driver.find_element(
                By.XPATH, value='//*[@id="layers"]/div/div[2]/div/div/div/button'
            )
            welcoming.click()
            time.sleep(1)

            # Sign into X
            try:
                sign_in4 = self.driver.find_element(
                    By.XPATH,
                    value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[4]/a',
                )
                sign_in4.click()

            except NoSuchElementException:
                sign_in3 = self.driver.find_element(
                    By.XPATH,
                    value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[3]/a',
                )
                sign_in3.click()

            # Sign in with creds
            time.sleep(3)
            enter_email = self.driver.find_element(By.CSS_SELECTOR, value="input")
            enter_email.send_keys(X_EMAIL)

            next_button = self.driver.find_element(
                By.XPATH,
                value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]',
            )
            next_button.click()
            time.sleep(2)

            # Additional verification prompt
            try:
                text = "Enter your phone number or username"
                if (
                    text
                    == (
                        self.driver.find_element(
                            By.XPATH,
                            value='//*[@id="modal-header"]/span/span',
                        )
                    ).text
                ):
                    pass
                else:
                    # Non-existing element to create error
                    next_button = self.driver.find_element(
                        By.XPATH, value='//*[@id="new-error"]'
                    )

            except NoSuchElementException:
                enter_password = self.driver.find_element(By.NAME, value="password")
                enter_password.send_keys(X_PASS)

                login_button = self.driver.find_element(
                    By.XPATH,
                    value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input',
                )
                login_button.click()

            else:
                enter_username = self.driver.find_element(
                    By.CSS_SELECTOR, value="input"
                )
                enter_username.send_keys(X_USERNAME)

                next_button = self.driver.find_element(
                    By.XPATH,
                    value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button',
                )
                next_button.click()
                time.sleep(2)

                enter_password = self.driver.find_element(By.NAME, value="password")
                enter_password.send_keys(X_PASS)

                login_button = self.driver.find_element(
                    By.XPATH,
                    value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button',
                )
                login_button.click()

            # Post a tweet
            time.sleep(5)
            tweet_text = f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for 150down/10up?"

            start_tweet = self.driver.find_element(
                By.XPATH,
                value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div',
            )
            start_tweet.click()

            time.sleep(1)
            type_tweet = self.driver.find_element(
                By.CSS_SELECTOR,
                value="br[data-text='true']",
            )
            type_tweet.send_keys(tweet_text)

            post_tweet = self.driver.find_element(
                By.XPATH,
                value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button',
            )
            post_tweet.click()


x_bot = InternetSpeedTwitterBot()
x_bot.get_internet_speed()
x_bot.tweet_at_provider()
