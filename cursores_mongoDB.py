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

#
#
#   METODOS CRUD SIMPLES
#
#

# Insertar nuevo jugador
def insert_new_player():
    santanderCollection.insert({
        "jugador" : 'A.Gallego',
        "edad" : '25',
        "estatura": '1.80',
        "equipo" : 'Real Madrid',
        "posicion" : 'DEL'
    })
    print "Insertado correctamente"
    client.close()


# Borra los centrocampistas del Chelsea
def remove_med():
    for c in cursor:
        if c['posicion'] == "MED":
            premierCollection.remove(c)
    print "Borrado correctamente"
    client.close()


# Actualizar la edad
def update_age():
    for c in cursor2:
        if c['edad'] == "25":
            santanderCollection.update(c,{"$set": {"edad": 31}})
    print "Actualizado correctamente"
    client.close()



if __name__ == '__main__':
   insert_new_player()
   #remove_med()
   #update_age()

