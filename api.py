#TO DO:
# error code handling from both here and openweather
# detecting if latitude and longitude were sent from the browser and using that
# if an address is not found handling


#flask for routes, requests and json for external API calls, parse for url encoding
import requests, json, urllib.parse, datetime, flask
from flask import request, jsonify #sending back json to GET requests
from functions import * #some small reusable functions
from flask_cors import CORS

#initiate flask app
app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True


#get auth keys for HERE and openweather
with open("auth.json", "r") as read_file:
    auth = json.load(read_file)
geoKey = auth['here_key']
weatherKey = auth['weather_key']


@app.route('/weather_api', methods=['GET'])
def api_id():
    if 'location' in request.args:
        #get address from params
        loc = request.args['location']
        #turn it back to url encoding. note: is there a way to keep this raw in flask?
        urlLocation = urllib.parse.quote(loc)
        #call location api
        geoReq = requests.get(f'https://geocode.search.hereapi.com/v1/geocode?q={urlLocation}&apiKey={geoKey}')
        geo = geoReq.json()

        #extracting latitude and longitude 
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