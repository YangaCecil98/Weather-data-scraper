import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.theweathernetwork.com/en/city/za/oos-kaap/umtata/7-days'
response = requests.get(url)
print(f"status_code: {response.status_code}")
print()
soup = BeautifulSoup(response.text, 'html.parser')

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

print("time_of_day:", len(time_of_day))
print("reel_feels:", len(reel_feels))
print("temperature:", len(temperature))
print()

weather_record = {"Location":"Mthatha",
                  "Time_of_day":time_of_day,
                  "Temperature":temperature,
                  "Reel_feels":reel_feels
}

df = pd.DataFrame(weather_record)
df["Feels_difference"] = df["Temperature"].astype(int) - df["Reel_feels"].astype(int)
print(df)
