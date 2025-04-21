import streamlit as st
import pandas as pd
import time
from PIL import Image
from io import BytesIO

from src.support_API import *

# CONFIG INICIAL
st.set_page_config(
    page_title="AudioAlchemy",
    page_icon=":alembic:",
    layout="wide",
    initial_sidebar_state="expanded",
)

identificadores = st.text_area('Ingresa los identificadores (Sin espacios, separados por ",")', height=200)
if " " in identificadores:
    st.text("Hay espacios en tu texto")
identificadores = identificadores.split(',')
if len(identificadores) > 25:
    st.text("Más de 25 identificadores añadidos")
referencia = st.text_input("Ingresa la referencia")
rows = []  # Lista para guardar los resultados

if st.button(":green[Activar]"):

    for i in identificadores:
        row = fetch_data(i, referencia)
        rows.append(row)
        time.sleep(3)

    df = pd.DataFrame(rows)

    # Guardar el excel en la memoria
    output = BytesIO()
    df.to_excel(output, index=False, engine='xlsxwriter')
    output.seek(0)

    # Botón para descargar
    st.download_button(
        label="📥 Descargar resultados",
        data=output,
        file_name="csv_TC.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

icono = Image.open('img/icono.png')
st.sidebar.image(icono, width=100)
st.sidebar.title("AudioTransfer")
