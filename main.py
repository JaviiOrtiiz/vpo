import requests
import difflib
from bs4 import BeautifulSoup
import logging

# URL de la página a monitorear
url = "http://www.registresolicitants.cat/registre/"

# Archivo para almacenar el contenido previo html
archivo_previo = 'contenido_previo.html'

def obtener_y_parsear_contenido(url):
    # Realizar una solicitud GET para obtener el contenido de la página, usando el contexto SSL generado
    payload = {}
    # cookie en el archivo secrets.txt, segunda línea
    cookie = str(open('secrets.txt').read().strip().split('\n')[1])
    headers = {
        'Cookie': cookie
    }
    # utf 8 a response
    response = requests.request("GET", url, headers=headers, data=payload)
    contenido_raw = str(response.text)
    # Parsear el contenido html
    soup = BeautifulSoup(contenido_raw, 'html.parser')
    # Obtener el contenido del cuerpo del html. nos interesa solo el contenido dentro del div clas=contenidohome
    # opcion 1: obtener el div con la clase correspondiente
    texto = soup.find('div', class_="contenidohome").prettify()
    # eliminar odas las etiquetas html de ambas opciones
    texto = BeautifulSoup(texto, 'html.parser').get_text()
    
    # eliminar todos los saltos de línea
    # texto = texto.replace('\n', '')
    
    # devolver ambos resultados concatenados
    print(texto)
    return texto

def comparar_contenido(contenido_actual, contenido_previo):
    # Obtener diferencias entre el contenido actual y el contenido previo en el cuerpo del html
    differ = difflib.Differ()
    diff = list(differ.compare(contenido_previo.splitlines(), contenido_actual.splitlines()))
    # Filtrar solo las líneas que han cambiado
    cambios = [linea for linea in diff if linea.startswith('+ ') or linea.startswith('- ')]
    # Devolver los cambios en lista
    return cambios

def enviar_notificacion(cambio):
    # Aquí debes ingresar la URL del webhook donde deseas recibir las notificaciones, esta en el archivo secrets.txt
    # Aquí puedes personalizar el contenido de la notificación
    payload = {'message': cambio}
    headers = {'Content-Type': 'application/json'}
    # Enviar solicitud POST al webhook, en el archivo secrets.txt, primera línea
    webhook_url = str(open('secrets.txt').read().strip().split('\n')[0])
    requests.post(webhook_url, json=payload, headers=headers)

def main():
    # Obtener el contenido previo, si existe
    try:
        with open(archivo_previo, 'r', encoding='utf-8') as archivo:
            contenido_previo = archivo.read()
    except FileNotFoundError:
        contenido_previo = ''
    try:
        # Obtener el contenido actual
        contenido_actual = obtener_y_parsear_contenido(url)

        # Comparar contenido actual con contenido previo
        cambio = comparar_contenido(contenido_actual, contenido_previo)

        # Si hay cambios en la lista cambios, enviar notificación y actualizar el archivo con el nuevo contenido
        if cambio:
            for cambio_element in cambio:
                # Si pone "Badalona" en el cambio, enviar notificación O empieza por "    - ".
                if "Badalona" in cambio_element or cambio_element.startswith("    - "):
                    enviar_notificacion(cambio_element. replace("    - ", ""))
        with open(archivo_previo, 'w', encoding='utf-8') as archivo:
            archivo.write(str(contenido_actual)) 
    except Exception as e:
        print(e)
        logging.error(e)

main()