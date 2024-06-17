import requests  # type: ignore
from datetime import date, datetime
from credentials import NUTRITION_API_KEY, NUTRITION_APP_ID, SHEET_API_PASS

# Asking user for input to define their body metrics
weight = input("What's your weight in kilograms: ")
height = input("What's your height in centimeters: ")
age = input("How old are you? ")

# Set dynamic variables for date and time
today = date.today().strftime("%d/%m/%Y")
cur_time = datetime.now().strftime("%H:%M:%S")

# NutritionIX API endpoint and header
nut_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
nut_header = {"x-app-key": NUTRITION_API_KEY, "x-app-id": NUTRITION_APP_ID}

# Sheety API endpoint and header
sheet_endpoint = (
    "https://api.sheety.co/0709f3ce4d1ea714fa09186598fa8811/myWorkouts/workouts"
)
sheet_header = {"Authorization": f"Bearer {SHEET_API_PASS}"}

# Created a loop to update the tracker
while True:
    workout = input("Describe your workout: ").lower()
    if workout == "end":
        break
    nut_parameters = {
        "query": workout,
        "weight_kg": weight,
        "height_cm": height,
        "age": age,
    }
    # Used NutritionIX NLP API to generate workout results and characteristics
    nut_response = requests.post(
        url=nut_endpoint, json=nut_parameters, headers=nut_header
    )
    nut_data = nut_response.json()["exercises"][0]
    duration = nut_data["duration_min"]
    calories = nut_data["nf_calories"]
    exercise = nut_data["name"]
    sheet_parameters = {
        "workout": {
            "date": today,
            "time": cur_time,
            "exercise": exercise.title(),
            "duration": duration,
            "calories": calories,
        }
    }
    # Updated sheet by sending POST request to Sheety API
    sheet_response = requests.post(
        url=sheet_endpoint, json=sheet_parameters, headers=sheet_header
    )
    print(
        "Your workout sheet has been updated.\nIf you are finished with updating your tracker, enter 'end'."
    )
