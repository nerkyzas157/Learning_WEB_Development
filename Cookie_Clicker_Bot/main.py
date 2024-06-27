from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.common.keys import Keys  # type: ignore
import time


URL = "http://orteil.dashnet.org/experiments/cookie/"

chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option("detach", True)

# Launched the browser
driver = webdriver.Chrome(options=chrome_option)
driver.get(URL)
driver.maximize_window()

# Defined "Cookie"
cookie = driver.find_element(By.ID, value="cookie")


# Created a function for refreshing buttons and buying upgrades
def buy(best_buy):
    n = prices.index(best_buy)
    if n == 0:
        cursor = driver.find_element(By.ID, value="buyCursor")
        cursor.click()
    elif n == 1:
        grandma = driver.find_element(By.ID, value="buyGrandma")
        grandma.click()
    elif n == 2:
        factory = driver.find_element(By.ID, value="buyFactory")
        factory.click()
    elif n == 3:
        mine = driver.find_element(By.ID, value="buyMine")
        mine.click()


# Defined variables
score = driver.find_element(By.ID, value="cps")

cursor_price = int(
    (driver.find_element(By.CSS_SELECTOR, value="#buyCursor b"))
    .text.split(" - ")[1]
    .replace(",", "")
)
grandma_price = int(
    (driver.find_element(By.CSS_SELECTOR, value="#buyGrandma b"))
    .text.split(" - ")[1]
    .replace(",", "")
)
factory_price = int(
    (driver.find_element(By.CSS_SELECTOR, value="#buyFactory b"))
    .text.split(" - ")[1]
    .replace(",", "")
)
mine_price = int(
    (driver.find_element(By.CSS_SELECTOR, value="#buyMine b"))
    .text.split(" - ")[1]
    .replace(",", "")
)

prices = [cursor_price, grandma_price, factory_price, mine_price]

# Set bot rules
start = time.time()
end_game = time.time()
while True:
    cookie.click()
    end = time.time()
    if (end - start) > 3:
        start = time.time()
        affordable = []
        for i in prices:
            money = int(
                (driver.find_element(By.ID, value="money")).text.replace(",", "")
            )
            if money > i:
                affordable.append(i)
        try:
            best_buy = max(affordable)
        except ValueError:
            pass
        else:
            buy(best_buy)
        finally:
            if (end - end_game) > 300:
                print(f"Your final score is {score.text}")
                break

driver.quit()
