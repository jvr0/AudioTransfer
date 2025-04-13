from requests_oauthlib import OAuth1
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
import requests as req
import os
import time
# Cargar las variables del archivo .env
load_dotenv()

# Juramento para autentificarse en la API. OAuth1: identificación usuario y contraseña
oauth = OAuth1(
                os.getenv("key"),
                client_secret=os.getenv('secret'),
                resource_owner_key=os.getenv('access_oauth_token'),
                resource_owner_secret=os.getenv('access_oauth_token_secret'),
                verifier=os.getenv('oauth_verifier')
                )

def fetch_data(id):
    url = f"https://api.discogs.com/releases/{id}"
    res = req.get(url, auth=oauth)
    data = res.json()

    formats = data.get('formats', [])
    identifiers = data.get('identifiers', [])

    # Construcción de la parte de formatos
    format_parts = []
    if formats:
        quantity = formats[0].get('qty')
        name = formats[0].get('name')
        descriptions = formats[0].get('descriptions', [])
        if quantity:
            format_parts.append(f"{quantity} x")
        if name:
            format_parts.append(name)
        if descriptions:
            format_parts.append(", ".join(descriptions))
    format_line = " ".join(format_parts)

    # Identificadores útiles
    catalog_number = next((i['value'] for i in identifiers if i.get('type') == 'Catalog#'), None)
    barcode = next((i['value'] for i in identifiers if i.get('type') == 'Barcode'), None)

    # Construcción de la celda final
    descripcion_larga = f"""{data.get('name', '')} - {data.get('title', '')}
    {format_line}
    {data.get('country', '')}, {data.get('year', '')}
    Cat. No: {catalog_number if catalog_number else ''}
    Barcode: {barcode if barcode else ''}"""

    print(descripcion_larga)
    return descripcion_larga

fetch_data(12723436)