from datetime import datetime
import json
import requests
import os
from dict2xml import dict2xml

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

    else:
        # Guardar en error en archivo
        filename = "Errores/ELogin - " + datetime.now().strftime("%d-%m %H%M%S") + ".json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            json.dump(
                response.json(), f
            )
            f.close()
        return 'Error de login en servidor/aplicación, guardado:' + str(response.json()), False


# Comprobar si esta logueado
def checklogin():
    global tk

    try:
        tk
    except NameError as e:
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
    payload = payload.read()
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
    else:
        # Guardar en error en archivo
        filename = "Errores/EEnvioXML - " + \
            datetime.now().strftime("%d-%m %H%M%S") + ".json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            json.dump(
                response.json(), f
            )
            f.close()
        return "Error de substa en servidor/aplicación, guardado:" + str(response.json())


def preloadbydate():
    global tk

    # Comprobar si esta logueado
    if checklogin():
        return "Tienes que iniciar sesión."

    # Peticion POST
    url = ''
    payload = json.dumps({"nombreUsuario": user, "password": password})
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + tk
    }
    params = {'fecha': datetime.now().strftime("%Y-%m-%d")}
    response = requests.post(
        url,
        headers=headers,
        params=params,
        data=payload
    )

    if response.status_code == 200:
        # Guardar en archivo
        folder = "Precargas"
        filename = "Precarga - " + datetime.now().strftime("%d-%m %H%M%S") + ".xml"
        os.makedirs(os.path.dirname(folder + "/" + filename), exist_ok=True)
        with open(folder + "/" + filename, "w") as f:
            dict2xml(
                response.json(), f
            )
            f.close()
        return 'Precarga guardada: ' + filename

    else:
        # Guardar en error en archivo
        filename = "Errores/EPrecarga - " + \
            datetime.now().strftime("%d-%m %H%M%S") + ".json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            json.dump(
                response.json(), f
            )
            f.close()
        return 'Error de precarga en servidor/aplicación, guardado: ' + str(response.json())
