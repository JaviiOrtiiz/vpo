import requests
import difflib
from bs4 import BeautifulSoup

# URL de la página a monitorear
url = "http://www.registresolicitants.cat/registre/"

# Archivo para almacenar el contenido previo html
archivo_previo = 'contenido_previo.html'

def obtener_y_parsear_contenido(url,class_name):
    # Realizar una solicitud GET para obtener el contenido de la página, usando el contexto SSL generado
    payload = {}
    # cookie en el archivo secrets.txt, segunda línea
    cookie = str(open('secrets.txt').read().strip().split('\n')[1])
    headers = {
        'Cookie': cookie
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    contenido_raw = str(response.text.encode('utf-8'))
    # Parsear el contenido html
    soup = BeautifulSoup(contenido_raw, 'html.parser')
    # Obtener el contenido del cuerpo del html. nos interesa solo el contenido dentro del div clas=contenidohome
    # opcion 1: obtener el div con la clase correspondiente
    option1 = soup.find('div', class_=class_name).prettify()
    #opcion 2: obtener los <p> 
    option2 = soup.find_all('p')
    # eliminar odas las etiquetas html de ambas opciones
    option1 = BeautifulSoup(option1, 'html.parser').get_text()
    option2 = [BeautifulSoup(p.prettify(), 'html.parser').get_text() for p in option2]
    # eliminar todos los saltos de línea
    option1 = option1.replace('\n', '')
    option2 = [p.replace('\n', '') for p in option2]
    # devolver ambos resultados concatenados
    return option1 + '\n'.join(option2)

def comparar_contenido(contenido_actual, contenido_previo):
    # Obtener diferencias entre el contenido actual y el contenido previo en el cuerpo del html
    differ = difflib.Differ()
    diff = list(differ.compare(contenido_previo.splitlines(), contenido_actual.splitlines()))
    # Filtrar solo las líneas que han cambiado
    cambios = [linea for linea in diff if linea.startswith('+ ') or linea.startswith('- ')]
    # Devolver los cambios como string
    return '\n'.join(cambios)

def enviar_notificacion(message):
    # Aquí debes ingresar la URL del webhook donde deseas recibir las notificaciones, esta en el archivo secrets.txt
    # Aquí puedes personalizar el contenido de la notificación
    payload = {'message': message}
    headers = {'Content-Type': 'application/json'}
    # Enviar solicitud POST al webhook, en el archivo secrets.txt, primera línea
    webhook_url = str(open('secrets.txt').read().strip().split('\n')[0])
    requests.post(webhook_url, json=payload, headers=headers)

def todo(url,archivo_previo, class_name):
    # Obtener el contenido previo, si existe
    try:
        with open(archivo_previo, 'r') as archivo:
            
            #contenido_previo = archivo.read() # error invalid start byte
            contenido_previo = archivo.read().encode('utf-8').decode('utf-8')
    except FileNotFoundError:
        contenido_previo = ''

    # Obtener el contenido actual
    contenido_actual = obtener_y_parsear_contenido(url,class_name)

    # Comparar contenido actual con contenido previo
    cambio = comparar_contenido(contenido_actual, contenido_previo)

    # Si hay cambios, enviar notificación y actualizar el archivo con el nuevo contenido
    if cambio:
        if 'olh.cat' in url:
            cambio = 'Badalona'
        else:
            cambio = 'Catalunya'
        enviar_notificacion(cambio)
        with open(archivo_previo, 'w') as archivo:
            archivo.write(str(contenido_actual))

# Para la página de Catalunya:
todo("http://www.registresolicitants.cat/registre/",'contenido_previo_cat.html','contenidohome')

# Para la página de Badalona:
todo("https://www.olh.cat/habitatge-protegit/",'contenido_previo_bdn.html','wpb_wrapper')
