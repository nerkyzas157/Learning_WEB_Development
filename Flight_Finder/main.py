# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager

f_data = FlightData()
connect = NotificationManager()
flight_search = FlightSearch()
db = DataManager()
sheet_data = db.get_sheet_data()

for i in sheet_data:
    # If IATA field empty, update it with corresponding IATA code
    if len(i["iataCode"]) == 0:
        iata = flight_search.get_iata(i["city"])
        db.put_iata(iata=iata, row=i["id"])
    # Find cheapest flight to that city
    flight_data = flight_search.find_cheapest_flight(i["iataCode"], 400, adults=1, non_stop="true")
    # If no cheap flights were found, continue with the loop
    if flight_data == False:
        print(f"No cheap flight were found for {i["city"]}.")
        continue
    # If requirments were satisfied, form a message and send it to the target
    else:
        email_list = db.get_emails()
        for n in email_list:
            connect.send_email(email=n["email"], email_text=f_data.msg_body(flight_data))


# i["lowestPrice"]
