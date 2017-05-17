import pymongo
from bokeh.layouts import row
from bokeh.plotting import figure, show, output_file
from pymongo import MongoClient





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

equiposSantander = []
jugadoresSantander = []
dicSantander = dict()

def getNumJugadSantander():
    for c in cursorSantander:
        if c['equipo'] not in equiposSantander:
            equiposSantander.append(c['equipo'])

    for e in equiposSantander:
        x = santander.find({'equipo':str(e.encode('utf-8'))}).count()
        jugadoresSantander.append(x)



    dot = figure(title="Numero de jugadores por equipo (Liga Santander)", tools="", toolbar_location=None,
              y_range=equiposSantander,x_range=[0,50])

    dot.segment(0, equiposSantander, jugadoresSantander, equiposSantander, line_width=2, line_color="green",)
    dot.circle(jugadoresSantander, equiposSantander, size=15, fill_color="orange", line_color="green", line_width=3, )

    output_file("numJugadoresXEquipo(Santander).html")
    show(dot)

if __name__ == '__main__':
   getNumJugadPremier()
   getNumJugadSantander()




