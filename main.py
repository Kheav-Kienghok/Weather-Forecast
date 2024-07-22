from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def get_weather_data(location):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    url = f'https://www.google.com/search?q=weather+in+{location}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        datetimes = soup.find('div', attrs={'id': 'wob_dts'}).text[-8:]
        status = soup.find('span', attrs={'id': 'wob_dc'}).text
        temp = soup.find('span', attrs={'id': 'wob_tm'}).text
        wind = soup.find('span', attrs={'id': 'wob_ws'}).text
        humidity = soup.find('span', attrs={'id': 'wob_hm'}).text
        wind_per_hr = int(humidity[:2]) / (100 * int(wind[:2]))

        data = {
            'location': location.title(),
            'hour': datetimes,
            'temperature': temp,
            'weather_status': status,
            'wind': wind,
            'humidity': humidity, 
            'wind_per_hr': f"{wind_per_hr:.2f}"
        }
    
        return data

    except ZeroDivisionError:
        wind_per_hr = 'N/A'
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None


def weather_icon_url(status):
    icons = {
        'Clear': 'https://openweathermap.org/img/wn/01d.png',
        'Cloudy': 'https://openweathermap.org/img/wn/02d.png',
        'Rain': 'https://openweathermap.org/img/wn/10d.png',
        'Storm': 'https://openweathermap.org/img/wn/11d.png',
        'Snow': 'https://openweathermap.org/img/wn/13d.png',
        'Fog': 'https://openweathermap.org/img/wn/50d.png',
        'Drizzle': 'https://openweathermap.org/img/wn/09d.png',
        'Thunderstorm': 'https://openweathermap.org/img/wn/11d.png'
    }
    return icons.get(status, 'https://openweathermap.org/img/wn/50d.png')  

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        location = request.form.get('location')
        weather_data = get_weather_data(location)
    
    return render_template('index.html', weather_data=weather_data, weather_icon_url=weather_icon_url)
    
if __name__ == '__main__':
    app.run(debug=True)