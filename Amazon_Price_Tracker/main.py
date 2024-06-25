import smtplib
import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
from dotenv import dotenv_values  # type: ignore

# Set a constant variable for the URL
URL = "https://www.amazon.com/PlayStation®5-console-slim-PlayStation-5/dp/B0CL61F39H/ref=sr_1_1"

# Made soup
response = requests.get(URL)
html = response.text
soup = BeautifulSoup(html, "html.parser")

# Pulled price and item name
item_name_tag = soup.find(name="span", id="productTitle", class_="a-size-large")
price_tag = soup.find(name="span", class_="a-offscreen")
price = float(price_tag.getText()[1:])
def_item_name = bytes(item_name_tag.getText().strip(), "utf-8")
item_name = def_item_name.decode("ascii", "ignore")

# Pull credentials
config = dotenv_values(".env")
my_email = config["SMTP_EMAIL"]
app_password = config["SMTP_APP_PASS"]

# Check price, if satisfied, notify user
if price > 400:
    connection = smtplib.SMTP("smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(user=my_email, password=app_password)
    connection.sendmail(
        from_addr=my_email,
        to_addrs="nerijus157@gmail.com",
        msg=f'Subject: Alert!\nPrice for "{item_name}" dropped below your target! It\'s waiting for you only at ${price}.',
    )
