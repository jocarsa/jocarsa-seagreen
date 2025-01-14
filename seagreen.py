from funciones.registrosporhora import registrosPorHora
import os

carpeta = "/var/log/apache2/"
for root, dirs, files in os.walk(carpeta):
    for file in files:
        if file.endswith('.log'):
            registrosPorHora(carpeta+file)
