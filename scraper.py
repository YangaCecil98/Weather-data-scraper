#Importing necessary packages/libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.theweathernetwork.com/en/city/za/oos-kaap/umtata/7-days'
#HTTP GET() Request from a server/db
response = requests.get(url)
#Status Request
print(f"status_code: {response.status_code}")
print()
soup = BeautifulSoup(response.text, 'html.parser')
#Value extracting function from the source code
def get_value(soup, testid, remove=None):

    elements = soup.select(f'[data-testid = "{testid}"]')
    values = [
        element.get_text(strip=True)
        for element in elements
    ]

    if remove:
        values = [value.replace(remove, "") for value in values]

    return values

time_of_day =get_value(soup,"row-date-or-time")
reel_feels =get_value(soup,"row-feels-like", remove="Feels")
temperature =get_value(soup, "row-temperature", remove ="°")
precipitation_prob =get_value(soup, "collapsed-row-pop-info")

print("time_of_day_values:", len(time_of_day))
print("reel_feels_values:", len(reel_feels))
print("temperature_values:", len(temperature))
print()

weather_record = {"Location":"Mthatha",
                  "Time_of_day":time_of_day,
                  "Temperature":temperature,
                  "Reel_feels":reel_feels
}

df = pd.DataFrame(weather_record)
df["Feels_difference"] = df["Temperature"].astype(int) - df["Reel_feels"].astype(int)
print(df)

df.to_csv("weather-data.csv", index=False)
