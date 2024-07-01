from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.common.keys import Keys  # type: ignore
from selenium.common.exceptions import NoSuchElementException  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
import requests  # type: ignore
import time


GOOGLE_FORMS_URL = "https://forms.gle/k9pupcVzKLcWumU39"
ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"

response = requests.get(ZILLOW_URL)
html = response.text
soup = BeautifulSoup(html, "html.parser")
addresses = soup.find_all(name="address")
prices = soup.find_all(class_="PropertyCardWrapper__StyledPriceLine")
links = soup.find_all(class_="property-card-link")

address_list = []
price_list = []
link_list = []

for i in addresses:
    address = (i.getText()).strip()
    address_list.append(address)

for i in prices:
    full_price = (i.getText()).split("+")[0]
    price = full_price.split("/")[0]
    price_list.append(price)

for i in links:
    link_list.append(i.get("href"))


chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_option)
driver.maximize_window()

driver.get(GOOGLE_FORMS_URL)
time.sleep(5)

for i in address_list:
    list_index = address_list.index(i)

    enter_address = driver.find_element(
        By.XPATH,
        value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input',
    )
    enter_address.send_keys(i)

    enter_price = driver.find_element(
        By.XPATH,
        value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input',
    )
    enter_price.send_keys(price_list[list_index])

    enter_link = driver.find_element(
        By.XPATH,
        value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input',
    )
    enter_link.send_keys(link_list[list_index])

    submit_button = driver.find_element(
        By.XPATH,
        value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div',
    )
    submit_button.click()

    time.sleep(3)

    new_response = driver.find_element(
        By.XPATH, value="/html/body/div[1]/div[2]/div[1]/div/div[4]/a"
    )
    new_response.click()

    time.sleep(3)

driver.quit()
