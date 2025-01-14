import matplotlib.pyplot as plt
import os
import re
from funciones.ayudante import get_filename_without_extension

def parse_log_line(line):
    """
    Parses a single line of the log file and extracts relevant fields.

    Returns a dictionary with keys:
    - ip
    - status
    - user_agent
    """
    # Regular expression to parse the log line
    log_pattern = re.compile(
        r'(?P<ip>\S+) \S+ \S+ \[[^\]]+\] "\S+ \S+ \S+" (?P<status>\d{3}) \d+ "[^"]*" "(?P<user_agent>[^"]*)"'
    )
    match = log_pattern.match(line)
    if match:
        return {
            'ip': match.group('ip'),
            'status': match.group('status'),
            'user_agent': match.group('user_agent')
        }
    else:
        return None

def response_status_pie_chart(ruta):
    """
    Generates a pie chart for response status codes.

    Args:
        ruta (str): Path to the log file.
    """
    status_counts = {}

    with open(ruta, 'r') as archivo:
        for linea in archivo:
            parsed = parse_log_line(linea)
            if parsed:
                status = parsed['status']
                status_counts[status] = status_counts.get(status, 0) + 1

    if not status_counts:
        print("No status codes found in the log file.")
        return

    # Prepare data for pie chart
    labels = list(status_counts.keys())
    sizes = list(status_counts.values())

    # Create pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Distribución de Códigos de Respuesta HTTP")
    plt.tight_layout()

    # Save the chart
    nombre_archivo = get_filename_without_extension(ruta)
    virtual_host = nombre_archivo.split("-")[0]
    output_dir = os.path.join("imagenes", virtual_host)
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, f"{nombre_archivo}_response_status.png"))
    plt.close()
    print(f"Response status pie chart saved to {output_dir}")

def operating_systems_pie_chart(ruta):
    """
    Generates a pie chart for operating systems based on user-agent.

    Args:
        ruta (str): Path to the log file.
    """
    os_counts = {}
    # Define patterns for operating systems
    os_patterns = {
        'Windows': re.compile(r'Windows NT'),
        'macOS': re.compile(r'Mac OS X'),
        'Linux': re.compile(r'Linux'),
        'Android': re.compile(r'Android'),
        'iOS': re.compile(r'iPhone|iPad'),
        'Other': re.compile(r'.*')  # Default
    }

    with open(ruta, 'r') as archivo:
        for linea in archivo:
            parsed = parse_log_line(linea)
            if parsed:
                user_agent = parsed['user_agent']
                detected = False
                for os_name, pattern in os_patterns.items():
                    if pattern.search(user_agent):
                        os_counts[os_name] = os_counts.get(os_name, 0) + 1
                        detected = True
                        break
                if not detected:
                    os_counts['Other'] = os_counts.get('Other', 0) + 1

    if not os_counts:
        print("No operating systems found in the log file.")
        return

    # Prepare data for pie chart
    labels = list(os_counts.keys())
    sizes = list(os_counts.values())

    # Create pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Distribución de Sistemas Operativos")
    plt.tight_layout()

    # Save the chart
    nombre_archivo = get_filename_without_extension(ruta)
    virtual_host = nombre_archivo.split("-")[0]
    output_dir = os.path.join("imagenes", virtual_host)
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, f"{nombre_archivo}_operating_systems.png"))
    plt.close()
    print(f"Operating systems pie chart saved to {output_dir}")

def browsers_pie_chart(ruta):
    """
    Generates a pie chart for browsers based on user-agent.

    Args:
        ruta (str): Path to the log file.
    """
    browser_counts = {}
    # Define patterns for browsers
    browser_patterns = {
        'Chrome': re.compile(r'Chrome/(?!(?:.*Edg|OPR))'),  # Exclude Edge and Opera
        'Firefox': re.compile(r'Firefox/'),
        'Safari': re.compile(r'Safari/(?!(?:.*Chrome))'),  # Exclude Chrome
        'Edge': re.compile(r'Edg/|Edge/'),
        'Internet Explorer': re.compile(r'MSIE |Trident/'),
        'Opera': re.compile(r'OPR/|Opera/'),
        'Other': re.compile(r'.*')  # Default
    }

    with open(ruta, 'r') as archivo:
        for linea in archivo:
            parsed = parse_log_line(linea)
            if parsed:
                user_agent = parsed['user_agent']
                detected = False
                for browser_name, pattern in browser_patterns.items():
                    if pattern.search(user_agent):
                        browser_counts[browser_name] = browser_counts.get(browser_name, 0) + 1
                        detected = True
                        break
                if not detected:
                    browser_counts['Other'] = browser_counts.get('Other', 0) + 1

    if not browser_counts:
        print("No browsers found in the log file.")
        return

    # Prepare data for pie chart
    labels = list(browser_counts.keys())
    sizes = list(browser_counts.values())

    # Create pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Distribución de Navegadores")
    plt.tight_layout()

    # Save the chart
    nombre_archivo = get_filename_without_extension(ruta)
    virtual_host = nombre_archivo.split("-")[0]
    output_dir = os.path.join("imagenes", virtual_host)
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, f"{nombre_archivo}_browsers.png"))
    plt.close()
    print(f"Browsers pie chart saved to {output_dir}")

def robots_pie_chart(ruta):
    """
    Generates a pie chart indicating whether accesses are from robots or humans.

    Args:
        ruta (str): Path to the log file.
    """
    robot_count = 0
    human_count = 0
    # Define patterns for robots
    robot_patterns = [
        re.compile(r'bot', re.I),
        re.compile(r'spider', re.I),
        re.compile(r'crawl', re.I),
        re.compile(r'facebookexternalhit', re.I),
        re.compile(r'Googlebot', re.I),
        re.compile(r'Bingbot', re.I),
        # Add more known robot user-agent identifiers here
    ]

    with open(ruta, 'r') as archivo:
        for linea in archivo:
            parsed = parse_log_line(linea)
            if parsed:
                user_agent = parsed['user_agent']
                is_robot = any(pattern.search(user_agent) for pattern in robot_patterns)
                if is_robot:
                    robot_count += 1
                else:
                    human_count += 1

    if robot_count == 0 and human_count == 0:
        print("No data found to classify as robot or human.")
        return

    # Prepare data for pie chart
    labels = []
    sizes = []
    colors = []
    if robot_count > 0:
        labels.append('Robot')
        sizes.append(robot_count)
        colors.append('#ff9999')  # Red
    if human_count > 0:
        labels.append('Human')
        sizes.append(human_count)
        colors.append('#66b3ff')  # Blue

    # Create pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    plt.title("Accesos de Robots vs Humanos")
    plt.tight_layout()

    # Save the chart
    nombre_archivo = get_filename_without_extension(ruta)
    virtual_host = nombre_archivo.split("-")[0]
    output_dir = os.path.join("imagenes", virtual_host)
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, f"{nombre_archivo}_robots.png"))
    plt.close()
    print(f"Robots pie chart saved to {output_dir}")
