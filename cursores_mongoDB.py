# -*- coding: utf-8 -*-
from pymongo import MongoClient


# Conexión con la base de datos
client = MongoClient()
db = client.liga
premierCollection = db.premier


cursor = premierCollection.find({"equipo": "Chelsea"})

for c in cursor:
    print c['jugador']