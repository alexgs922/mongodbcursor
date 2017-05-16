import requests
import htmlmin
from bs4 import BeautifulSoup
from pymongo import MongoClient

def getDataPlayers():
    ##peticion a la web
    url ="http://www.resultados-futbol.com/primera/grupo1/jugadores"
    req = requests.get(url)


    #Minify html - quitar espacios en blanco
    rmin = htmlmin.minify(req.text, "html5lib",remove_empty_space=True)

    ##Soup - scrapping
    soup = BeautifulSoup(rmin, "html.parser")


    ##Obtenemos la tabla de jugadores como array
    jugadores_tables = soup.find_all('table',{'id':'tabla1'})

    jugadores_dict = []

    for j in jugadores_tables:
        datos = j.find_all("tr")
        for f in datos:
            ##nombre de jugador
            jugador = f.find_next("td").find_next("strong").string

            #posicion de jugador
            posicion = f.find_next("td").find_next("td").find_next("td").find_next("td").find_next("td").string

            #Equipo del jugador
            equipo = jugador.parent.parent.parent.parent.parent.parent.parent.parent.find_next('span').find_next('span').getText()
            print(equipo)

            #Diccionario de entrada
            dic_in = {"jugador" : jugador,
                      "posicion" : posicion,
                      "equipo" : equipo,
                      }

            #array de jugadores
            jugadores_dict.append(dic_in)

    return jugadores_dict

print(getDataPlayers())

def insertarData():
    client = MongoClient()
    db = client.liga
    santanderCollection = db.santander

    data = getDataPlayers()

    for d in data:
        santanderCollection.insert({
            "jugador": d['jugador'],
            "equipo": d['equipo'],
            "posicion": d['posicion'],
            #"puntos":d['rawpoints'],
            #"coste":d['coste'],
        })

    print "Insertado correctamente"

if __name__ == '__main__':
    insertarData()
