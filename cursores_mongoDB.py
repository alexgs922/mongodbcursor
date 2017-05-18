# -*- coding: utf-8 -*-
from pymongo import MongoClient


# Conexión con la base de datos llamada "liga" y con la coleccion "premier"
client = MongoClient()
db = client.liga
premierCollection = db.premier
santanderCollection = db.santander

#creación del cursor
cursor = premierCollection.find({"equipo": "Chelsea"})
cursor2 = santanderCollection.find({"equipo":"Real Madrid"})

#Borra los centrocampistas del Chelsea
def getRemoveMED():
    for c in cursor:
        if c['posicion'] == "MED":
            premierCollection.remove(c)

#actualizar la edad
def setUpdateAge():
    for c in cursor2:
        if c['edad'] == "25":
            santanderCollection.update_many(c,{"$set": {"edad":31}})

#insertar nuevo jugador
def getInsertNewPlayer():
    santanderCollection.insert({
        "jugador" : 'A.Gallego',
        "edad" : '25',
        "estatura": '1.80',
        "equipo" : 'Real Madrid',
        "posicion" : 'DEL'
    })

if __name__ == '__main__':
   #getRemoveMED()
   #setUpdateAge()
   getInsertNewPlayer()

