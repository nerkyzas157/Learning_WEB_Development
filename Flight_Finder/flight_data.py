class FlightData:
    def msg_body(self, flight_data):
        return f"Subject: Low price alert!\nOnly {flight_data[0]} Euros to fly from {flight_data[3]} to {flight_data[4]}, on {flight_data[5][0]} until {flight_data[6][0]}. Outbound flight is with {flight_data[1]} and return flight is with {flight_data[2]}."


# low_price, carrier_code_ob, carrier_code_return, dep_iata, arr_iata, ob_date, return_date
