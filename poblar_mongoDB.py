# -*- coding: utf-8 -*-
import requests
import htmlmin
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient

# Conexión con la base de datos
client = MongoClient()
db = client.liga
premierCollection = db.premier

def getDataPlayers():
    url = "http://fantasy.premierleague.com/player-list/"
    r = requests.get(url)

    ##Minify html - quitar espacios en blanco
    rmin = htmlmin.minify(r.text, remove_empty_space=True)

    ##Soup - scrapping
    soup = BeautifulSoup(rmin, "html.parser")

    ##Obtenemos tipos de jugadores y nos quedamos con la primera letra para crear un identificador
    # Goalkeepers - Porteros
    # Defenders - Defensas
    # Midfielders - Mediocentros
    # Forwards - Delanteros/Atacantes

    tipo_jugador = soup.find_all('h2')

    i = 0
    for tipo in tipo_jugador:
        tipo_jugador[i] = tipo.string[0]
        i = i + 1


    ## Obtenemos todas las tablas como array
    jugadores_tables = soup.find_all("table")

    ## Encontramos el nombre de las columnas de la tabla
    column_name = soup.table.find_all('th')

    ## Obtenemos el texto para el array
    i = 0
    for name in column_name:
        column_name[i] = name.string
        i = i + 1


    ## Añadimos posicion position
    column_name.append('Position')


    jugadores_dict = []

    ptype = [u'G',u'D',u'M',u'F']

    j=0
    for t in jugadores_tables:
        tipo_num =  int(j/2)
        j=j+1
        datos = t.find_all("td")

        for p in range (0,len(datos)/4):
            datos[4*p].string = datos[4*p].string.encode('ascii', 'replace')
            dict_entry = {"extractdate":str(datetime.today()),
                          "jugador": datos[4*p].string,
                          "equipo": datos[4*p+1].string,
                          "rawpoints": int(datos[4*p+2].string),
                          "coste": float(datos[4*p+3].string[1:]),
                          "posicion": ptype[tipo_num]
                          }
            jugadores_dict.append(dict_entry)

    return jugadores_dict


def insertarData():

    data = getDataPlayers()

    bd = premierCollection.find()

    if bd.count() == 0:
        for d in data:
            premierCollection.insert({
                "extractdate": d['extractdate'],
                "jugador": d['jugador'],
                "equipo": d['equipo'],
                "rawpoints": d['rawpoints'],
                "coste": d['coste'],
                "posicion": d['posicion']
            })
        print "Insertado correctamente "
    else:
        premierCollection.remove()
        for d in data:
            premierCollection.insert({
                "extractdate": d['extractdate'],
                "jugador": d['jugador'],
                "equipo": d['equipo'],
                "rawpoints": d['rawpoints'],
                "coste": d['coste'],
                "posicion": d['posicion']
            })
        print "Insertado correctamente "

client.close()


if __name__ == '__main__':
    insertarData()