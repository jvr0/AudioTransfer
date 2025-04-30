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
referencia = st.text_input("Ingresa la referencia")

# Validaciones
hay_espacios = " " in identificadores
caracteres_invalidos = not all(c.isdigit() or c == ',' for c in identificadores)
lista_identificadores = identificadores.split(',') if identificadores else []
demasiados_identificadores = len(lista_identificadores) > 25
referencia_vacia = referencia.strip() == ""

identificadores = identificadores.replace(' ','')

# Mensajes de error
if hay_espacios:
    st.text("No se permiten espacios")
if caracteres_invalidos:
    st.text("Solo se permiten números y comas")
if demasiados_identificadores:
    st.text("Máximo 25 identificadores")
if referencia_vacia:
    st.text("La referencia no puede estar vacía")

rows = []

# Botón desactivado si hay errores
boton_desactivado = hay_espacios or demasiados_identificadores or referencia_vacia

if st.button(":green[Activar]", disabled=boton_desactivado):
    st.success("Accediendo a datos de Discogs")

    for i in lista_identificadores:
        row = fetch_data(i, referencia) # type: ignore
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
