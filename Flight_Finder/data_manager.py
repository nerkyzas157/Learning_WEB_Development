import requests  # type: ignore
from dotenv import dotenv_values  # type: ignore


class DataManager:
    def __init__(self):
        config = dotenv_values(".env")
        api_pass = config["SHEETY_API_PASS"]
        self.get_endpoint = config["PRICES_ENDPOINT"]
        self.users_get_endpoint = config["USERS_ENDPOINT"]
        self.sheet_header = {"Authorization": f"Bearer {api_pass}"}

    def get_sheet_data(self):
        get_response = requests.get(url=self.get_endpoint, headers=self.sheet_header)
        get_response.raise_for_status
        return get_response.json()["prices"]

    def put_iata(self, iata: str, row: int):
        put_endpoint = self.get_endpoint + f"/{row}"
        sheet_parameters = {
            "price": {
                "iataCode": iata,
            }
        }
        put_response = requests.put(
            url=put_endpoint, json=sheet_parameters, headers=self.sheet_header
        )
        put_response.raise_for_status

    def get_emails(self):
        get_response = requests.get(
            url=self.users_get_endpoint, headers=self.sheet_header
        )
        get_response.raise_for_status
        return get_response.json()["users"]
