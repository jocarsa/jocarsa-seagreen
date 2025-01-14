from funciones.registrosporhora import registrosPorHora
from funciones.distintasips import distinctIPs
from funciones.masfunciones import *
from funciones.paises import *
import os

carpeta = "/var/log/apache2/"
for root, dirs, files in os.walk(carpeta):
    for file in files:
        if file.endswith('.log'):
            registrosPorHora(carpeta+file)
            distinctIPs(carpeta+file)
            response_status_pie_chart(carpeta+file)
            operating_systems_pie_chart(carpeta+file)
            browsers_pie_chart(carpeta+file)
            robots_pie_chart(carpeta+file)
            countries_pie_chart(carpeta+file, "GeoLite2-Country.mmdb")
