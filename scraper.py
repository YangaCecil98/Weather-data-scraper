#Importing necessary packages/libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = 'https://www.theweathernetwork.com/en/city/za/oos-kaap/umtata/7-days'
#HTTP GET() Request from a server/db
response = requests.get(url)
#Status Request
print(f"status_code: {response.status_code}")
print()
soup = BeautifulSoup(response.text, 'html.parser')
#Value extracting function from the source code
def get_value(soup):

    elements = soup.select('[data-testid="forecast-module-row"]')

    weather_record = []

    for row in elements:

        # Time of day
        time_element = row.select_one(
            '[data-testid="row-date-or-time"]'
        )
        time = time_element.get_text(strip=True) if time_element else None

        # Temperature
        temperature_element = row.select_one(
            '[data-testid="row-temperature"]'
        )
        temperature = (
            temperature_element.get_text(strip=True)
            if temperature_element else None
        )
        if temperature:
            temperature = int(temperature.replace("°", ""))

        # Real feel
        feels_element = row.select_one(
            '[data-testid="row-feels-like"]'
        )
        feels_text = (
            feels_element.get_text(" ", strip=True)
            if feels_element else ""
        )

        # Extract the number from "Feels 21"
        feels_match = re.search(r'(\d+)', feels_text)
        real_feels = (
            int(feels_match.group(1))
            if feels_match else None
        )

        # Precipitation probability
        pop_element = row.select_one(
            '[data-testid="collapsed-row-pop-info"]'
        )

        if pop_element:
            pop_text = pop_element.get_text(" ", strip=True)
            pop_match = re.search(r'(\d+)\s*%', pop_text)

            precipitation = (
                int(pop_match.group(1))
                if pop_match else None
            )
        else:
            precipitation = None

        weather_record.append({
            "Location": "Mthatha",
            "Time_of_day": time,
            "Temperature": temperature,
            "Real_feels": real_feels,
            "Precipitation_prob": precipitation
        })

    return weather_record

weather_data = get_value(soup)
df =pd.DataFrame(weather_data)
df["Feels_difference"] = df["Temperature"] - df["Real_feels"]
print(df.head())

df.to_csv("weather-data.csv", index=False)
