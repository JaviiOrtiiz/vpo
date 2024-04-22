import requests
import difflib

# URL de la página a monitorear
url = "http://www.registresolicitants.cat/registre/"

# Archivo para almacenar el contenido previo html
archivo_previo = 'contenido_previo.html'

def obtener_contenido(url):
    # Realizar una solicitud GET para obtener el contenido de la página, usando el contexto SSL generado
    payload = {}
    # cookie en el archivo secrets.txt, segunda línea
    cookie = str(open('secrets.txt').read().strip().split('\n')[1])
    headers = {
        'Cookie': cookie
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    # Devolver el contenido html de la página como string
    return str(response.text.encode('utf-8'))

def comparar_contenido(contenido_actual, contenido_previo):
    # Obtener diferencias entre el contenido actual y el contenido previo en el cuerpo del html
    differ = difflib.Differ()
    diff = list(differ.compare(contenido_previo.splitlines(), contenido_actual.splitlines()))
    # Filtrar solo las líneas que han cambiado
    cambios = [linea for linea in diff if linea.startswith('+ ') or linea.startswith('- ')]
    # Devolver los cambios como string
    return '\n'.join(cambios)

def enviar_notificacion(cambio):
    # Aquí debes ingresar la URL del webhook donde deseas recibir las notificaciones, esta en el archivo secrets.txt
    # Aquí puedes personalizar el contenido de la notificación
    payload = {'cambio': cambio}
    # Enviar solicitud POST al webhook, en el archivo secrets.txt, primera línea
    webhook_url = str(open('secrets.txt').read().strip().split('\n')[0])
    requests.post(webhook_url, json=payload)

# Obtener el contenido previo, si existe
try:
    with open(archivo_previo, 'r') as archivo:
        contenido_previo = archivo.read()
except FileNotFoundError:
    contenido_previo = ''

# Obtener el contenido actual
contenido_actual = obtener_contenido(url)

# Comparar contenido actual con contenido previo
cambio = comparar_contenido(contenido_actual, contenido_previo)

# Si hay cambios, enviar notificación y actualizar el archivo con el nuevo contenido
if cambio:
    enviar_notificacion(cambio)
    with open(archivo_previo, 'w') as archivo:
        archivo.write(str(contenido_actual))