import requests  # type: ignore
from dotenv import dotenv_values  # type: ignore
from datetime import date, timedelta


class FlightSearch:
    def __init__(self):
        config = dotenv_values(".env")
        self.api_key = config["AMADEUS_API_KEY"]
        self.api_secret = config["AMADEUS_API_SECRET"]
        self.access_token = self.authenticate()
        self.home_iata = "VNO"

    def authenticate(self):
        auth_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        auth_header = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret,
        }
        auth_response = requests.post(url=auth_url, headers=auth_header, data=data)
        auth_response.raise_for_status
        return auth_response.json()["access_token"]

    def get_iata(self, city):
        endpoint = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
        header = {"Authorization": f"Bearer {self.access_token}"}
        parameters = {
            "keyword": city.upper(),
        }
        iata_response = requests.get(url=endpoint, headers=header, params=parameters)
        iata_response.raise_for_status
        return iata_response.json()["data"][0]["iataCode"]

    def find_cheapest_flight(self, destination: str, max_price: int, adults, non_stop):
        departure_date = str(date.today() + timedelta(days=1))
        return_date = str(date.today() + timedelta(days=6))
        header = {"Authorization": f"Bearer {self.access_token}"}
        endpoint = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        parameters = {
            "originLocationCode": self.home_iata,
            "destinationLocationCode": destination,
            "departureDate": departure_date,
            "returnDate": return_date,
            "adults": adults,
            "nonStop": non_stop,
            "currencyCode": "EUR",
            "maxPrice": max_price,
        }
        data_response = requests.get(url=endpoint, headers=header, params=parameters)
        data_response.raise_for_status
        low_price = max_price
        for i in data_response.json()["data"]:
            price = float(i["price"]["grandTotal"])
            if price < low_price:
                low_price = price
                carrier_code_ob = i["itineraries"][0]["segments"][0]["operating"][
                    "carrierCode"
                ]
                carrier_code_return = i["itineraries"][-1]["segments"][0]["operating"][
                    "carrierCode"
                ]
                dep_iata = i["itineraries"][0]["segments"][0]["departure"]["iataCode"]
                arr_iata = i["itineraries"][-1]["segments"][0]["departure"]["iataCode"]
                ob_date = i["itineraries"][0]["segments"][0]["departure"]["at"].split(
                    "T"
                )
                return_date = i["itineraries"][-1]["segments"][0]["departure"][
                    "at"
                ].split("T")
        if low_price < max_price:
            return (
                low_price,
                carrier_code_ob,
                carrier_code_return,
                dep_iata,
                arr_iata,
                ob_date,
                return_date,
            )
            # if UnboundLocalError
        else:
            return False
