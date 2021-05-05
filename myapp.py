import json
import web
import requests
import os
from _datetime import datetime
from http import cookies
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

API_KEY = os.environ.get("KEY")
API_TRANS_KEY = os.environ.get("API_TRANS_KEY")

# Generating routes
urls = (
    '/', 'accueil',
    '/(.*)', 'meteo',
)

app = web.application(urls, globals())
stockage = cookies.SimpleCookie()

class meteo:
    def GET(self, city):
        web.header('charset', 'UTF-8')
        web.header('Content-Type', 'application/json')
        if city.isnumeric():
            url_api = "http://api.openweathermap.org/data/2.5/weather?zip=" + city + ",fr&appid=" + API_KEY
        else:
            url_api = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + API_KEY
        conv_K_to_C = 273.15
        if city in stockage:
            contenu = stockage[city].value
            #test = dict(contenu)
            #toto = test['weather']['main']
            #cookies = {}
            #for key, morsel in stockage.items():
            #    cookies[key] = morsel.value
            # test = cookies[city]['weather']['main']
            #print('tes la')
            #return test

        else:
            response = requests.get(url_api)
            contenu = response.json()
            ville = contenu['name']
            temp_actu = contenu['main']['temp'] - conv_K_to_C
            temp_min = contenu['main']['temp_min'] - conv_K_to_C
            temp_max = contenu['main']['temp_max'] - conv_K_to_C
            temp_ressenti = contenu['main']['feels_like'] - conv_K_to_C
            humidity = contenu['main']['humidity']
            meteo_actu = contenu['weather'][0]['main']
            meteo_desc = contenu['weather'][0]['description']
            url = "https://systran-systran-platform-for-language-processing-v1.p.rapidapi.com/translation/text/translate"
            querystring = {"source": "en", "target": "fr", "input": meteo_actu}
            querystring2 = {"source": "en", "target": "fr", "input": meteo_desc}
            headers = {'x-rapidapi-key': API_TRANS_KEY,
                       'x-rapidapi-host': "systran-systran-platform-for-language-processing-v1.p.rapidapi.com"}
            response_translate_meteo_actu = requests.request("GET", url, headers=headers, params=querystring)
            response_translate_meteo_desc = requests.request("GET", url, headers=headers, params=querystring2)
            translate_meteo_actu = response_translate_meteo_actu.json()
            translate_meteo_desc = response_translate_meteo_desc.json()
            meteo_actu = translate_meteo_actu['outputs'][0]['output']
            meteo_desc = translate_meteo_desc['outputs'][0]['output']
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            contenu['time'] = dt_string
            stockage[city] = contenu

        fichier = open("histo.txt", "a")
        fichier.write(
            "=========================================== " + "\n" + "La ville choisi est : " + ville + "\n" + "La météo actuelle est : " + meteo_actu + \
            ", petite description : " + meteo_desc + "\n" + "Le taux d'humidité est de : " + str(round(humidity)) + \
            "% " + "\n" + "La température actuelle est de : " + str(
                round(temp_actu)) + "°C " + "\n" + "La température minimale est de : " + str(round(temp_min)) + \
            "°C " + "\n" + "La température maximale est de : " + str(
                round(temp_max)) + "°C " + "\n" + "La température ressenti est de : " + str(
                round(temp_ressenti)) + "°C" + "\n" + "\n")
        fichier.close()

        jsonErwan = {
            'ville': ville,
            'temp actu': round(temp_actu),
            'temp min': round(temp_min),
            'temp max': round(temp_max),
            'météo(meteo)': meteo_actu,
        }
        return json.dumps(jsonErwan)

           #"<head><meta charset="'utf-8'"></head>La ville choisi est : " + ville + "<br>" + 'La météo actuelle est : ' + meteo_actu + ", petite description : " + meteo_desc + "<br>" + "Le taux d'humidité est de : " + str(round(humidity)) + "% <br>" + "La température actuelle est de : " + str(round(temp_actu)) + "°C <br>" + "La température minimale est de : " + str(round(temp_min)) + "°C <br>" + "La température maximale est de : " + str(round(temp_max)) + "°C <br>" + "La température ressenti est de : " + str(round(temp_ressenti)) + "°C" +  "<br><br><br><br><br><br><br><br><br><br><br> Regarde à l'endroit ou tu as mis mon dossier, un fichier a été crée avec l'hitorique de tes recherches !"

class accueil:
    def GET(self):
        return "Hello, met une ville dans l'url pour savoir la météo de cette ville !"

if __name__ == "__main__":
    app.run()