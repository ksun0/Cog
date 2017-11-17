import pyowm
from Dashboard.Extensions.ExtensionLib.QAFramework import *
from .models import *
import pdb

extension_id = 'a874e455-c381-497c-b332-8b3c0ca91fae' # Used to identify this extension's events

def main():
    request = yield
    owm = pyowm.OWM('548f2db5a3c699fb2c06d8aae9be495f')
    observation = owm.weather_at_place('andover,ma')
    w = observation.get_weather()
    temperature = str(w.get_temperature('fahrenheit'))
    description = str(w.get_status())
    # print(description)
    html = 'Temperature: ' + temperature + ' | Description: ' + description
    WeatherModel.objects.filter(extension_id=extension_id).delete()
    weather_object = WeatherModel.objects.create(temperature=temperature, description=description, extension_id=extension_id)
    weather_object.save()
    yield ask(html, 'html', request)
