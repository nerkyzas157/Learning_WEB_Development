from datetime import date
import requests  # type: ignore
from credentials import TOKEN

USERNAME = "nerkyzas157"
GRAPH_ID = "beergraph1"

# Defined dynamic date variable:
today = date.today().strftime("%Y%m%d")

# Defined headers parameters:
headers = {
    "X-USER-TOKEN": TOKEN,
}

# Created user credentials:
user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

pixela_endpoint = "https://pixe.la/v1/users"

# Sent POST request to create the account:
response = requests.post(url=pixela_endpoint, json=user_params)
print(response.text)


# Created graph specifications:
graph_config = {
    "id": GRAPH_ID,
    "name": "Beer Drank",
    "unit": "litres",
    "type": "float",
    "color": "ichou",
}

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

# Sent POST request to create the graph
response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
print(response.text)

# Created pixel specifications:
pixel_config = {
    "date": today,
    "quantity": "1",
}

pixel_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"

# Sent POST request to create a pixel in the graph
response = requests.post(url=pixel_endpoint, json=pixel_config, headers=headers)
print(response.text)

# Updating the graph with current timezone:
update_graph_config = {
    "timezone": "Europe/Vilnius",
}
update_response = requests.put(
    url=pixel_endpoint, json=update_graph_config, headers=headers
)
print(update_response.text)

# Deleting test pixel:
del_pixel_endpoint = requests.delete(
    f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today}"
)
print(del_pixel_endpoint.text)

# Defined WEB link to access the graph on the browser:
WEB_LINK = "https://pixe.la//v1/users/nerkyzas157/graphs/beergraph1.html"

# TODO: Create GUI application for creating new pixels
