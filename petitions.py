import json
import os
from datetime import datetime
from xml.dom import minidom

import requests

global tk
user = ''
password = ''


def login():
    global tk

    # Peticion POST
    url = ''
    payload = json.dumps({"nombreUsuario": user, "password": password})
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(
        url,
        headers=headers,
        data=payload
    )

    # Comprobar respuesta
    if response.status_code == 200:
        # Guardar token
        tk = json.loads(json.dumps(response.json()))["token"]
        return 'Inicio de sesión correcto.', True
    elif response.status_code == 401:
        return 'Inicio de sesion incorrecto.', False

    else:
        save_error("Errores/ELogin - " + datetime.now().strftime("%d-%m %H%M%S") + ".json", response)
        return 'Error de login en servidor/aplicación, guardado:' + str(response.json()), False


# Comprobar si esta logueado
def checklogin():
    global tk

    try:
        tk
    except NameError:
        return True


def sendauction(payload):
    global tk

    # Comprobar si esta logueado
    if checklogin():
        return "Tienes que iniciar sesión."

    # Peticion POST
    url = ''
    headers = {
        'Authorization': 'Bearer ' + tk,
        'Content-Type': 'application/xml'
    }
    payload = payload
    response = requests.post(
        url,
        headers=headers,
        data=payload
    )

    # Comprobar respuesta
    if response.status_code == 201:
        return 'Subasta guardada.'
    elif response.status_code == 500:
        return 'Error de subasta.'
    elif response.status_code == 401:
        return 'Reinicia la aplicacion.'
    else:
        save_error("Errores/EEnvioXML - " + datetime.now().strftime("%d-%m %H%M%S") + ".json", response)
        return "Error de substa en servidor/aplicación, guardado:" + str(response.json())


def preloadbydate(fecha):
    global tk

    # Comprobar si esta logueado
    if checklogin():
        return "Tienes que iniciar sesión."

    # Peticion POST
    url = ''
    payload = json.dumps({"nombreUsuario": user, "password": password})
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/xml',
        'Authorization': 'Bearer ' + tk
    }
    params = {'fecha': fecha}
    response = requests.post(
        url,
        headers=headers,
        params=params,
        data=payload
    )

    if response.status_code == 200:
        # Guardar en archivo
        folder = "Precargas"
        filename = "Precarga - " + fecha + ".xml"
        os.makedirs(os.path.dirname(folder + "/" + filename), exist_ok=True)
        with open(folder + "/" + filename, "w") as f:
            f.write(str(minidom.parseString(response.text).toprettyxml(indent="   ")))
            f.close()
        return 'Precarga guardada: ' + filename
    elif response.status_code == 401:
        return 'Reinicia la aplicacion.'

    else:
        save_error("Errores/EPrecarga - " + datetime.now().strftime("%d-%m %H%M%S") + ".json", response)
        return 'Error de precarga en servidor/aplicación, guardado: ' + str(response.json())


def downloadbuyers():
    global tk

    # Comprobar si esta logueado
    if checklogin():
        return "Tienes que iniciar sesión."

    # Peticion POST
    url = ''
    payload = json.dumps({"nombreUsuario": user, "password": password})
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/xml',
        'Authorization': 'Bearer ' + tk
    }
    response = requests.post(
        url,
        headers=headers,
        data=payload
    )

    if response.status_code == 200:
        # Guardar en archivo
        folder = "Compradores"
        filename = "Compradores - " + datetime.now().strftime("%d-%m %H%M%S") + ".xml"
        os.makedirs(os.path.dirname(folder + "/" + filename), exist_ok=True)
        with open(folder + "/" + filename, "w") as f:
            f.write(str(minidom.parseString(response.text).toprettyxml(indent="   ")))
            f.close()
        return 'Compradores guardados: ' + filename
    elif response.status_code == 401:
        return 'Reinicia la aplicacion.'

    else:
        save_error("Errores/ECompradores - " + datetime.now().strftime("%d-%m %H%M%S") + ".json", response)
        return 'Error de compradores en servidor/aplicación, guardado: ' + str(response.json())


def save_error(filename, response):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump(
            response.json(), f
        )
        f.close()
