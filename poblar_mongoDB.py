# -*- coding: utf-8 -*-
import json

import requests
import htmlmin
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient

# Conexión con la base de datos
client = MongoClient()
db = client.liga
premierCollection = db.premier
santanderCollection = db.santander

def getDataPlayersPremier():
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

    ptype = [u'POR',u'DEF',u'MED',u'DEL']

    j=0
    for t in jugadores_tables:
        tipo_num =  int(j/2)
        j=j+1
        datos = t.find_all("td")

        for p in range (0,len(datos)/4):
            datos[4*p].string = datos[4*p].string.encode('utf-8')
            dict_entry = {"extractdate":str(datetime.today()),
                          "jugador": datos[4*p].string,
                          "equipo": datos[4*p+1].string,
                          "rawpoints": int(datos[4*p+2].string),
                          "coste": float(datos[4*p+3].string[1:]),
                          "posicion": ptype[tipo_num]
                          }
            jugadores_dict.append(dict_entry)
    return jugadores_dict


def getDataPlayersSantander():
    ##peticion a la web
    url = "http://www.resultados-futbol.com/primera/grupo1/jugadores"
    r = requests.get(url)

    ##Minify html - quitar espacios en blanco
    rmin = htmlmin.minify(r.text, remove_empty_space=True)

    ##Soup - scrapping
    soup = BeautifulSoup(rmin, "html.parser")

    ##Obtenemos la tabla de jugadores como array
    jugadores_tables = soup.find_all('table', {'id': 'tabla1'})

    jugadores_dict = []


    for j in jugadores_tables:
        datos = j.find_all("tr")
        for d in datos:
            jugador = d.td.strong.string

            #edad jugador
            edad = d.td.find_next('td').string
            if edad is not None:
                edad2 = edad[:2]
            else:
                edad2 = ""

            #estatura jugador
            estatura = d.td.find_next('td').find_next('td').string
            if d.td.find_next('td').find_next('td').string is not None:
                estatura2 = estatura[:3]
            else:
                estatura2 = 0


            # posicion de jugador str(.encode('iso-8859-1'))
            posicion = d.find('td',{'class':'pos1'}).string

            # Equipo del jugador
            equipo = jugador.parent.parent.parent.parent.parent.parent.parent.parent.find_next('span').find_next('span').img['alt']

            # Diccionario de entrada
            dic_in = {"jugador": jugador.replace(". ", "."),
                      "edad":edad2,
                      "estatura":str(float(estatura2)*0.01)[:4],
                      "posicion": posicion,
                      "equipo": equipo,
                      }

            # array de jugadores
            jugadores_dict.append(dic_in)



    return jugadores_dict




def insertarData():
    data = getDataPlayersPremier()
    data1 = getDataPlayersSantander()
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
    print "Insertado correctamente: premier league"
    santanderCollection.remove()
    for d in data1:
        santanderCollection.insert({
            "jugador": str(d['jugador'].encode('iso-8859-1')),
            "edad":d['edad'],
            "estatura":d['estatura'],
            "posicion": d['posicion'],
            "equipo": str(d['equipo'].encode('iso-8859-1'))
        })
    print "Insertado correctamente: liga santander"


client.close()


if __name__ == '__main__':
   insertarData()