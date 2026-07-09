import joblib
import pandas as pd
import requests
import datetime

# ============================================================
# 1. LOCATION
# ============================================================

lat = 10.728422
lon = 79.020276

print("Latitude:", lat)
print("Longitude:", lon)

try:
    loc_data = requests.get("http://ip-api.com/json/", timeout=5).json()
    print("City:", loc_data.get("city", "Unknown"))
except:
    print("City: Unknown")

# ============================================================
# 2. WEATHER (OpenWeather)
# ============================================================

API_KEY = "e59ee45fa8393fc8b5ec7bc58d1f5215"

weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

response = requests.get(weather_url, timeout=10)

if response.status_code != 200:
    raise Exception("Weather API failed")

weather = response.json()

temperature = weather["main"]["temp"]
humidity = weather["main"]["humidity"]

print("Temperature:", temperature)
print("Humidity:", humidity)

# ============================================================
# 3. RAINFALL (NASA POWER)
# ============================================================

today = datetime.date.today()
year = today.year - 1

start_month = today.month
end_month = today.month + 2

if end_month > 12:
    end_month -= 12
    end_year = year + 1
else:
    end_year = year

start_date = datetime.date(year, start_month, 1)

if end_month == 12:
    end_date = datetime.date(end_year + 1, 1, 1) - datetime.timedelta(days=1)
else:
    end_date = datetime.date(end_year, end_month + 1, 1) - datetime.timedelta(days=1)

start = start_date.strftime("%Y%m%d")
end = end_date.strftime("%Y%m%d")

nasa_url = (
    "https://power.larc.nasa.gov/api/temporal/daily/point?"
    f"parameters=PRECTOTCORR"
    f"&community=AG"
    f"&latitude={lat}"
    f"&longitude={lon}"
    f"&start={start}"
    f"&end={end}"
    f"&format=JSON"
)

try:
    nasa_data = requests.get(nasa_url, timeout=20).json()
    rainfall_values = nasa_data["properties"]["parameter"]["PRECTOTCORR"].values()
    rainfall = sum([v for v in rainfall_values if v > -999])
except:
    rainfall = 0

print("3-Month Rainfall:", round(rainfall, 2), "mm")

# ============================================================
# 4. LOAD MODEL
# ============================================================

model_data = joblib.load("crop_model_all.pkl")

model = model_data["voting_model"]   # or stacking_model
le = model_data["label_encoder"]









# ============================================================
# 5. INPUT
# ============================================================



import requests
import pandas as pd

CHANNEL_ID = "3328309"
READ_API_KEY = "HUFCQ9NJMNTBJC6I"

# Fetch last 10 entries instead of 1
url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=10"

response = requests.get(url)
data = response.json()

feeds = data['feeds']

# Function to get last non-zero value
def get_valid_value(field_name):
    for entry in reversed(feeds):  # check latest → older
        value = entry.get(field_name)
        if value is not None:
            value = float(value)
            if value != 0:
                return value
    return 0  # fallback if all are zero

# Extract values safely
Moisture = get_valid_value('field1')
Temp     = get_valid_value('field2')
ph       = get_valid_value('field3')
EC       = get_valid_value('field4')
N        = get_valid_value('field5')
P        = get_valid_value('field6')
K        = get_valid_value('field7')


print("Received Data:", N, P, K, Temp, Moisture, ph)

# Your model input
columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

input_df = pd.DataFrame([[N, P, K, temperature, humidity, ph, rainfall]],
                        columns=columns)




"""
# ============================================================
# 5. INPUT
# ============================================================

columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

import requests
import pandas as pd

CHANNEL_ID = "3328309"
READ_API_KEY = "HUFCQ9NJMNTBJC6I"

url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=1"

response = requests.get(url)
data = response.json()

latest = data['feeds'][0]

# Extract values
Moisture = float(latest['field1'])
Temp = float(latest['field2'])
ph = float(latest['field3'])
EC = float(latest['field4'])
N = float(latest['field5'])
P = float(latest['field6'])
K = float(latest['field7'])

print("Received Data:", N, P, K, temperature, humidity, ph, rainfall)

input_df = pd.DataFrame([[N, P, K, temperature, humidity, ph, rainfall]],
                        columns=columns)

"""


# ============================================================
# 5. INPUT
# ============================================================
"""
import random

columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

N = random.randint(0, 140)
P = random.randint(5, 145)
K = random.randint(5, 205)
ph = round(random.uniform(5.0, 7.5), 2)

input_df = pd.DataFrame([[N, P, K, temperature, humidity, ph, rainfall]],
                        columns=columns)

"""

# ============================================================
# 6. PREDICT
# ============================================================

prediction = model.predict(input_df)
crop = le.inverse_transform(prediction)

print("\n===== INPUT =====")
print(input_df.to_string(index=False))

print("\n===== RESULT =====")
print("Recommended Crop:", crop[0])