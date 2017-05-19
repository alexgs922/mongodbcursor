# -*- coding: utf-8 -*-

from bokeh.plotting import figure, show, output_file
from pymongo import MongoClient
from bokeh.charts import Bar, output_file, show

# Conexión con la base de datos llamada "liga" y con la coleccion "premier"
client =MongoClient()
db = client.liga
premier = db.premier
santander = db.santander


# Cursor y variables para liga Premier
cursorPremier = premier.find()

equiposPremier = []
jugadoresPremier = []
dicPremier = dict()


# Cursor y variables para liga Santander
cursorSantander = santander.find()

posicionesSantander = []
jugadoresSantander = []
dicSantander = dict()


def get_num_jugadores_premier():

    title = "Numero de jugadores por equipo de la Premier League"


    for c in cursorPremier:
        if c['equipo'] not in equiposPremier:
            equiposPremier.append(c['equipo'])


    for e in equiposPremier:
        x = premier.find({'equipo':str(e)}).count()
        jugadoresPremier.append(x)

    output_file("numJugadoresEquipo(Premier).html", title="grafica_premier.py")

    dot = figure(title=title, tools="pan,wheel_zoom,reset,save", y_range=equiposPremier, x_range=[0,50], plot_width=1200, plot_height=600, x_axis_label='Número de jugadores', y_axis_label='Equipos')

    dot.segment(0, equiposPremier, jugadoresPremier, equiposPremier, line_width=10, line_color="green")
    dot.circle(jugadoresPremier, equiposPremier, size=10, fill_color="orange", line_color="green", line_width=3 )

    show(dot)
    client.close()


def get_num_jugadores_santander():

    title = "Numero de jugadores por posicion de la Liga Santander"

    for c in cursorSantander:
        if c['posicion'] not in posicionesSantander:
            posicionesSantander.append(c['posicion'])

    for e in posicionesSantander:
        x = santander.find({'posicion':str(e.encode('utf-8'))}).count()
        jugadoresSantander.append(x)

    output_file("numJugadoresEquipo(Santander).html", title="grafica_santander.py")

    dot = figure(title=title, tools="pan,wheel_zoom,reset,save", y_range=[0,500], x_range=posicionesSantander, plot_width=600, plot_height=600, x_axis_label='Posiciones', y_axis_label='Número de jugadores')

    dot.segment(posicionesSantander, 0,  posicionesSantander, jugadoresSantander, line_width=10, line_color="purple")
    dot.circle(posicionesSantander, jugadoresSantander, size=15, fill_color="orange", line_color="purple", line_width=3 )

    show(dot)

    client.close()


if __name__ == '__main__':
   get_num_jugadores_premier()
   get_num_jugadores_santander()




