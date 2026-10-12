import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def get_weather(city):
    if not city or not city.strip():
        print("Error: City name cannot be empty.")
        return

    try:
        location_response = requests.get(
            GEOCODING_URL,
            params={"name": city.strip(), "count": 1, "language": "en"},
            timeout=10
        )
        location_response.raise_for_status()
        locations = location_response.json().get("results", [])

        if not locations:
            print("Error: City not found. Please try another city.")
            return

        location = locations[0]
        latitude = location["latitude"]
        longitude = location["longitude"]

        weather_response = requests.get(
            BASE_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,"
                           "apparent_temperature,wind_speed_10m"
            },
            timeout=10
        )
        weather_response.raise_for_status()
        weather = weather_response.json().get("current")

        if not weather:
            print("Error: Weather information is unavailable.")
            return

        print("\n--- Weather Information ---")
        print("City:", location["name"])
        print("Country:", location.get("country", "Unknown"))
        print("Temperature:", weather["temperature_2m"], "°C")
        print("Feels like:", weather["apparent_temperature"], "°C")
        print("Humidity:", weather["relative_humidity_2m"], "%")
        print("Wind speed:", weather["wind_speed_10m"], "km/h")

    except requests.exceptions.Timeout:
        print("Error: Request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        print("Error: Check your internet connection.")
    except requests.exceptions.HTTPError:
        print("Error: The weather service returned an error.")
    except (ValueError, KeyError):
        print("Error: Unable to process the weather data.")
    except requests.exceptions.RequestException:
        print("Error: Something went wrong while contacting the API.")


if __name__ == "__main__":
    city_name = input("Enter city name: ")
    get_weather(city_name)