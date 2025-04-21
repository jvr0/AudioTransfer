from requests_oauthlib import OAuth1
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
import requests as req
import os
import time
import random
# Cargar las variables del archivo .env
load_dotenv()

# Juramento para autentificarse en la API. OAuth1: identificación usuario y contraseña
oauth = OAuth1(
        st.secrets["key"],
        client_secret=st.secrets['secret'],
        resource_owner_key=st.secrets['access_oauth_token'],
        resource_owner_secret=st.secrets['access_oauth_token_secret'],
        verifier=st.secrets['oauth_verifier'])

def fetch_data(id, ref_num):
    url = f"https://api.discogs.com/releases/{id}"
    res = req.get(url, auth=oauth)
    data = res.json()

    barcode = next((i.get('value') for i in data.get('identifiers', []) if i.get('description') == 'Scanned'), "" )
    artista = data.get('artists_sort')
    titulo = data.get('title', '')
    country = data.get('country', '')
    released = data.get('released', '')
    formato_name = data.get('formats',[])[0].get('name', '')
    formato_description = data.get('formats',[])[0].get('descriptions', '')[0]
    catno = data.get('labels', '')[0].get('catno', '')

    row = {
'TÍTULO': f'{artista} - {titulo} ({formato_name})',
'DESCRIPCIÓN': f"""{artista} - {titulo}
{formato_name}, {formato_description}
{country}, {released}
Cat. No: {catno}
Barcode: {barcode}""",

        'REFERENCIA': f'{ref_num}-{str(random.randint(1000,9999))}',
        'PRECIO': '',
        'ISBN': f'{barcode}',
        'SECCIÓN': '453',
        'ESTADO': '5',
        'DESCRIPCIÓN DEL ESTADO': 'Envíos muy rápidos con tarifa plana, combine discos y pague solo por el primer lote.',
        'OPERACIÓN': 'ALTA',
        'STOCK': 1,
        'FECHA DE PUBLICACIÓN': 'hoy',
        'FORMA DE ENVÍO': 'Otros',
        'GASTOS FIJOS': '4,5',
        }
    
    print(f"Row from {id} added")

    return row

data = [12723436, 3375250, 1117020, 5960365, 12691804, 297641, 682481, 3165]


# Llamada de ejemplo

"""3375250, 1117020, 5960365, 12691804, 297641, 682481, 3165"""