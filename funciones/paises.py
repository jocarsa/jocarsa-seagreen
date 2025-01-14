# country_pie_chart.py

import matplotlib.pyplot as plt
import os
import re
import geoip2.database
import ipaddress
from funciones.ayudante import get_filename_without_extension

# Function to get country name from IP using GeoIP2
def get_country(ip, reader):
    """
    Retrieves the country name for a given IP address using the GeoIP2 reader.

    Args:
        ip (str): The IP address to lookup.
        reader (geoip2.database.Reader): An instance of the GeoIP2 reader.

    Returns:
        str: The country name if found, otherwise "Unknown", "Invalid IP", or an error message.
    """
    try:
        # geoip2 expects a string IP address
        response = reader.country(ip)
        return response.country.name
    except geoip2.errors.AddressNotFoundError:
        return "Unknown"
    except ipaddress.AddressValueError:
        return "Invalid IP"
    except Exception as e:
        return f"Error: {e}"

def countries_pie_chart(ruta, mmdb_path='GeoLite2-Country.mmdb'):
    """
    Generates a pie chart showing the distribution of accesses by country based on IP addresses.

    Args:
        ruta (str): Path to the Apache log file.
        mmdb_path (str): Path to the GeoLite2 Country MMDB database.
    """
    # Check if the log file exists
    if not os.path.isfile(ruta):
        print(f"Error: The log file {ruta} does not exist.")
        return

    # Initialize dictionary to count IP occurrences
    diccionario_ips = {}

    # Regular expression to parse the IP address from each log line
    # Adjust the regex based on your log file format
    # Example assumes IP is the first non-space string
    ip_pattern = re.compile(r'^(\S+)')

    # Read and parse the log file
    try:
        with open(ruta, 'r') as archivo:
            for linea in archivo:
                match = ip_pattern.match(linea)
                if match:
                    ip = match.group(1)
                    try:
                        # Validate IP format
                        ipaddress.IPv4Address(ip)
                        diccionario_ips[ip] = diccionario_ips.get(ip, 0) + 1
                    except ipaddress.AddressValueError:
                        # Skip lines with invalid IP addresses
                        continue
    except Exception as e:
        print(f"An error occurred while reading the log file: {e}")
        return

    if not diccionario_ips:
        print("No valid IP addresses found in the log file.")
        return

    # Initialize GeoIP2 reader
    try:
        reader = geoip2.database.Reader(mmdb_path)
    except FileNotFoundError:
        print(f"Error: The GeoLite2 database file {mmdb_path} does not exist.")
        return
    except Exception as e:
        print(f"An error occurred while opening the GeoLite2 database: {e}")
        return

    # Dictionary to hold country counts
    diccionario_paises = {}
    unknown_ips = []

    # Iterate over each IP and map to country
    for ip, count in diccionario_ips.items():
        country = get_country(ip, reader)
        if country not in ["Unknown", "Invalid IP"] and not country.startswith("Error"):
            diccionario_paises[country] = diccionario_paises.get(country, 0) + count
        else:
            unknown_ips.append(ip)

    # Close the GeoIP2 reader
    reader.close()

    if not diccionario_paises:
        print("No countries could be determined from the IP addresses.")
        return

    # Sort the countries by count in descending order
    ordenado_paises = dict(
        sorted(
            diccionario_paises.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )

    # Prepare data for pie chart
    labels = list(ordenado_paises.keys())
    sizes = list(ordenado_paises.values())

    # Optional: Limit the number of slices for better readability
    # Combine smaller slices into 'Other'
    def combine_small_slices(labels, sizes, threshold=0.02):
        """
        Combines slices smaller than a threshold into 'Other'.

        Args:
            labels (list): List of labels.
            sizes (list): Corresponding sizes.
            threshold (float): Threshold proportion below which slices are combined.

        Returns:
            tuple: (new_labels, new_sizes)
        """
        total = sum(sizes)
        new_labels = []
        new_sizes = []
        other_size = 0
        for label, size in zip(labels, sizes):
            proportion = size / total
            if proportion < threshold:
                other_size += size
            else:
                new_labels.append(label)
                new_sizes.append(size)
        if other_size > 0:
            new_labels.append('Other')
            new_sizes.append(other_size)
        return new_labels, new_sizes

    labels, sizes = combine_small_slices(labels, sizes, threshold=0.02)  # Adjust threshold as needed

    # Create pie chart
    plt.figure(figsize=(10, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Distribución de Accesos por País")
    plt.tight_layout()

    # Save the chart
    nombre_archivo = get_filename_without_extension(ruta)
    virtual_host = nombre_archivo.split("-")[0]
    output_dir = os.path.join("imagenes", virtual_host)
    os.makedirs(output_dir, exist_ok=True)
    chart_path = os.path.join(output_dir, f"{nombre_archivo}_countries.png")
    plt.savefig(chart_path)
    plt.close()
    print(f"Countries pie chart saved to {chart_path}")

    # Optional: Log unknown IPs
    if unknown_ips:
        unknown_log_path = os.path.join(output_dir, 'unknown_ips.log')
        try:
            with open(unknown_log_path, 'w') as f:
                for ip in unknown_ips:
                    f.write(f"{ip}\n")
            print(f"Unknown/Invalid IPs logged to {unknown_log_path}")
        except Exception as e:
            print(f"An error occurred while writing unknown IPs to log: {e}")

# Example usage
if __name__ == "__main__":
    # Path to your Apache log file
    log_file_path = "/var/log/apache2/jocarsa-oldlace-access.log"
    
    # Path to the GeoLite2 Country MMDB database
    mmdb_path = 'GeoLite2-Country.mmdb'  # Update this path if necessary
    
    # Generate the countries pie chart
    countries_pie_chart(log_file_path, mmdb_path)
