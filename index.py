from flask import Flask, render_template, request, jsonify
import os
# from amazon_credentials import access_key_id, secret_access_key, Region
if os.path.isfile("amazon_credentials.py"):
    from amazon_credentials import access_key_id, secret_access_key, Region
else:
    access_key_id="access_key_id"
    secret_access_key="secret_access_key"
    Region="Region"
import csv
import time
import threading
import datetime
import requests
import boto3
# from botocore.exceptions import BotoCoreError, NoCredentialsError

app = Flask(__name__)

API_URL = "https://api.open-meteo.com/v1/forecast"
LATITUDE = 50.93
LONGITUDE = 6.95
INTERVAL = 24 * 60 * 60  # Interval in seconds (e.g., 3600 for 1 hour)
amazon_flag = False
s3 = boto3.client('s3', aws_access_key_id=access_key_id,
                  aws_secret_access_key=secret_access_key,
                  region_name=Region)

try:
    response = s3.list_buckets()
    print("Connection to S3 successful. Buckets:")
    for bucket in response['Buckets']:
        a=bucket['Name']
        print("Bucket Name")
    amazon_flag = True
except Exception as e:
    amazon_flag = False
    print("An error occurred:", str(e))


def get_current_weather_data():
    print("INTERVAL:" + str(INTERVAL))
    # url = f"{API_URL}?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true&hourly=rain,showers,
    # visibility," \ f"temperature_2m&timezone=Europe/Berlin&forecast_days=1"
    url = f"{API_URL}?latitude={LATITUDE}&longitude={LONGITUDE}"
    params = {
        "current_weather": "true",
        "hourly": "rain,showers,visibility,temperature_2m",
        "timezone": "Europe/Berlin",
        "forecast_days": 1
    }
    print(url)
    response = requests.get(url, params)
    print(response)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve current weather data.")
        return None


def write_to_csv(data):
    if data:
        current_timestamp = time.time()
        filename = "csv/cologne_current_weather_" + str(current_timestamp) + ".csv"
        print(filename)
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            current_weather = data['current_weather']
            print(current_weather['time'])
            for key in data:
                if type(data[key]) is not dict:
                    writer.writerow([key, data[key]])
                else:
                    writer.writerow([key])
                    for values in data[key]:
                        if type(data[key][values]) is not list:
                            writer.writerow([values, data[key][values]])
                    if key == "hourly":
                        keys = data[key].keys()
                        keys = list(keys)
                        print()
                        print(keys)
                        for i in range(len(data[key][keys[0]])):
                            writer.writerow(
                                [data[key][keys[0]][i], data[key][keys[1]][i], data[key][keys[2]][i],
                                 data[key][keys[3]][i],
                                 data[key][keys[4]][i]])

            print(f"Current weather data successfully written to {filename}.")
        return filename
    else:
        print("No weather data available to write to CSV.")


def fetch_weather_data():
    global weather_data
    while True:
        current_weather_data = get_current_weather_data()
        if current_weather_data:
            current_datetime = datetime.datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            filename = write_to_csv(current_weather_data)
            bucket_name = "fraunhoferinterview"
            file_name = filename
            destination_folder = "data/" + filename
            if amazon_flag:
                s3.upload_file(file_name, bucket_name, destination_folder)
            else:
                current_weather_data['amazon_flag'] = amazon_flag
            print("**********************")
            print("INTERVAL" + str(INTERVAL))
            print("Uploaded to amazon aws")
            print("**********************")
            current_weather_data['last_update_time'] = formatted_datetime

            weather_data = current_weather_data
        time.sleep(INTERVAL)


@app.route('/', methods=['GET', 'POST'])
def index():
    print(weather_data)
    return render_template('index.html', weather_data=weather_data)


@app.route('/update_interval', methods=['GET'])
def update_interval():
    global INTERVAL  # Access the global variable
    interval_hour = int(request.args.get('intervalHour'))
    interval_minutes = int(request.args.get('intervalMinutes'))
    INTERVAL = (interval_hour * 60 + interval_minutes) * 60  # Convert hours and minutes to seconds

    return jsonify({'status': 'success'})


if __name__ == '__main__':
    weather_thread = threading.Thread(target=fetch_weather_data)
    weather_thread.daemon = True
    weather_thread.start()
    app.run(host='0.0.0.0', port=5000)
