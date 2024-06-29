from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.common.keys import Keys  # type: ignore
from dotenv import dotenv_values  # type: ignore
from selenium.common.exceptions import NoSuchElementException  # type: ignore
import time

# profile.jpg and profile2.jpg were generated using "https://www.thispersondoesnotexist.com"

config = dotenv_values(".env")
TINDER_PHONE = config["TINDER_PHONE"]

URL = "https://tinder.com/"
LIKE_LIMIT = 100

chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option("detach", True)

# Launched the browser
driver = webdriver.Chrome(options=chrome_option)
driver.get(URL)
driver.maximize_window()

time.sleep(3)

# Cookies pop-up
cookies = driver.find_element(
    By.XPATH, value='//*[@id="u1146625330"]/div/div[2]/div/div/div[1]/div[1]/button'
)
cookies.click()

time.sleep(1)

# Starting login process
log_in = driver.find_element(
    By.XPATH,
    value='//*[@id="u-1419960890"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a',
)
log_in.click()

time.sleep(2)

# Choosing login option
phone_login = driver.find_element(
    By.CSS_SELECTOR, value='[aria-label="Log in with phone number"]'
)
phone_login.click()

time.sleep(2)

# Logging in with phone number
enter_phone = driver.find_element(
    By.CSS_SELECTOR, value='[aria-label="Enter your mobile number"]'
)
enter_phone.send_keys(TINDER_PHONE)

next = driver.find_element(
    By.XPATH, value='//*[@id="u1146625330"]/div/div[1]/div[1]/div/div[3]/button'
)
next.click()

time.sleep(40)

# Email verification
email_verif = driver.find_element(
    By.XPATH, value='//*[@id="u1146625330"]/div/div[1]/div/div[1]/div/div[2]/button'
)
email_verif.click()

time.sleep(30)

# Location pop-up
location = driver.find_element(
    By.XPATH, value='//*[@id="u1146625330"]/div/div[1]/div/div/div[3]/button[1]'
)
location.click()

time.sleep(2)

# Notification pop-up
notifications = driver.find_element(
    By.XPATH, value='//*[@id="u1146625330"]/div/div[1]/div/div/div[3]/button[2]'
)
notifications.click()

time.sleep(5)
n = 3
# Created a for loop to like the day's limit
for i in range(LIKE_LIMIT):
    try:
        like = driver.find_element(
            By.XPATH,
            value=f'//*[@id="u-1419960890"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[{n}]/div/div[4]/button',
        )
        like.click()
        n = 3
        time.sleep(2)
    except NoSuchElementException:
        n = 4
        continue
