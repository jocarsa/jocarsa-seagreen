import matplotlib.pyplot as plt
import os
from funciones.ayudante import get_filename_without_extension

def distinctIPs(ruta):
    archivo = open(ruta, 'r')
    lineas = archivo.readlines()
    archivo.close()
    diccionario = {}

    for linea in lineas:
        ip = linea.split(' ')[0]
        if ip not in diccionario:
            diccionario[ip] = 1
        else:
            diccionario[ip] += 1

    # Ordenar las IPs por número de accesos en orden descendente y limitar a 20
    sorted_ips = sorted(diccionario.items(), key=lambda x: x[1], reverse=True)[:20]
    ips = [item[0] for item in sorted_ips]
    counts = [item[1] for item in sorted_ips]

    # Crear el gráfico
    plt.figure(figsize=(12, 8))
    plt.bar(ips, counts)
    plt.xlabel("Dirección IP")
    plt.ylabel("Número de accesos")
    plt.title("Top 20 Accesos por IP")
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Guardar el gráfico
    nombre_archivo = get_filename_without_extension(ruta)
    os.makedirs("imagenes", exist_ok=True)
    virtual_host = nombre_archivo.split("-")[0]
    os.makedirs("imagenes/"+virtual_host, exist_ok=True)
    plt.savefig(f"imagenes/{virtual_host}/{nombre_archivo}_distintasips.png")
    plt.close()
