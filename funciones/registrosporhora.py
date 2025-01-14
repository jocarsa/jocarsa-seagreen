import matplotlib.pyplot as plt
import os
from funciones.ayudante import get_filename_without_extension

def registrosPorHora(ruta): 
    archivo = open(ruta,'r')
    lineas = archivo.readlines()
    archivo.close()
    diccionario = {}

    for linea in lineas:
        inicio = linea.find('[')
        final = linea.find(']')
        tiempo = linea[inicio+1:final]
        partes = tiempo.split(':')
        hora = partes[1]
        if hora not in diccionario:
            diccionario[hora] = 1
        else:
            diccionario[hora] += 1
    
    horas = sorted(diccionario.keys())
    numero = [diccionario[hora] for hora in horas]

    plt.figure(figsize=(10, 6))
    plt.bar(horas, numero)
    plt.xlabel("Hora del día")
    plt.ylabel("Número de accesos")
    plt.title("Accesos por horas")
    plt.xticks(rotation=45)
    plt.tight_layout()
    nombre_archivo = get_filename_without_extension(ruta)
    os.makedirs("imagenes", exist_ok=True)
    plt.savefig("imagenes/"+nombre_archivo+".png")