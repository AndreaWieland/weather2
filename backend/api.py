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
with open("./auth.json", "r") as read_file:
    auth = json.load(read_file)
geoKey = auth['here_key']
weatherKey = auth['weather_key']


@app.route('/', methods=['GET'])
def api_id():
    #for later: return different content for command line!
    #if 'curl' in str(request.user_agent):
    #    return(str(request.user_agent))
    if 'location' in request.args or ('latitude' in request.args and 'longitude' in request.args):
        #using lat and long from html geolocation api
        if 'latitude' in request.args:
            lat = request.args['latitude']
            lon = request.args['longitude']
        #translating a user input complete or partial address to lat and long
        if 'location' in request.args:
            loc = request.args['location']
            #call location api
            geoReq = requests.get(f'https://geocode.search.hereapi.com/v1/geocode?q={loc}&apiKey={geoKey}')
            geo = geoReq.json()
            
            if len(geo['items']) == 0:
                locationError = {
                    'status':'NF',
                    'message': 'Location not found. Try another query'
                }
                return jsonify(locationError)
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



app.run(host='0.0.0.0',port=5000)
