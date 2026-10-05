import requests
import re
from urllib.parse import urlparse

def obtener_dominio(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return urlparse(url).netloc.replace('www.', '')

def escanear_w3techs():
    url_input = input("Ingresa el link de la página a analizar: ").strip()
    dominio = obtener_dominio(url_input)
    
    url_w3techs = f"https://w3techs.com/sites/info/{dominio}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    try:
        response = requests.get(url_w3techs, headers=headers, timeout=15)
        
        if response.status_code == 403:
            print("Error: W3Techs bloqueó la petición (Protección Anti-Bot activa).")
            return
        elif response.status_code != 200:
            print(f"Error: Respuesta inesperada del servidor (Código {response.status_code}).")
            return

        patron = r'<a href="[^"]*technologies/details/(ec|py|cm)-[^"]*">([^<]+)</a>'
        coincidencias = re.findall(patron, response.text)
        
        encontrados = set()
        for categoria, nombre in coincidencias:
            if categoria == 'ec':
                encontrados.add(f"Ecommerce (Comercio): {nombre}")
            elif categoria == 'py':
                encontrados.add(f"Pasarela de Pago: {nombre}")
            elif categoria == 'cm':
                encontrados.add(f"Sistema de Gestión (CMS): {nombre}")

        if encontrados:
            print("\n-> EXTRACCIÓN DINÁMICA DE W3TECHS:")
            for item in sorted(encontrados):
                print(f" - {item}")
            print()
        else:
            print("\n-> W3Techs no muestra datos de comercio para esta página.\n")

    except requests.exceptions.RequestException:
        print("-> ERROR: No se pudo conectar a W3Techs.\n")

while True:
    escanear_w3techs()
    if input("¿Deseas analizar otra página? (s/n): ").strip().lower() != 's':
        break
