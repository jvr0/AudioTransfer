from requests_oauthlib import OAuth1
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
import requests as req
import time
import os
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

    row = {
        'title': data.get('title'),
        'country': data.get('country'),
        'released': data.get('released'),
        'notes': data.get('notes'),
        'barcode': data.get('identifiers')[1].get('value') if len(data.get('identifiers', [])) > 1 else None,
        'matrix': data.get('identifiers')[5].get('value') if len(data.get('identifiers', [])) > 5 else None,
        'format': data.get('formats')[0].get('name') if data.get('formats') else None,
        'year': data.get('year'),
        'name': data.get('artists_sort')
    }

    return row

# Llamada de ejemplo


data = [12723436, 3375250, 1117020]

rows = []  # Lista para guardar los resultados

for i in data:
    row = fetch_data(i)
    rows.append(row)
    time.sleep(2)

df = pd.DataFrame(rows)

df.to_excel('results.xlsx', index=False)