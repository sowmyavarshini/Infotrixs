import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
api_key = os.getenv("api_key")
OWM_endpoint = "https://api.openweathermap.org/data/2.5/weather"
favorite_city = []


# function for checking weather details
def get_weather_by_city(city_name):
        params = {
            'q': city_name,
            'appid': api_key,

        }

        try:
            # sending http request
            response = requests.get(OWM_endpoint, params=params)
            # data in json format
            weather_data = response.json()

            # status_code=200 means it is successful
            if response.status_code == 200:
                return weather_data
            else:
                print(f"Error: {weather_data['message']}")
                return None

        except requests.RequestException as e:
            print(f"Request Error: {e}")
            return None


#function to add fav cities
def add_favorite_city(city_name):
    if city_name not in favorite_city:
        favorite_city.append(city_name)  # adding cities to the empty list
        print(f"{city_name} added to favorites.")


def remove_favorite_city(city_name):
    if city_name in favorite_city:  # removing city from fav as per user choice
        favorite_city.remove(city_name)
        print(f"{city_name} removed from favorites.")
    else:
        print(f"{city_name} is not in favorites.")


def list_favorite_cities():  # printing fav cities in the list
    print("Favorite Cities:")
    for city in favorite_city:
        print(f"- {city}")


def auto_refresh(interval_sec):
    for _ in range(2):
        for city in favorite_city:
            data = get_weather_by_city(city)
            if data:
                print(f"Weather in {city}: {data['weather'][0]['description']}, "
                          f"Temperature: {data['main']['temp']}°C")
        time.sleep(interval_sec)


while True:
    print("\n")
    print("Options:")
    print("1. Check weather by city")
    print("2. Add favorite city")
    print("3. Remove favorite city")
    print("4. List favorite cities")
    print("5. Auto refresh favorite cities")
    print("6. Quit")
    print("\n")

    # users choice
    choice = input("Enter your choice (1-6): ")

    # checking users choice
    if choice == "1":
        city_name = input("Enter city name: ").lower().strip()
        weather_data = get_weather_by_city(city_name)
        if weather_data:
            print(f"Weather in {city_name}: {weather_data['weather'][0]['description']}, "
                  f"Temperature: {weather_data['main']['temp']}°C")

    elif choice == "2":
        city_name = input("Enter city name to add to favorites: ")
        add_favorite_city(city_name)

    elif choice == "3":
        city_name = input("Enter city name to remove from favorites: ")
        remove_favorite_city(city_name)

    elif choice == "4":
        list_favorite_cities()

    elif choice == "5":
        interval_sec = int(input("Enter auto-refresh interval in seconds (e.g., 15): "))
        auto_refresh(interval_sec)

    elif choice == "6":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please enter a number between 1 and 6.")

