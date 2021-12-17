import requests
import urllib.request
import urllib.parse
import http.client
import json

# Links
planets_link = 'https://swapi.dev/api/planets'
wookie_link = 'https://swapi.dev/api/films/?format=wookiee'
startship_link = 'https://swapi.dev/api/starships'

# Requests
planets = requests.get(planets_link)
wookie = requests.get(wookie_link)
startship = requests.get(startship_link)

# Convert to json
json_planets = planets.json()
json_wookie = wookie.content
json_startship = startship.json()

# Dictionaries
dict_planets = {}
dict_wookie = {}
dict_startship = {}

# Filters
cont = 1
for x in range(json_planets['count']):

    planets = requests.get(planets_link + '/{}'.format(cont))
    json_planets = planets.json()
    if json_planets['climate'] == 'arid':
        dict_planets[cont] = json_planets
    cont += 1

cont = 2
aux = 0

for x in range(json_startship['count']):

    startship = requests.get(startship_link + '/{}'.format(cont))
    if startship.status_code != 200:
        pass
    else:
        json_startship = startship.json()
        aux_ = json_startship['length']
        new = aux_.replace(",","")
        if float(new) > aux:
            dict_startship[0] = json_startship
            aux = float(new)
    cont += 1

dict_wookie = json_wookie

# Results
print('Planetas con clima arido')
print('|       |       |       |')
print('v       v       v       v')
print(dict_planets)
print('')
print('Cantidad de wookies en la pelicula 6 SW = {}'.format(dict_wookie))
print('La nave mas grande de star wars mide : {} '.format(dict_startship[0]['length']))
print('y se llama : {} '.format(dict_startship[0]['name']))
