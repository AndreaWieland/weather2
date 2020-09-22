import requests, json, urllib.parse, datetime
import flask
from flask import request, jsonify
from functions import *


#initiate flask app
app = flask.Flask(__name__)
app.config["DEBUG"] = True


#get auth keys
with open("auth.json", "r") as read_file:
    auth = json.load(read_file)
geoKey = auth['here_key']
weatherKey = auth['weather_key']


@app.route('/weather_api', methods=['GET'])
def api_id():
    if 'location' in request.args:
        #get address from params
        loc = request.args['location']
        #turn it back to url encoding. note: is there a way to keep the raw in flask?
        urlLocation = urllib.parse.quote(loc)
        #call location api
        geoReq = requests.get(f'https://geocode.search.hereapi.com/v1/geocode?q={urlLocation}&apiKey={geoKey}')
        #if the search comes up empty, the json is just an empty array. how to handle?
        geo = geoReq.json()

        lat = round(geo['items'][0]['position']['lat'],3)
        lon = round(geo['items'][0]['position']['lng'],3)

        req = requests.get(f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&appid={weatherKey}')

        res = req.json()

        forecastData = res['daily']
        forecasts = []
        for d in forecastData:
            dailytemps = list(d['temp'].values())
            forecast = {
                'conditions' : d['weather'][0]['description'].title(),
                'condition_id' : d['weather'][0]['id'],
                'cloud_cover' : d['clouds'],
                'humidity' : d['humidity'],
                'chance_of_precip' : d['pop'],
                'wind_metric' : round(d['wind_speed']),
                'wind_imperial' : round(d['wind_speed'] * 2.237),
                'high_far' : toFahrenheit(max(dailytemps)),
                'high_cel' : toCelsius(max(dailytemps)),
                'low_far' : toFahrenheit(min(dailytemps)),
                'low_cel' : toCelsius(min(dailytemps)),
                'day' : datetime.datetime.fromtimestamp(int(d['dt'] - res['timezone_offset'])).weekday()
            }
            forecasts.append(forecast)

        data = {
            'current' : {
                'fahrenheit_temp' : toFahrenheit(res['current']['temp']),
                'celsius_temp' : toCelsius(res['current']['temp']),
                'humidity' : res['current']['humidity'],
                'wind_metric' : round(res['current']['wind_speed']),
                'wind_imperial' : round(res['current']['wind_speed'] * 2.237),
                'conditions' : res['current']['weather'][0]['description'].title(),
                'condition_id' : res['current']['weather'][0]['id']
            },
            'forecasts' : forecasts
        }
        return(jsonify(data))
    else:
        return "No data available."


app.run()