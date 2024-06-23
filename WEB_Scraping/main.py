import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore

# Set URL as constant variable:
URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Scraping the WEB:
response = requests.get(URL)
html = response.text
soup = BeautifulSoup(html, "html.parser")
names = soup.find_all(name="h3", class_="title")
names.reverse()

# Transforming the data:
name_list = []

for i in names:
    name_list.append(i.getText())

# Creating a text file:
with open("movies.txt", mode="w") as file_to_create:
    # Appending data into the text file:
    with open(
        "movies.txt",
        mode="a",
        encoding="utf-8",
    ) as file:
        for i in name_list:
            file.write(f"{i}\n")
