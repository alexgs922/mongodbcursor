import pymongo
from bokeh.plotting import figure, show, output_file
from pymongo import MongoClient

from bokeh.charts import Bar, output_file, show





client =MongoClient()

output_file("prueba.html")

db = client.liga
premier = db.premier
santander = db.santander


cursorPremier = premier.find()

equiposPremier = []
jugadoresPremier = []
dicPremier = dict()

def getNumJugadPremier():
    for c in cursorPremier:
        if c['equipo'] not in equiposPremier:
            equiposPremier.append(c['equipo'])

    for e in equiposPremier:
        x = premier.find({'equipo':str(e)}).count()
        jugadoresPremier.append(x)



    dot = figure(title="Numero de jugadores por equipo (Premier League)", tools="", toolbar_location=None,
              y_range=equiposPremier,x_range=[0,50])

    dot.segment(0, equiposPremier, jugadoresPremier, equiposPremier, line_width=2, line_color="green",)
    dot.circle(jugadoresPremier, equiposPremier, size=15, fill_color="orange", line_color="green", line_width=3, )

    output_file("numJugadoresXEquipo(Premier).html")
    show(dot)


cursorSantander = santander.find()

posicionesSantander = []
jugadoresSantander = []
dicSantander = dict()

def getNumJugadSantander():
    for c in cursorSantander:
        if c['posicion'] not in posicionesSantander:
            posicionesSantander.append(c['posicion'])

    for e in posicionesSantander:
        x = santander.find({'posicion':str(e.encode('utf-8'))}).count()
        jugadoresSantander.append(x)


    dot = figure(title="Numero de jugadores por posicion (Liga Santander)", tools="", toolbar_location=None,
              y_range=[0,500],x_range=posicionesSantander)
    dot.segment(posicionesSantander, 0,  posicionesSantander, jugadoresSantander, line_width=10, line_color="purple",)
    dot.circle(posicionesSantander, jugadoresSantander, size=15, fill_color="orange", line_color="purple", line_width=3, )


    output_file("numJugadoresXEquipo(Santander).html")
    show(dot)

if __name__ == '__main__':
   getNumJugadPremier()
   getNumJugadSantander()




