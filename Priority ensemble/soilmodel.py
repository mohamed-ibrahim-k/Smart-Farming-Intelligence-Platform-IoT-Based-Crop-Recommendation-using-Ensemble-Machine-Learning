# ============================================================
#  PRIORITY-BASED CROP PREDICTION SYSTEM
# ============================================================

import joblib
import pandas as pd
import requests
import datetime

# ============================================================
# 1. LOAD MODEL
# ============================================================

model_data = joblib.load("crop_model_priority_final.pkl")

model = model_data["model"]
le = model_data["label_encoder"]
scaler = model_data["scaler"]
columns = model_data["columns"]

# ============================================================
# 2. TRANSFORM FUNCTION (SAME AS TRAINING)
# ============================================================

def transform_input(df):
    df = df[columns]

    X_scaled = scaler.transform(df)
    X_scaled = pd.DataFrame(X_scaled, columns=columns)

    # PRIORITY WEIGHTS (same as training)
    X_scaled['rainfall']   *= 1.8
    X_scaled['temperature']*= 1.5
    X_scaled[['N','P','K']] *= 1.2
    X_scaled['ph']         *= 1.0
    X_scaled['humidity']   *= 0.8

    return X_scaled

# ============================================================
# 3. LOCATION (SAFE)
# ============================================================

print("Fetching location...")

lat = 10.7287
lon = 79.0208

try:
    loc_data = requests.get("http://ip-api.com/json/", timeout=5).json()
    lat = loc_data.get("lat", 11.0)
    lon = loc_data.get("lon", 78.0)
    city = loc_data.get("city", "Unknown")

except:
    print("Using default location...")
    lat, lon = 10.7287, 79.0208


""" print("Latitude:", lat)
    print("Longitude:", lon)
    print("City:", city)"""

# ============================================================
# 4. WEATHER (OpenWeather)
# ============================================================

API_KEY = "e59ee45fa8393fc8b5ec7bc58d1f5215"

lat = 10.7287
lon = 79.0208
city = "Thirumalaisamudram"
print("Latitude:",lat)
print("Longitude:",lon)
print("City:",city)


try:
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    weather = requests.get(weather_url, timeout=5).json()

    temperature = weather["main"]["temp"]
    humidity = weather["main"]["humidity"]

except:
    print("Weather API failed, using default values")
    temperature = 30
    humidity = 60

print("Temperature:", temperature)
print("Humidity:", humidity)

# ============================================================
# 5. RAINFALL (NASA POWER)
# ============================================================

try:
    today = datetime.date.today()
    start = (today - datetime.timedelta(days=90)).strftime("%Y%m%d")
    end = today.strftime("%Y%m%d")

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

    nasa_data = requests.get(nasa_url, timeout=10).json()
    rainfall_values = nasa_data["properties"]["parameter"]["PRECTOTCORR"].values()

    rainfall = sum(v for v in rainfall_values if v > -999)

except:
    print("NASA API failed, using default rainfall")
    rainfall = 100

print("3-Month Rainfall:", round(rainfall, 2), "mm")

# ============================================================
# 6. SENSOR INPUT (ThingSpeak or manual)
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

print("Received Data:", N, P, K, ph)

# ============================================================
# 7. CREATE INPUT
# ============================================================

input_df = pd.DataFrame([[N, P, K, temperature, humidity, ph, rainfall]],
                        columns=columns)

# Apply transformation
input_processed = transform_input(input_df)

# ============================================================
# 8. PREDICTION
# ============================================================

prediction = model.predict(input_processed)
crop = le.inverse_transform(prediction)

print("\n===== INPUT =====")
print(input_df.to_string(index=False))

print("\n===== RESULT =====")
print("Recommended Crop:", crop[0])














# ============================================================
# 9. PROBABILITY (Top 5)
# ============================================================

proba = model.predict_proba(input_processed)
proba_df = pd.DataFrame(proba, columns=le.classes_)

print("\nTop 5 Probabilities:")
print(proba_df.T.sort_values(by=0, ascending=False).head(5))