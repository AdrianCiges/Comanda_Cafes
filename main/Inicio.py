import streamlit as st
import pandas as pd
import overpy
from collections import Counter
from PIL import Image
import base64
import io
import datetime
from datetime import datetime, time, timedelta
import re
import streamlit.components.v1 as components
import time as timee
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import math
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import urllib.parse
import geocoder
import os
import leafmap.foliumap as leafmap
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
import json
import googlemaps
import streamlit as st
import ast
import smtplib
from email.mime.text import MIMEText
import streamlit.components.v1 as components
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

st.set_page_config(layout="wide", page_title="Ruta del Café", page_icon="./img/cafe5.png")

# # Cambiar el tema de la página principal
# st.markdown(
#     """
#     <style>
#     .stApp {
#         background-color: #e9ecef;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Texto principal
# texto_principal = '<h1 style="text-align:center"><span style="font-size: 40px;">☕ </span> <u>LA RUTA DEL CAFÉ</u></h1>'

# Estilos CSS para el logo y el contenedor
estilos_css = f"""
    <style>
    .logo-container {{
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .logo-img {{
        height: 40px;
        width: auto;
        margin-left: 20px;
    }}
    </style>
    """

# Ruta de la imagen del logo
LOGO_IMAGE = "./img/mapa.png"

# Texto principal
texto_principal = '<h1 style="text-align:center"><span style="font-size: 40px;">☕ </span> <u> LA RUTA DEL CAFÉ</u></h1>'
    
# Leer la imagen del logo y codificarla en base64
with open(LOGO_IMAGE, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# Mostrar el texto principal y el logo
st.markdown(estilos_css, unsafe_allow_html=True)
st.markdown(
    f'<div class="logo-container">{texto_principal}<img src="data:image/png;base64,{encoded_image}" class="logo-img"></div>',
    unsafe_allow_html=True
)

# Cambiar el fondo de la página principal a una imagen
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://github.com/AdrianCiges/Comanda_Cafes/blob/main/img/wood_background3.jpg?raw=true");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

ms = st.session_state
if "themes" not in ms: 
  ms.themes = {"current_theme": "light",
                    "refreshed": True,
                    
                    "light": {"theme.base": "dark",
                              "theme.backgroundColor": "white",
                              "theme.primaryColor": "red",
                              "theme.secondaryBackgroundColor": "#ebedf0",
                              "theme.textColor": "black",
                              "button_face": "🌜"},

                    "dark":  {"theme.base": "light",
                              "theme.backgroundColor": "white",
                              "theme.primaryColor": "red",
                              "theme.secondaryBackgroundColor": "#ebedf0",
                              "theme.textColor": "black",
                              "button_face": "🌞"},
                    }
  

def ChangeTheme():
  previous_theme = ms.themes["current_theme"]
  tdict = ms.themes["light"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]
  for vkey, vval in tdict.items(): 
    if vkey.startswith("theme"): st._config.set_option(vkey, vval)

  ms.themes["refreshed"] = False
  if previous_theme == "dark": ms.themes["current_theme"] = "light"
  elif previous_theme == "light": ms.themes["current_theme"] = "dark"


btn_face = ms.themes["light"]["button_face"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]["button_face"]
# st.button(btn_face, on_click=ChangeTheme)

if ms.themes["refreshed"] == False:
  ms.themes["refreshed"] = True
  st.rerun()
# ------------------------------------------------------------------------------------CONFIG⬆️-------------------------------------
# ---------------------------------------------------------------------------------FUNCIONES⬇️-------------------------------------

def convert_coordinates(input_string):
    # Dividir las coordenadas en latitud y longitud
    lat, lon = map(float, input_string.split(', '))

    # Convertir la latitud a grados, minutos y segundos
    lat_deg = int(lat)
    lat_min = int((lat - lat_deg) * 60)
    lat_sec = (lat - lat_deg - lat_min / 60) * 3600

    # Convertir la longitud a grados, minutos y segundos
    lon_deg = int(lon)
    lon_min = int((lon - lon_deg) * 60)
    lon_sec = (lon - lon_deg - lon_min / 60) * 3600

    # Construir la cadena de salida en el formato deseado
    if "-" in str(lat) and "-" in str(lon):
        output_string = f"{lat_deg}°{lat_min}'{lat_sec:.1f}\"S+{lon_deg}°{lon_min}'{lon_sec:.1f}\"W"
    elif "-" in str(lat):
        output_string = f"{lat_deg}°{lat_min}'{lat_sec:.1f}\"S+{lon_deg}°{lon_min}'{lon_sec:.1f}\"E"
    elif "-" in str(lon):
        output_string = f"{lat_deg}°{lat_min}'{lat_sec:.1f}\"N+{lon_deg}°{lon_min}'{lon_sec:.1f}\"W"
    else:
        output_string = f"{lat_deg}°{lat_min}'{lat_sec:.1f}\"N+{lon_deg}°{lon_min}'{lon_sec:.1f}\"E"

    return output_string.replace("-","")

def make_clickable(val):
    # target _blank to open new window
    return '<a target="_blank" href="{}">{}</a>'.format(val,val)

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in meters between two points
    on the Earth's surface identified by latitude and longitude.
    :param lat1: Latitude of the first point (in degrees)
    :param lon1: Longitude of the first point (in degrees)
    :param lat2: Latitude of the second point (in degrees)
    :param lon2: Longitude of the second point (in degrees)
    :return: Distance in meters
    """
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    radius_earth = 6371000  # Earth's radius in meters
    distance = radius_earth * c

    return int(distance)


@st.cache_data
def get_data():
    data_url = os.path.join(os.path.dirname(__file__), '..', 'data', 'cafeterias_horarios_ocupacion.xlsx')
    df = pd.read_excel(data_url, engine='openpyxl', usecols= [ 'Columna1', 'url', 'nombre', 'ciudad', 'precio', 'latitud', 'longitud',
                                                               'rating', 'reviews', 'cerrado', 'cerrado_temporal', 'horarios',
                                                               'ocupacion', 'lgbt', 'aperitivos', 'terraza', 'cerveza',
                                                               'desayuno_almuerzo', 'sentarse', 'llevar', 'postres', 'acepta_reserva',
                                                               'perros', 'perros_fuera', 'wifi', 'wifi_gratis', 'vino',
                                                               'horario_raw_lunes', 'horario_raw', 'horario_raw_martes',
                                                               'horario_martes', 'horario_raw_miércoles', 'horario_miércoles',
                                                               'horario_raw_jueves', 'horario_jueves', 'horario_raw_viernes',
                                                               'horario_viernes', 'horario_raw_sábado', 'horario_sábado',
                                                               'horario_raw_domingo', 'horario_domingo', 'ocupacion_lunes',
                                                               'ocupacion_martes', 'ocupacion_miércoles', 'ocupacion_jueves',
                                                               'ocupacion_viernes', 'ocupacion_sábado', 'ocupacion_domingo' ],
                      nrows=20000)
    df = df.drop('Columna1', axis=1)
    return df

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    modify = st.checkbox("🎯 Añadir filtros")
    if not modify:
        return df

    df = df.copy()

    modification_container = st.container()

    with modification_container:
        columnas_filtro = ['☕ Nombre', '🏙️ Ciudad', '🔓 Abierto Ahora', '💲 Nivel de precios','⭐ Puntuación', '💬 Nº Comentarios', '📊 % Ocupación Ahora',
                             '🪑 Puedes sentarte', '☀️ Tiene terraza', '🍺 Sirve Cerveza', '🍷 Sirve vino', '🥪 Sirve desayunos/almuerzos', '🫒 Sirve aperitivos', '🍪 Sirve postres', '🚶‍♂️ Para llevar', 
                             '🙋‍♀️ Acepta reserva', '🐕‍🦺 Acepta perros', '🐕 Acepta perros fuera', '🛜 Tiene Wifi','🛜 Tiene Wifi Gratis', '🏳️‍🌈 LGBT+ friendly',
                          ]
        to_filter_columns = st.multiselect("Filtrar cafeterías por:", columnas_filtro, placeholder="Selecciona un campo")
        st.write('-----------')
        
        for column in to_filter_columns:
            # Si la columna es '💬 Nº Comentarios', usa un widget especial en la barra lateral
            if column == '💬 Nº Comentarios':
                left, right = st.columns((1, 20))
                # left.write("↳")
                user_num_input = right.number_input(
                    f"{column} mínimo",
                    min_value=int(df[column].min()),
                    max_value=int(df[column].max()),
                    value=int(df[column].min()),
                )
                st.write('-----------')
                df = df[df[column] >= user_num_input]
            else:
                left, right = st.columns((1, 20))
                # left.write("↳")
                # Trata las columnas con < 10 valores únicos como categóricas
                if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                    user_cat_input = right.multiselect(
                        f"{column}",
                        sorted(df[column].unique()),
                        default=sorted(list(df[column].unique())),
                    )
                    st.write('-----------')
                    df = df[df[column].isin(user_cat_input)]
                elif is_numeric_dtype(df[column]):
                    _min = float(df[column].min())
                    _max = float(df[column].max())
                    step = (_max - _min) / 100
                    user_num_input = right.slider(
                        f"{column}",
                        min_value=_min,
                        max_value=_max,
                        value=(_min, _max),
                        step=step,
                    )
                    st.write('-----------')
                    df = df[df[column].between(*user_num_input)]
                elif is_datetime64_any_dtype(df[column]):
                    user_date_input = right.date_input(
                        f"{column}",
                        value=(
                            df[column].min(),
                            df[column].max(),
                        ),
                    )
                    st.write('-----------')
                    if len(user_date_input) == 2:
                        user_date_input = tuple(map(pd.to_datetime, user_date_input))
                        start_date, end_date = user_date_input
                        df = df.loc[df[column].between(start_date, end_date)]
                else:
                    user_text_input = right.text_input(
                        f"{column}",
                    )
                    st.write('-----------')
                    if user_text_input:
                        df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

# def buscar_cafeterias(latitud, longitud, key, radio=10000):
#     # Configurar la clave de API

#     gmaps = googlemaps.Client(key=key)

#     # Realizar la búsqueda
#     resultados = gmaps.places_nearby(location=(latitud, longitud), radius=radio, type='cafe')

#     # Extraer la información deseada
#     cafeterias = []
#     for lugar in resultados['results']:
#         # Detalles básicos
#         place_id = lugar.get('place_id', None)
#         nombre = lugar.get('name', None)
#         latitud = lugar.get('geometry', {}).get('location', None).get('lat')
#         longitud = lugar.get('geometry', {}).get('location', None).get('lng')
#         rating = lugar.get('rating', None)
#         opiniones = lugar.get('user_ratings_total', None)

#         # Obtener detalles del lugar
#         detalles = gmaps.place(place_id=place_id)
#         abierto_ahora = detalles.get('result', {}).get('current_opening_hours', {}).get('open_now', None)
#         wheelchair_accessible_entrance = detalles.get('result', {}).get('wheelchair_accessible_entrance', None) 
#         price_level = detalles.get('result', {}).get('price_level', None)
#         reservable = detalles.get('result', {}).get('reservable', None)
        
#         # Más detalles
#         serves_breakfast = detalles.get('result', {}).get('serves_breakfast', None)
#         serves_brunch = detalles.get('result', {}).get('serves_brunch', None)
#         serves_lunch = detalles.get('result', {}).get('serves_lunch', None)
#         serves_dinner = detalles.get('result', {}).get('serves_dinner', None)
#         serves_vegetarian_food = detalles.get('result', {}).get('serves_vegetarian_food', None)
#         serves_beer = detalles.get('result', {}).get('serves_beer', None)
#         serves_wine = detalles.get('result', {}).get('serves_wine', None)
#         takeout = detalles.get('result', {}).get('takeout', None)
#         url = detalles.get('result', {}).get('url')

#         cafeterias.append([nombre, abierto_ahora, latitud, longitud, rating, 
#                            opiniones, wheelchair_accessible_entrance, reservable, price_level,
#                            serves_breakfast, serves_brunch, serves_lunch, serves_dinner,
#                            serves_vegetarian_food, serves_beer, serves_wine, takeout, url])

#         # Convertir a DataFrame
#         df_cafeterias = pd.DataFrame(cafeterias, columns=['nombre', 'abierto_ahora', 'latitud', 'longitud', 'rating', 
#                                                           'opiniones', 'wheelchair_accessible_entrance', 'reservable','price_level',
#                                                           'serves_breakfast', 'serves_brunch', 'serves_lunch', 'serves_dinner',
#                                                           'serves_vegetarian_food', 'serves_beer', 'serves_wine', 'takeout', 'url'])

#         return df_cafeterias


# def convertir_a_decimal(hora_str):
#     # Normalizar la cadena para unificar los formatos de AM/PM y eliminar espacios no estándar
#     hora_str = re.sub(r'\s+', ' ', hora_str)  # Convierte todos los espacios a espacios estándar
#     hora_str = hora_str.replace('\xa0', ' ').upper()  # Reemplaza espacios no separables y normaliza a mayúsculas
#     hora_str = re.sub(r'([AP])\.?\s*M\.?', r'\1M', hora_str)  # Normaliza las marcas de AM/PM

#     # Extraer horas, minutos y periodo (AM/PM) utilizando una expresión regular
#     match = re.match(r'(\d+):?(\d*)\s*([AP]M)?', hora_str)
#     if match:
#         horas, minutos, periodo = match.groups()
#         horas = int(horas)
#         minutos = int(minutos) if minutos else 0
#         if periodo == 'PM' and horas < 12:
#             horas += 12
#         elif periodo == 'AM' and horas == 12:
#             horas = 0
        
#         # Convertir horas y minutos a formato decimal
#         hora_decimal = horas + minutos / 60
        
#         return round(hora_decimal, 2)
#     return None

# def procesar_horarios(horarios):
#     intervalos_finales = []
#     for horario in horarios:
#         # Inicializar una lista para este horario, que podría contener uno o dos intervalos
#         intervalos_de_este_horario = []
#         partes = horario.split(',')
#         for parte in partes:
#             # Usar expresión regular para dividir en 'inicio' y 'fin', manejando posibles errores
#             match = re.match(r'(.*?)(?:\s+to\s+)(.*)', parte.strip(), re.IGNORECASE)
#             if match:
#                 inicio, fin = match.groups()
#                 inicio_decimal = convertir_a_decimal(inicio)
#                 fin_decimal = convertir_a_decimal(fin)
#                 # Ajuste por cruce de medianoche si es necesario
#                 if fin_decimal < inicio_decimal:
#                     fin_decimal += 24
#                 intervalos_de_este_horario.append([inicio_decimal, fin_decimal])
#             else:
# #                 print(f"No se pudo procesar el intervalo: {parte}")
# #                 intervalos_de_este_horario.append('Desconocido')
#                 pass
#         # Añadir los intervalos procesados para este horario a la lista final
#         intervalos_finales.append(intervalos_de_este_horario)
#     return intervalos_finales

# Función para sustituir valores
def sustituir_valor(val):
    if val == True:
        return "Sí"
    elif val == False:
        return "No"
    else:
        return val 

def sustituir_valor_emoji(val):
    if val == "Sí":
        return "✅"
    elif val == "No":
        return "❌"
    else:
        return val 
# ---------------------------------------------------------------------------------FUNCIONES⬆️-------------------------------------
# --------------------------------------------------------------------------------------UBI ⬇️-------------------------------------

tab1, tab2 = st.tabs(["🗺️ Localizador", "📋 Comanda"])

loc = get_geolocation()
    
num_cafeterias = st.sidebar.number_input("Nº de cafeterías", value=10, min_value=1, max_value=1000, step=1, format="%i")

from_pc = st.sidebar.checkbox('Vista para ordenador')

with tab1:

    st.write('')

    if num_cafeterias != 1:
        st.markdown(f"<h2 style='margin-top: 0px; margin-bottom: -10px;'>Tus {num_cafeterias} cafeterías más cercanas</h2>", unsafe_allow_html=True)
        st.write('')
    else:
        st.markdown(f"<h2 style='margin-top: 0px; margin-bottom: -10px;'>Tu cafetería más cercana</h2>", unsafe_allow_html=True)
        st.write('')
        
    
    # Cargamos el dataframe (necesitamos optimizar esto)
    df = get_data()
    
    # Obtener la fecha y hora actual
    ahora = datetime.now()
    hora_actual_float = datetime.now().hour + datetime.now().minute / 60 + 1
    hora_actual = datetime.now().hour + 1
    
    # Obtener el nombre del día de la semana en inglés
    dia_semana_ing = ahora.strftime("%A")
    
    # Diccionario para traducir el día de la semana al español
    dias_semana_es = {"Monday": "lunes", "Tuesday": "martes", "Wednesday": "miércoles", "Thursday": "jueves", "Friday": "viernes", "Saturday": "sábado", "Sunday": "domingo"}
    
    # Traducir el día de la semana al español
    dia_semana_es = dias_semana_es.get(dia_semana_ing, "Desconocido")
    
    # Renombramos las columnas
    nuevos_nombres = ['Link', 'Nombre', 'Ciudad','Nivel de precios','Latitud','Longitud','Puntuación', 'Nº Comentarios', 'Cerrado permanentemene', 'Cerrado temporalmente', 'Horario','Porcentaje de Ocupación', 'LGBT+ friendly', 'Sirve aperitivos', 'Tiene terraza', 'Sirve Cerveza', 'Sirve desayunos/almuerzos', 'Puedes sentarte', 'Para llevar', 'Sirve postres', 'Acepta reserva', 'Acepta perros', 'Acepta perros fuera', 'Tiene Wifi','Tiene Wifi Gratis', 'Sirve vino', 
                       'horario_raw_lunes', 'horario_lunes', 
                       'horario_raw_martes', 'horario_martes', 
                       'horario_raw_miércoles', 'horario_miércoles',
                       'horario_raw_jueves', 'horario_jueves', 
                       'horario_raw_viernes', 'horario_viernes', 
                       'horario_raw_sábado', 'horario_sábado',
                       'horario_raw_domingo', 'horario_domingo', 
                       'ocupacion_lunes', 'ocupacion_martes', 'ocupacion_miércoles', 'ocupacion_jueves', 'ocupacion_viernes', 'ocupacion_sábado', 'ocupacion_domingo']
    
    df.columns = nuevos_nombres
    
    columna_dia_hoy_raw = "horario_raw_"+dia_semana_es
    columna_dia_hoy = "horario_"+dia_semana_es
    columna_ocupacion_hoy = "ocupacion_"+dia_semana_es
    columna_ocupacion_ahora = []
    
    for o in df[columna_ocupacion_hoy]:
        try:
            # Decodificar el JSON una sola vez
            ocupacion = json.loads(o.replace("'", '"'))
            # Buscar la hora actual dentro de los objetos decodificados
            encontrado = False
            for h in ocupacion:
                if h['hour'] == hora_actual:
                    columna_ocupacion_ahora.append(h['occupancyPercent'])
                    encontrado = True
                    break  # Salir del bucle una vez encontrada la hora actual
            if not encontrado:
                # Si no se encuentra la hora actual, agregar 'Desconocido' o un valor por defecto
                columna_ocupacion_ahora.append(0)
        except json.JSONDecodeError:
            # Manejar cadenas vacías, malformadas o valores None
            columna_ocupacion_ahora.append(0)
    
    df['Ocupación Ahora'] = columna_ocupacion_ahora
    
    output = []
    
    for horario_str in df[columna_dia_hoy]:
        try:
            # Convertir el string que representa una lista a una lista real
            horario = ast.literal_eval(horario_str)
        except (ValueError, SyntaxError):
            # Si hay un error en la conversión, establecer horario a una lista vacía
            horario = []
    
        horario_dict = {}
    
        if len(horario) > 1:
            for i, sublista in enumerate(horario):
                if len(sublista) == 2:
                    inicio, fin = sublista
                    duracion = fin - inicio
                    if duracion < 0:
                        duracion += 12 if i == 0 else 24
                    horario_dict[inicio] = duracion
        else:
            for sublista in horario:
                if len(sublista) == 2:
                    inicio, fin = sublista
                    duracion = fin - inicio
                    if duracion < 0:
                        duracion += 24
                    horario_dict[inicio] = duracion
                    
        output.append(horario_dict)
    
    
    abierto_ahora = []
    
    for horario_dict in output:
        abierto = False  # Asumimos que inicialmente no está abierto
        for inicio, duracion in horario_dict.items():
            # Calcular si la hora actual está dentro del rango de apertura
            if inicio <= hora_actual_float < (inicio + duracion):
                abierto = True
                break  # No necesitamos seguir revisando otros horarios si ya encontramos uno que está abierto
        abierto_ahora.append(abierto)
    
    df['Abierto Ahora'] = abierto_ahora
    
    columnas_a_modificar = ['Abierto Ahora',
                      'Puedes sentarte', 'Tiene terraza', 'Sirve Cerveza', 'Sirve vino', 'Sirve desayunos/almuerzos', 'Sirve aperitivos', 'Sirve postres', 'Para llevar', 
                      'Acepta reserva', 'Acepta perros', 'Acepta perros fuera', 'Tiene Wifi','Tiene Wifi Gratis', 'LGBT+ friendly',
                     ]
    for columna in columnas_a_modificar:
        df[columna] = df[columna].apply(sustituir_valor)
    
    # Reordenamos el dataframe
    df = df[['Link', 'Nombre', 'Ciudad','Abierto Ahora', 'Nivel de precios','Latitud','Longitud', 'Puntuación', 'Nº Comentarios', columna_dia_hoy_raw, 'Ocupación Ahora', # columna_ocupacion_hoy
             'Cerrado permanentemene', 'Cerrado temporalmente', #'Horario','Porcentaje de Ocupación', 
             'Puedes sentarte', 'Tiene terraza', 'Sirve Cerveza', 'Sirve vino', 'Sirve desayunos/almuerzos', 'Sirve aperitivos', 'Sirve postres', 'Para llevar', 
             'Acepta reserva', 'Acepta perros', 'Acepta perros fuera', 'Tiene Wifi','Tiene Wifi Gratis', 'LGBT+ friendly',
            ]]
    
    
    # Renombramos las columnas
    nuevos_nombres = ['Link', '☕ Nombre', '🏙️ Ciudad', '🔓 Abierto Ahora', '💲 Nivel de precios','Latitud','Longitud', '⭐ Puntuación', '💬 Nº Comentarios', '🕐 Horario hoy', '📊 % Ocupación Ahora',
                      'Cerrado permanentemene', 'Cerrado temporalmente', #'Horario','Porcentaje de Ocupación', 
                      '🪑 Puedes sentarte', '☀️ Tiene terraza', '🍺 Sirve Cerveza', '🍷 Sirve vino', '🥪 Sirve desayunos/almuerzos', '🫒 Sirve aperitivos', '🍪 Sirve postres', '🚶‍♂️ Para llevar', 
                      '🙋‍♀️ Acepta reserva', '🐕‍🦺 Acepta perros', '🐕 Acepta perros fuera', '🛜 Tiene Wifi','🛜 Tiene Wifi Gratis', '🏳️‍🌈 LGBT+ friendly',
                     ]
    
    df.columns = nuevos_nombres
    
    df = filter_dataframe(df)
    
    # st.write('')
    # with st.expander("👀 Ver detalle de cafeterías por cercanía"):
    #     st.dataframe(df.drop(['Link', 'Latitud', 'Longitud', 'Cerrado permanentemene', 'Cerrado temporalmente'], axis=1))# df = df.drop_duplicates()
    
    dictio_coords_saviour = {'A Arnoia': '42.25708815, -8.140103499999999', 'A Bergueira': '42.3667652, -7.9713327', 'A Coruña': '43.35931967283019, -8.408809210188679', 'A Groba': '42.3143189, -8.0939238', 'A Gudiña': '42.058911699999996, -7.1433636499999995', 'A Manchica': '42.224468200000004, -7.92699195', 'A Pobra de Trives': '42.33941900000001, -7.2531991', 'A Pobra do Brollón': '42.5559915, -7.393168633333333', 'A Porriña': '42.5239083, -8.6381766', 'A Rúa': '42.39476532, -7.109764660000001', 'A Silva': '42.831987, -7.7451658', 'A Valenza': '42.3185108, -7.88170715', 'Abejar': '41.8059654, -2.7863609', 'Acebo': '40.2033636, -6.7166603', 'Adahuesca': '42.1446239, -0.0083713', 'Aeropuerto de los Rodeos': '28.4908052, -16.3540533', 'Aguas Nuevas': '38.918518750000004, -1.91993275', 'Aguilar de Campoo': '42.7930599875, -4.26182045', 'Alaquàs': '39.45579524615384, -0.45603970769230767', 'Alar del Rey': '42.6604632, -4.310896666666667', 'Albacete': '38.99396769451219, -1.8604693884146342', 'Albaladejo': '38.619095, -2.8105448', 'Albalat dels Sorells': '39.5439796, -0.3476004', 'Albalate de Zorita': '40.3072914, -2.8436451', 'Albalate del Arzobispo': '41.12166395, -0.5112047', 'Albarellos': '41.9490277, -7.4954226', 'Albarracín': '40.407931175, -1.4418352', 'Albentosa': '40.1035019, -0.768731', 'Alberca Las Torres': '37.94122805, -1.1474524750000001', 'Alboraya': '39.49771223333333, -0.34291486666666665', 'Alcalá de los Gazules': '36.4599205, -5.7229989', 'Alcalá del Obispo': '42.0767936, -0.2910567', 'Alcalá del Valle': '36.9029977, -5.170835', 'Alcantarilla': '37.95938313333333, -1.2163164', 'Alcaudete': '37.5908086, -4.0825846', 'Alcañices': '41.6994641, -6.3476807', 'Alcañiz': '41.050346266666665, -0.13218654000000002', 'Alcobendas': '40.537532506249995, -3.644522027083333', 'Alcolea': '37.9324378, -4.6725869', 'Alcolea de Cinca': '41.7194404, 0.117748', 'Alcolea del Pinar': '41.034336, -2.483005', "Alcora (L')": '39.9844579, -0.0449499', 'Alcorcón': '40.346937623076926, -3.8246613384615387', 'Alcorisa': '40.891921875, -0.382282725', 'Alcántara': '39.7135594, -6.8834611', 'Alcázar de San Juan': '39.39237252352941, -3.2141288529411765', 'Aldaia': '39.464053875000005, -0.460205225', 'Aldea del Rey': '38.7380926, -3.8387235', 'Alfafar': '39.421628157142855, -0.3900224571428571', 'Alfara del Patriarca': '39.54613776666667, -0.3855027', 'Algeciras': '36.129599940909095, -5.451225079545455', 'Algeciras, Cádiz': '36.1232321, -5.4402632', 'Algora': '40.9563192, -2.6649263', 'Algorta': '43.354168, -3.010696', 'Alhambra': '38.8995321, -3.053234', 'Alicante': '38.351139425, -0.4825341448275862', 'Alija del Infantado': '42.1394549, -5.8348798', 'Aljucer': '37.95673375, -1.1520158', 'Allariz': '42.189755059999996, -7.798886980000001', 'Almadrones': '40.898436, -2.7604716', 'Almadén': '38.77590516666667, -4.831611233333334', 'Almagro': '38.88943612857143, -3.710858657142857', 'Almazcara': '42.5982352, -6.5033174', 'Almazán': '41.4861031, -2.5306262333333334', 'Almería': '36.842224141358024, -2.444184687037037', 'Almodóvar del Campo': '38.7113609, -4.1773953', 'Almonacid de Zorita': '40.32352305, -2.8479994', 'Almudévar': '42.0391188, -0.5814069', 'Almàssera': '39.512481466666664, -0.3572853833333333', 'Alovera': '40.589690700000006, -3.2480645', 'Alquerías': '38.01360673333333, -1.0354416333333332', 'Alquézar': '42.172219375, 0.02536625', 'Altafulla': '41.1413274, 1.3460283', 'Alumbres': '37.6043609, -0.9153767', 'Ampudia': '41.9172999, -4.7794893', 'Amusco': '42.1724281, -4.4713058', 'Andorra': '41.10512500714286, -0.4517797642857143', 'Aneiros ,Ferrol': '43.5002714, -8.2422635', 'Ansoáin': '42.83162675, -1.6375133499999999', 'Ansó': '42.7557431, -0.8289101', 'Antas de Ulla': '42.782454099999995, -7.8907459499999995', 'Aranzueque': '40.49217, -3.07671', 'Arcenillas': '41.4814406, -5.7019707', 'Arcos de Jalón': '41.226355866666665, -2.2548016', 'Arcos de la Frontera': '36.7551052, -5.81028066', 'Arcos de la Polvorosa': '41.9439071, -5.7002105', 'Ardea': '41.727467, 12.508821', 'Areeta (Getxo)': '43.3260711, -3.0139231', 'Arenals del Sol': '38.251796850000005, -0.5183434499999999', 'Arenas de San Juan': '39.2191853, -3.5041915', 'Arenillas de Nuño Pérez': '42.516314, -4.5311106', 'Argamasilla de Alba': '39.1290317, -3.0900646333333337', 'Argamasilla de Calatrava': '38.72746996666667, -4.0802077', 'Armunia': '42.578793, -5.58787', 'Arnuíde': '42.1966645, -7.6081339', 'Arquillos': '38.1820655, -3.4309652', 'Arroyo De La Vega': '40.530445, -3.638562', 'Arroyo Frio': '37.9462398, -2.9206735', 'Arroyo de la Luz': '39.48068766666666, -6.581768333333334', 'Arén': '42.253479, 0.7315558', 'As Campiñas': '42.9761179, -7.5622911', 'As Nogais': '42.8102803, -7.11054695', 'Astorga': '42.45767355, -6.058464675', 'Astudillo': '42.19293495, -4.2933407500000005', 'Astún': '42.80929108, -0.5039525599999999', 'Atienza': '41.199778, -2.8709096', 'Avileses': '37.8476863, -0.9445742', 'Avilés': '43.55286543295455, -5.921562445454546', 'Ayerbe': '42.2762871, -0.6895295', 'Ayoó de Vidriales': '42.1306591, -6.0661631', 'Azucaica': '39.8838045, -3.9734657', 'Azuqueca de Henares': '40.5658762, -3.2656561272727274', 'Aínsa': '42.41475916666667, 0.14359746666666667', 'Badajoz': '38.874810194594595, -6.976294775675676', 'Badalona': '41.44967363469387, 2.236860312244898', 'Baeza': '37.995315399999996, -3.4697106933333335', 'Bailén': '38.09501313, -3.777121', 'Bajamar': '28.5560025, -16.3356064', 'Balcon de Telde': '28.0263073, -15.4218569', 'Baltanás': '41.9378961, -4.2464796', 'Bande': '42.0320019, -7.9752946', 'Baracaldo': '43.290894300000005, -2.98567875', 'Barajas': '40.47561458, -3.57947958', 'Barakaldo': '43.292550786585366, -2.989846254878049', 'Baralla': '42.8938241, -7.250885', 'Barbadás': '42.31632722857143, -7.882901628571429', 'Barbastro': '42.03541387142857, 0.12646596428571427', 'Barbate': '36.18906846363637, -5.921519459090908', 'Barcelona': '41.39942715652174, 2.1666052008152175', 'Barco (O)': '42.4182773, -6.9905149', 'Barking': '51.53698585, 0.08710231666666667', 'Barqueros': '37.940859, -1.3707157', 'Barral': '42.2960934, -8.0942368', 'Barriada Río San Pedro': '36.51922435, -6.2313375', 'Barrio': '38.8434263, -6.9682251', 'Barruelo de Santullán': '42.908028933333334, -4.288699966666667', 'Base Aerea Conjunta Torrejón': '40.4794997, -3.4424855', 'Baños de Montemayor': '40.3189048, -5.8582194', 'Beas de Segura': '38.254954966666666, -2.8989985666666667', 'Becerreá': '42.853390024999996, -7.1620365', 'Beckenham': '51.40586378571429, -0.02888294285714286', 'Begíjar': '37.9853839, -3.5312602', 'Bellavista': '37.3226108, -5.9681959', 'Belvedere': '51.4914615, 0.1508589', 'Belver de Cinca': '41.6927327, 0.1797619', 'Belvís de Monroy': '39.8193258, -5.6088495', 'Bembibre': '42.61679496666667, -6.417519025', 'Benabarre': '42.108117166666666, 0.48607079999999997', 'Benalup-Casas Viejas': '36.34367966666667, -5.810055599999999', 'Benasque': '42.6039198, 0.5231539666666667', 'Benavente': '42.00317287826087, -5.676131339130435', 'Benavides de Órbigo': '42.50179075, -5.89483295', 'Benetússer': '39.42164126153846, -0.3969357', 'Beniaján': '37.9759952, -1.070431', 'Benlloch': '39.5154278, -0.4243857', 'Berlanga de Duero': '41.464378, -2.8604726', 'Bermillo de Sayago': '41.365918, -6.112139233333333', 'Bernueces': '43.5188979, -5.6293182', 'Berriozar': '42.83434535, -1.6716538', 'Betote': '42.8015927, -7.4123665', 'Bexley': '51.440301266666665, 0.14475058333333332', 'Bexleyheath': '51.4574757, 0.140995975', 'Bielsa': '42.6350064, 0.2181759', 'Biescas': '42.628150149999996, -0.32205325', 'Bilbao': '43.26211947838983, -2.9337297305084746', 'Binéfar': '41.849194340000004, 0.29457883999999995', 'Boadilla del Monte': '40.41454893333333, -3.8765289499999995', 'Bolaños de Calatrava': '38.90588041666667, -3.6571757333333337', 'Boltaña': '42.4353711, 0.0871539', 'Bonanza': '36.798203, -6.3367141', 'Bonavista': '41.1200445, 1.1948172', 'Bonfim': '41.1542678, -8.5959519', 'Bonrepòs i Mirambell': '39.5177783, -0.36459346666666664', 'Boqueixon': '42.8920311, -8.419247', 'Bornos': '36.8193085, -5.7430403000000005', 'Boñar': '42.8658254, -5.3236521', 'Brentford': '51.48700434166667, -0.30552958333333335', 'Bretó': '41.8778533, -5.7375493', 'Brihuega': '40.7615353, -2.86902235', 'Broadway': '51.512961, -0.3025954', 'Bromley': '51.40028562162163, 0.020055324324324324', 'Bronchales': '40.5081097, -1.5865472', 'Broto': '42.6040428, -0.1218488', 'Brozas': '39.614177925, -6.7743728', 'Burgos': '42.34686996533333, -3.686416834', 'Burjassot': '39.50964039230769, -0.4136154615384615', 'Burunchel': '37.94682903333333, -2.9512444666666666', 'Bustillo del Páramo': '42.4410473, -5.79062105', 'Bóveda': '42.6543617, -7.4775596', "Ca'n Pastilla": '39.533094028571426, 2.723473042857143', 'Cabanillas del Campo': '40.63168511428571, -3.2276431571428574', 'Cabezabellosa': '40.1385126, -6.0014591', 'Cabezo de Torres': '38.0250948, -1.124715875', 'Cabo de Gata': '36.7806318, -2.2433897', 'Cabo de Palos': '37.63232775, -0.70434925', 'Caboalles de Abajo': '42.9517729, -6.3718465', 'Cabrejas del Pinar': '41.7952002, -2.849622', 'Cacabelos': '42.59840809999999, -6.724931842857143', 'Calaceite': '41.0152852, 0.1886673', 'Calafell': '39.5082639, 2.7528032', 'Calamocha': '40.92010775, -1.2974614500000001', 'Calanda': '40.9413298, -0.2339329', 'Calero (El)': '27.9957601, -15.3960662', 'Calvos de Randín': '41.946877, -7.8970688', 'Calzada de Calatrava': '38.704041399999994, -3.77617775', 'Calzadilla': '40.0574964, -6.5341958', 'Calzadilla de la Cueza': '42.328564, -4.80447', 'Cambados': '42.5194137, -8.8167788', 'Caminomorisco': '40.3265258, -6.29060475', 'Caminreal': '40.8379704, -1.3071357', 'Campanhã': '41.1554807, -8.5713936', 'Campazas': '42.1419316, -5.493746', 'Campillo de Arenas': '37.5553226, -3.635106', 'Campo': '42.409430349999994, 0.39637469999999997', 'Campo de Criptana': '39.40283903333333, -3.1266859166666663', 'Camponaraya': '42.578531133333335, -6.671107766666666', 'Canales': '42.7841021, -5.7996205', 'Canals': '38.963939075, -0.5847714166666667', 'Candanchú': '42.7823833, -0.53232955', 'Candasnos': '41.51859566, 0.04047252', 'Canena': '38.0516614, -3.4867458', 'Canfranc-Estación': '42.7520426, -0.5152145', 'Canredondo': '40.8131878, -2.4943294', 'Canteras': '37.61206586666667, -1.0419923666666666', 'Caraquiz': '40.7875879, -3.4902642', 'Carbajales de Alba': '41.6527597, -5.9963113', 'Carcaboso': '40.0498452, -6.2176541', 'Carrión de Calatrava': '39.01811385, -3.81734625', 'Carrión de los Condes': '42.3375785, -4.603724166666667', 'Carrus': '38.2789635, -0.7194694', 'Carshalton': '51.367220225, -0.1730855', 'Cartagena': '37.621564778527606, -0.9785270920245399', 'Cartuja Baja': '41.60473165, -0.82432345', 'Carucedo': '42.49004, -6.76744', 'Casar de Cáceres': '39.56058935, -6.41862785', 'Casar de Talavera (El)': '39.9619146, -4.9147711', 'Casas Nuevas': '27.9940119, -15.390981525', 'Casas de Don Gómez': '40.0074199, -6.5993654', 'Casas del Castañar': '40.1084022, -5.8961338', 'Casaseca de las Chanas': '41.4377592, -5.6746592', 'Casatejada': '39.88595205, -5.68319915', 'Cascón de la Nava': '42.0563935, -4.6444739', 'Castejón': '42.14228574, -1.69741404', 'Castejón de Sos': '42.5125386, 0.4925354', 'Castel Romano': '41.71554245, 12.44515105', 'Castellar de Santiago': '38.53950725, -3.27836775', 'Castellón de la Plana': '39.98502614605263, -0.0428149125', 'Castillazuelo': '42.0684204, 0.0655224', 'Castrillo de Don Juan': '41.7912909, -4.070834', 'Castrillo de la Ribera': '42.5457752, -5.5472529', 'Castro Caldelas': '42.37457303333333, -7.4161500333333334', 'Castro de Ribeiras': '43.1410821, -7.4934137', 'Catarroja': '39.40834274, -0.40544234', 'Cazorla': '37.91301325, -3.0022980833333333', 'Ceclavín': '39.82115835, -6.77559035', 'Cedofeita': '41.1620613, -8.6300791', 'Cedrillas': '40.4363054, -0.8525654', 'Celanova': '42.1524659, -7.956869630769232', 'Cella': '40.4542736, -1.287146', 'Cerro Muriano': '38.00344115, -4.768909', 'Cervera de Pisuerga': '42.864858725, -4.49821045', 'Chantada': '42.60966405333333, -7.77039182', 'Chapela': '42.257939, -8.6742727', 'Chessington': '51.346396975000005, -0.313036425', 'Chiclana de la Frontera': '36.41542557037037, -6.149041503703704', 'Chilluévar': '38.001901366666665, -3.031916633333333', 'Chillón': '38.7965724, -4.8651931', 'Chipiona': '36.7365202, -6.4284145', 'Chislehurst': '51.416287142857136, 0.06465552857142857', 'Churra': '38.03457778, -1.1454428399999999', 'Ciampino': '41.79946125, 12.59038365', 'Cifuentes': '40.7834243, -2.6241526', 'Cilleros': '40.1144833, -6.7929984', 'Cimanes de la Vega': '42.1194117, -5.5966863', 'Cisneros': '42.2214327, -4.8574241', 'Cistierna': '42.8030551, -5.1294286', 'Ciudad Quesada': '38.0376802, -0.7055148', 'Ciudad Real': '38.988141775, -3.9126477033333336', 'Cobatillas': '38.0527951, -1.0808707499999999', 'Cogolludo': '40.9473308, -3.0889489', 'Coles': '42.41317295, -7.8556102', 'Collado Villalba': '40.62889060689655, -4.006730355172414', 'Collonades': '51.35591, -0.1154', 'Colloto': '43.377519175, -5.7995711750000005', 'Colungo': '42.172741, 0.065453', 'Conchel': '41.8851202, 0.1445512', 'Congosto': '42.6172611, -6.5189569', 'Conil de la Frontera': '36.28793880625, -6.08725996875', 'Coria': '39.98630912857143, -6.536394542857143', 'Cornellà de Llobregat': '41.3555910125, 2.0773028333333334', 'Corredoria': '43.3849186, -5.823104166666667', 'Cortes': '42.3389737, -3.6895016', 'Cortijos Nuevos': '38.2467545, -2.7262274', 'Corvera': '37.8257199, -1.15962', 'Coslada': '40.42620416756757, -3.5517938', 'Coto de Bornos': '36.849218, -5.6935842', 'Coto-Ríos': '38.0469145, -2.8487742', 'Coulsdon': '51.317472175, -0.133419575', 'Covaleda': '41.9344123, -2.8815256', 'Coy': '37.9486244, -1.8122944', 'Cp': '28.4529164, -16.2838771', 'Cretas': '40.9229859, 0.2136514', 'Croydon': '51.373842208571425, -0.08881808000000001', 'Ctra. Acceso Central Térmica N: S/N': '36.1819471, -5.4371755', 'Cualedro': '41.986986375, -7.58035305', 'Cuenca': '40.068779464705884, -2.1353676686274508', 'Cuesta Blanca': '37.64264215, -1.0953062500000001', 'Cuevas de Almudén': '40.7132269, -0.8298109', 'Curbe': '41.907371, -0.312771', 'Cáceres': '39.47134537816092, -6.376309583908046', 'Cádiz': '36.526413873563214, -6.274857685057471', 'Córdoba': '37.88608491962617, -4.781265535514019', 'Dacón': '42.42215825, -8.0489783', 'Dagenham': '51.552345679999995, 0.14286287999999997', 'Daimiel': '39.0683077, -3.611267114285714', 'Dartford': '51.45047928, 0.17992574', 'Donadío': '37.9275544, -3.3650207', 'Donostia-San Sebastian': '43.313913859124085, -1.9806090014598539', 'Dos Hermanas': '37.29192572666667, -5.927649404', 'Duruelo de la Sierra': '41.9552996, -2.9312931', 'El Albujón': '37.71832023333334, -1.0475134', 'El Algar': '37.64657226, -0.86691512', 'El Alquián': '36.85274121428571, -2.3544686', 'El Arenal': '39.5068708, 2.7532191', 'El Burgo Ranero': '42.4215963, -5.2182497', 'El Burgo de Osma': '41.5872582, -3.067740325', 'El Casar': '40.7028646, -3.4323835000000003', 'El Casar de Talavera': '39.953789, -4.9074781', 'El Chaparral': '38.016104150000004, -0.6988627000000001', 'El Cuervo': '36.85120513333334, -6.040427066666666', 'El Esparragal': '38.0459302, -1.083015', 'El Gastor': '36.854586133333335, -5.3215882', 'El Grado': '42.1441945, 0.2266248', 'El Grao de Castellón': '39.97698061111111, 0.014212577777777778', 'El Higueron': '37.869619, -4.8542245', 'El Palmar': '37.938154016666665, -1.1655313166666665', 'El Pinar': '36.5309279, -6.1987537', 'El Poblenou': '41.5612738, 2.1285507', 'El Portal': '36.6350033, -6.1314626', 'El Poyo del Cid': '40.8833323, -1.3332181', 'El Puerto de Sta María': '36.59591840666667, -6.231946753333333', 'El Puntal': '38.0158033, -1.14844525', 'El Raal': '38.039638266666664, -1.0344383', 'El Robledo': '39.2172742, -4.28396675', 'El Rosario': '28.4197349, -16.3203926', 'El Torno': '39.2544026, -4.2573204', 'El Zabal': '36.182625, -5.3498114', 'El pilar': '41.1176326, 1.2131901', 'Elche': '38.26780385649351, -0.6967227350649351', 'Elche Parque Industrial': '38.2909536, -0.6120989', 'Enfield': '51.65410817647059, -0.06584039411764706', 'Entrimo': '41.933034, -8.1188032', 'Erith': '51.486859100000004, 0.16180203333333334', 'Es Pil·larí': '39.52596, 2.7345697', 'Es Secar de la Real': '39.6067711, 2.6440078', 'Escarrilla': '42.7336769, -0.31328465', 'Esgos': '42.318517150000005, -7.6874248000000005', 'Espera': '36.8717085, -5.8060656999999996', 'Espinardo': '38.010557883333334, -1.1537594833333333', 'Estación': '39.719773675, -0.46073474999999986', 'Estación Linares-Baeza': '38.0687716, -3.5894427', 'Estación de Medinaceli': '41.1660348, -2.4215815', 'Estadilla': '42.0557461, 0.2416486', 'Estella del Marqués': '36.6862142, -6.0794687', 'Esteras de Medinaceli': '41.107432, -2.4450739', 'Estrecho de San Gines': '37.6296074, -0.8288571', 'Fabero': '42.7667765, -6.627059975', 'Facinas': '36.1423813, -5.6984129', 'Fariza': '41.420664, -6.2710391', 'Feltham': '51.4491169, -0.41645504285714285', 'Fermoselle': '41.31826256666667, -6.398144866666667', 'Ferreira de Pantón': '42.5054881, -7.6257091', 'Ferrol': '43.48838615607477, -8.225633858878505', "Foia d'Elx": '38.21207375, -0.68345275', 'Foios': '39.536958049999996, -0.35292', 'Fontanar': '40.7211263, -3.171838', 'Formigal': '42.773563, -0.3604418', 'Fortanete': '40.5027154, -0.5195523', 'Fraga': '41.52154224375, 0.33732396875', 'Fresno de la Ribera': '41.5289916, -5.5654101', 'Friamonde': '42.69479, -7.7023159', 'Frómista': '42.26641385, -4.40644525', 'Fuenlabrada': '40.287100390361445, -3.797767201204819', 'Fuenllana': '38.7566123, -2.9588705', 'Fuente el Fresno': '39.230299224999996, -3.77404655', 'Fuentelahiguera de Albatages': '40.7851835, -3.307653', 'Fuentelapeña': '41.2525956, -5.3828317', 'Fuentes de Nava': '42.0834, -4.7846399', 'Galapagar': '40.57776835, -4.003897707142857', 'Galisteo': '39.9739425, -6.2657642', 'Galiñáns': '42.4383955, -8.778981', 'Gargüera': '40.06174, -5.92887', 'Garrovillas': '39.709745100000006, -6.5485387500000005', 'Gata': '40.2374551, -6.5966397', 'Gea y Truyols': '37.8477738, -1.0410842', 'Germans Sàbat': '41.9951024, 2.8069758', 'Getafe': '40.308838217857144, -3.7264821589285715', 'Getxo': '43.34240160967742, -3.010334016129032', 'Gijón': '43.5338167045977, -5.667527423371647', 'Girona': '41.97899764090909, 2.818326618939394', 'Godella': '39.520899299999996, -0.4152584666666666', 'Golmayo': '41.7742552, -2.5003592', 'Gordoncillo': '42.1352048, -5.4013116', 'Granada': '37.17808149240506, -3.6034549312236286', 'Graus': '42.20116308, 0.32790432', 'Grazalema': '36.7584692, -5.365649966666666', 'Grañén': '41.9392547, -0.3693688', 'Greater': '51.3774, 0.103827', 'Greenford': '51.53334805, -0.32123840000000004', 'Guadacorte': '36.1891114, -5.4323192', 'Guadalajara': '40.632373856, -3.1647458360000003', 'Guadalcacín': '36.7280497, -6.090190666666667', 'Guadalupe de Maciascoque': '37.9979708, -1.1758043', 'Guamasa': '28.491696375, -16.36837485', 'Guardo': '42.789253, -4.844712876923077', 'Guarromán': '38.1825937, -3.6879601', 'Gustei': '42.3970098, -7.853754', 'Hampton': '51.42718060000001, -0.3556418666666667', 'Hanwell': '51.4964405, -0.3252897', 'Harrow': '51.57952378571429, -0.32837454285714285', 'Hayes': '51.50508958, -0.41842155999999997', 'Herencia': '39.36755, -3.3540527599999996', 'Herrera de Pisuerga': '42.595713, -4.3306930999999995', 'Hervás': '40.27242114, -5.861490519999999', 'Hinojares': '37.7154795, -2.9998152', 'Hontoria': '40.90712045, -4.11139695', 'Horcajo de los Montes': '39.326990550000005, -4.65120925', 'Hornchurch': '51.55987631333333, 0.21317141333333334', 'Hornos': '38.217057, -2.720558', 'Hospital de Órbigo': '42.4614755, -5.879544800000001', "Hospitalet de Llobregat (L')": '41.3602236, 2.0798001', 'Hounslow': '51.47146347352941, -0.4313221823529412', 'Huelva': '37.26272268157895, -6.9426139289473685', 'Huergas de Babia': '42.956809, -6.092531', 'Huesca': '42.149762525, -0.392696121875', 'Humanes': '40.8277361, -3.1539036', 'IMEPE': '40.3368449, -3.8174337', 'Ibros': '38.02125313333333, -3.5027163', 'Igüeña': '42.7287826, -6.2781801', 'Ilford': '51.569143706666665, 0.08242901333333334', 'Isla Plana': '37.574714349999994, -1.2107659499999999', 'Isla de': '38.1664695, -0.4830773', 'Isleworth': '51.473945, -0.322897', 'Iznatoraf': '38.15688645, -3.0333475500000002', 'Jabalquinto': '38.0195037, -3.7280984', 'Jaca': '42.571529940909095, -0.5489699727272727', 'Jadraque': '40.9258015, -2.9249613', 'Jarandilla de la Vera': '40.12859345, -5.6626861', 'Jaraíz de la Vera': '40.05899502, -5.7538598400000005', 'Jarilla': '40.1857753, -6.0065037', 'Javalí Nuevo': '37.9860582, -1.2181222', 'Javalí Viejo': '37.98950285, -1.20260185', 'Jaén': '37.78014886506024, -3.7918087891566263', 'Jerez de la Frontera': '36.686790102912624, -6.131552945631069', 'Jerte': '40.2061724, -5.771634', 'Josa': '40.9557537, -0.7668081', 'Jubilee': '51.5051638, -0.0196044', 'Jódar': '37.841471766666665, -3.3526539', 'Keston': '51.3623051, 0.02802445', 'Kingston upon Thames': '51.41493991875, -0.2999121375', "L'Altet": '38.27275336666667, -0.5408746333333333', 'La Aljorra': '37.692539749999995, -1.0689392500000001', 'La Aparecida': '37.6685846, -0.9549697', 'La Barca de la Florida': '36.64865622, -5.9334001800000005', 'La Bañeza': '42.30139615384615, -5.898397030769231', 'La Bóveda de Toro': '41.340928, -5.4097826', 'La Camocha': '43.4870666, -5.6503469', 'La Carolina': '38.2736747, -3.6115786500000002', 'La Cañada': '36.83500601428572, -2.4051000714285715', 'La Cueva': '38.0253802, -1.0896568', 'La Escucha': '37.5441314, -1.6931923', 'La Estación': '41.2245684, -0.4390448', 'La Fortuna': '40.357649699999996, -3.7786475', 'La Garita': '28.00791265, -15.3776839', 'La Herradura': '27.992987, -15.4350965', 'La Hoya': '37.71072905, -1.59452535', 'La Iruela': '37.9222916, -2.9921952', 'La Laguna': '28.481307314166667, -16.314221861666667', 'La Línea de la Concepción': '36.16448798181818, -5.350248518181818', 'La Magdalena': '42.7844675, -5.7981246', 'La Manga': '37.655424933333336, -0.7206012666666667', 'La Manga Club': '37.6006615, -0.8043504', 'La Martina': '42.54151575, -6.63227355', 'La Mata': '38.017649166666665, -0.6552972', 'La Palma': '37.6892544, -0.9628415', 'La Pardilla': '28.0231902, -15.3883478', 'La Puebla': '37.7179946, -0.9204093', 'La Puebla de Valverde': '40.2200172, -0.9401012', 'La Puerta de Segura': '38.349997200000004, -2.7375957', 'La Solana': '38.94299157142857, -3.236368257142857', 'La Virgen del Camino': '42.580659025, -5.6412983', 'La Ñora': '37.9910631, -1.1910265500000001', 'Laderas del Campillo': '38.046154, -1.0828412', 'Lampaza': '42.1044648, -7.8639549', 'Langa de Duero': '41.609973, -3.4010461', 'Larouco': '42.3466096, -7.1623696', 'Las Campas': '43.3651241, -5.8860295', 'Las Huesas': '27.98419255, -15.392543799999999', 'Las Medianias': '27.9800963, -15.4266272', 'Las Mercedes': '28.5156187, -16.302004349999997', 'Las Palmas de Gran Canaria': '28.129645660162602, -15.430950703252032', 'Las Remudas': '28.009833, -15.390083', 'Las Rozas de Madrid': '40.50548222857143, -3.8859199964285716', 'Laza': '42.060358, -7.4650271', 'Leganés': '40.333947937000005, -3.757634225', 'Leiro': '42.370119, -8.1250664', 'Les Baies': '38.21929973333334, -0.6439075666666666', 'Leystonstone': '51.5695, 0.012202', 'León': '42.599584804651165, -5.575564213953489', 'Linares': '38.09523885945946, -3.634189772972973', 'Lincoln': '53.22896717439024, -0.5418955', 'Llano de Brujas': '38.0048897, -1.07197', 'Lleida': '41.61688401521739, 0.6256506760869565', 'Lodares': '41.1894198, -2.4015557', 'Logroño': '42.462202311695904, -2.4483244959064328', 'Lombillo de los Barrios': '42.5172511, -6.5424978', 'London': '51.50008564821429, -0.13242266535714287', 'Londres': '51.517295499999996, -0.0735433', 'Loporzano': '42.2012704, -0.3111731', 'Lorca': '37.6701947442623, -1.6944428196721313', 'Los Barrios': '36.18263614166667, -5.467576866666666', 'Los Belones': '37.62284554, -0.77634642', 'Los Cortijillos': '36.18720365, -5.4383461', 'Los Dolores': '37.9767609, -1.1054764', 'Los Martínez del Puerto': '37.8183012, -1.078573', 'Los Moriscos': '27.93768815, -15.389333650000001', 'Los Nietos': '37.6499943, -0.7865', 'Los Ramos': '37.9915497, -1.0369327', 'Los Rábanos': '41.7181739, -2.4754613', 'Los Villares': '37.6883309, -3.818507285714286', 'Losar de la Vera': '40.12096006666667, -5.607044866666667', 'Lubián': '42.034718, -6.8429904', 'Lugo': '43.00738203163265, -7.556781552040817', 'Láncara': '42.86465423333333, -7.4450718333333334', 'Lérida': '41.622000025, 0.6299593', 'Línea De La Concepción ( La )': '36.1610759, -5.348501', 'Maceda': '42.27020084285714, -7.650124414285714', 'Madrid': '40.424607675123156, -3.685111448522167', 'Madridanos': '41.4782642, -5.6048459', 'Madrigal de la Vera': '40.14764726666667, -5.3690527', 'Majadahonda': '40.47223782647058, -3.8762876000000004', 'Malagón': '39.168119274999995, -3.8531882', 'Maliaño': '43.4430572, -3.8465251', 'Malpartida de Plasencia': '39.9315499, -6.16073315', 'Mancha Real': '37.786231975, -3.6083306', 'Manises': '39.492391386363636, -0.46510985909090913', 'Mansilla de las Mulas': '42.4974167, -5.416360324999999', 'Mantiel': '40.6188438, -2.6620595', 'Manzanal del Puerto': '42.5991984, -6.2298737', 'Manzanares': '39.00126258125, -3.37064789375', 'Manzaneda': '42.3099743, -7.2338635', 'Maqueda': '36.7328356, -4.5655318', 'Marbella': '36.50773136569343, -4.895492078832117', 'Marchamalo': '40.66936105, -3.2031919', 'Marpequeña': '28.002512425, -15.3894131', 'Martos': '37.717579125, -3.971626035', 'Martín del Río': '40.8438748, -0.8967835', 'Marín': '42.3899131, -8.7018238', 'Mas de las Matas': '40.828714, -0.240474', 'Masegoso de Tajuña': '40.8251599, -2.69554', 'Maside': '42.41197815, -8.02667885', 'Massanassa': '39.412382789999995, -0.39762933', 'Matarrosa del Sil': '42.7560633, -6.5316445', 'Mataró': '41.541815953333334, 2.43999132', 'Matas-Pinar-Monte Rozas ( Las )': '40.5320189, -3.8900343', 'Matola': '38.2268002, -0.7456967', 'Medina-Sidonia': '36.456324, -5.9275193', 'Medinaceli': '41.168654450000005, -2.42148045', 'Meliana': '39.529047659999996, -0.35085842', 'Membrilla': '38.96384004, -3.3681370999999998', 'Membrío': '39.5273027, -7.0518776', 'Mengíbar': '37.96922922, -3.80613034', 'Miajadas': '39.1523145, -5.9082029', 'Middlesex': '51.4617086, -0.4452057', 'Miguelturra': '38.95916901818182, -3.884678090909091', 'Mirabel': '39.8609069, -6.2336964', 'Miranda': '37.6767971, -1.0208957', 'Mislata': '39.476444735, -0.419110695', 'Mitcham': '51.4001766, -0.1694298', 'Mogón': '38.0740932, -3.0316682', 'Mohedas de Granadilla': '40.2673613, -6.2025114666666665', 'Molina de Aragón': '40.842620350000004, -1.8879446', 'Moncada': '39.546481568749996, -0.39480060625', 'Mondéjar': '40.3228638, -3.1105099', 'Monfarracinos': '41.5505294, -5.7047465', 'Monforte de Lemos': '42.52097885925926, -7.51370545925926', 'Monreal del Campo': '40.7552823, -1.3387225', 'Montalbán': '40.8326503, -0.7989974', 'Montamarta': '41.6497772, -5.8042939', 'Monteagudo': '38.0195308, -1.0956287', 'Monteagudo de las Vicarías': '41.3655199, -2.1701', 'Montehermoso': '40.08824945, -6.3514041', 'Montejos del Camino': '42.584327, -5.6896317', 'Montequinto': '37.33837235, -5.93099731', 'Monterde de Albarracín': '40.49761, -1.49255', 'Monterroso': '42.792857525, -7.83472805', 'Montiel': '38.69834165, -2.8663411500000002', 'Monzón': '41.91234650909091, 0.19266224545454547', 'Mora de Rubielos': '40.2511438, -0.7532404', 'Moraleja': '40.06606834285714, -6.6612867571428565', 'Moraleja del Vino': '41.465252199999995, -5.6578817', 'Morales de Toro': '41.5358093, -5.3075686', 'Morales del Vino': '41.44323236666667, -5.7351434999999995', 'Moralina': '41.4895545, -6.1387034', 'Morden': '51.4020202, -0.19511703333333333', 'Moreiras': '42.3002731, -7.9200154', 'Morón de Almazán': '41.41263, -2.41193', 'Mugueimes': '41.957074866666666, -7.972773766666667', 'Murcia': '37.982644666666666, -1.127306750925926', 'Museros': '39.5655029, -0.3415109', 'Mutilva': '42.8045951, -1.6222925', 'Málaga': '36.71417034545454, -4.443067285521885', 'Mérida': '38.91681533529412, -6.344387509803921', 'Móstoles': '40.324170957142854, -3.864314089010989', 'Narón': '43.4886043, -8.2035097', 'Navalmoral de la Mata': '39.89146728, -5.542735733333333', 'Navas de San Juan': '38.181636749999996, -3.3151696499999996', 'Navas del Madroño': '39.6232446, -6.6512445', 'New Malden': '51.398718145454545, -0.2537318090909091', 'Noceda': '42.7141389, -6.3997056', 'Northwood': '51.611823, -0.425224', 'Nueno': '42.2450828, -0.4452331', 'Nueva Jarilla': '36.7599921, -6.0330811', 'Nuñomoral': '40.4066064, -6.2479253', 'O Barco': '42.416273499999996, -6.988247584615385', 'O Carballiño': '42.430575770588234, -8.078441688235294', 'O Corgo': '42.93647582, -7.436068539999999', 'O Cotón': '42.8750886, -7.9051913', 'Ofra': '28.452378, -16.2866844', 'Oia': '42.1896769, -8.7999621', 'Ojos Negros': '40.7378018, -1.4986517', 'Ojos de Garza': '27.9463042, -15.39389605', 'Olleros de Sabero': '42.8302724, -5.1830919', 'Olvera': '36.9339532, -5.25957275', 'Onzonilla': '42.5439867, -5.5637956', 'Oporto': '41.1659195, -8.5950563', 'Orbón': '43.5577306, -5.9232237', 'Orcera': '38.317592700000006, -2.6632711000000002', 'Orpington': '51.375295003846155, 0.08323821538461539', 'Ortigal': '28.471132, -16.376971', 'Osorno': '42.40934955, -4.36224535', 'Ostia': '41.733864454545454, 12.278892086363635', 'Ostia Antica': '41.7597011, 12.3020852', 'Otero de Bodas': '41.9367058, -6.1499363', 'Ourense': '42.3419908415493, -7.862884305633802', 'Outeiro de Rei': '43.055424, -7.608391', 'Outomuro': '42.2253718, -8.0185495', 'Oviedo': '43.36508059897436, -5.84789066', 'Padornelo': '42.0334604, -6.8368616', 'Padrenda': '42.144678266666666, -8.177335833333332', 'Padrenda de Abaixo': '42.4680017, -8.7994057', 'Paiporta': '39.428043522222225, -0.4161973666666667', 'Palas de Rei': '42.8730853, -7.86950955', 'Palencia': '42.00696751967214, -4.527581191803279', 'Palma': '39.573502170903005, 2.659054004013378', 'Palmones': '36.17542253333334, -5.436960766666666', 'Pamplona': '42.81446789268293, -1.6490197115853658', 'Panticosa': '42.722338, -0.281177', 'Paradela': '42.9187884, -8.5300951', 'Paredes de Nava': '42.1521833, -4.69472605', 'Pareja': '40.5566664, -2.6495201', 'Parla': '40.238003463157895, -3.7672410868421053', 'Parque de La Laguna': '42.4602698, -2.4612372', 'Parquelagos': '40.5957581, -3.9588961', 'Pastrana': '40.4173002, -2.9236993', 'Paterna': '39.511094609375, -0.440431525', 'Peal de Becerro': '37.913989, -3.1193029', 'Pedrafita do Cebreiro': '42.7126213, -7.1260455', 'Pedro Muñoz': '39.403384433333336, -2.9514408999999997', 'Peque': '42.0735836, -6.2741493', 'Peracense': '40.6407424, -1.4706565', 'Peraleda de San Román': '39.7403936, -5.3868466', 'Peralejos': '40.4840473, -1.032192', 'Perales de Tajuña': '40.4069304, -3.6692929', 'Perazancas': '42.7853715, -4.4215998', 'Perleta': '38.2504874, -0.6328483', 'Peñarroya de Tastavíns': '40.7699155, 0.0327604', 'Picanya': '39.434414275, -0.43405415', 'Piedrabuena': '39.03384995, -4.1720615', 'Pielas': '42.51854, -7.9626799', 'Pinner': '51.57757296666667, -0.3981519333333334', 'Pinofranqueado': '40.3019162, -6.3337202', 'Piornal': '40.1178139, -5.84932875', 'Pioz': '40.4638037, -3.17800165', 'Plasencia': '40.03185189411765, -6.088014052941176', 'Plasencia del Monte': '42.2265273, -0.5818633', 'Poblado de Sancti Petri': '36.3816069, -6.1955455', 'Pobladura de Pelayo Garcia, Leon': '42.3064111, -5.6867738', 'Pobladura del Valle': '42.103208, -5.734892', 'Poblete': '38.936928449999996, -3.98045495', 'Pol. Ind. El Goro': '27.9669579, -15.3908871', 'Pol. Ind. Pla de la Vallonga': '38.3516901, -0.5569608', 'Poligono Industrial de Constantí': '41.1313614, 1.2017585', 'Ponferrada': '42.54912822328767, -6.598824263013698', 'Ponte Galeria-la Pisana': '41.818699699999996, 12.3484631', 'Pontevedra': '42.42860158333333, -8.639992716666667', 'Port Saplaya': '39.511089, -0.32128535', 'Porto': '41.15491757752294, -8.616797720183486', 'Portomarín': '42.8071157, -7.61583695', 'Porzuna': '39.1479101, -4.1537301', 'Pozo Alcón': '37.701992, -2.9331429', 'Pozo Estrecho': '37.71138773333333, -0.9926996666666666', 'Pozuelo de Alarcón': '40.43944499333334, -3.7998061066666664', 'Pozuelo de Calatrava': '38.91275986666667, -3.836501933333333', 'Pozuelo de Vidriales': '42.0390123, -5.9632463', 'Prado del Rey': '36.7845763, -5.5582263', 'Puebla de Sanabria': '42.0523952, -6.632892725', 'Puebla de Trives': '42.3393146, -7.2537201', 'Puebla del Príncipe': '38.5659895, -2.9288657', 'Puente Tocinos': '37.9907092, -1.1027494', 'Puente Villarente': '42.5455622, -5.4590078', 'Puente de Domingo Flórez': '42.4113222, -6.8193847', 'Puente de Génave': '38.355764699999995, -2.8002493499999996', 'Puenteareas': '42.059286, -7.137608', 'Puerto Lápice': '39.299017375, -3.4621941', 'Puerto Real': '36.5296071875, -6.19511665', 'Puerto Serrano': '36.9228396, -5.5441182', 'Puerto de la Cruz': '28.4240155, -16.3210659', 'Puertollano': '38.688732452380954, -4.105357057142857', 'Pumarejo de Tera': '41.9724186, -6.0297772', 'Punta Prima': '37.9477842, -0.7141646', 'Punta del Hidalgo': '28.5685764, -16.3256108', 'Purias': '37.59907035, -1.65650625', 'Purley': '51.3374786, -0.11305302857142856', 'Quart de Poblet': '39.48253619090909, -0.44500877272727274', 'Quesada': '37.8443945, -3.0677047', 'Quintana del Marco': '42.20446, -5.8549614', 'Quintela': '42.9652489, -7.4574694', 'Quiroga': '42.4752794, -7.2718253', 'Rabanal de Arriba': '42.9001949, -6.3099203', 'Rafal': '39.5836473, 2.6806628', 'Rainham': '51.5168444, 0.1907201', 'Raíces Nuevo': '43.5741681, -5.9390716', 'Real': '42.4542304, -6.0158392', 'Reboredo': '42.2894137, -7.8319973', 'Retamar': '36.85122436666666, -2.310166166666667', 'Reus': '41.153498245544554, 1.1084743', 'Ribadavia': '42.289036518181824, -8.14370420909091', 'Ribadelago Nuevo': '42.1141484, -6.723541', 'Ribadumia': '42.5152742, -8.7664072', 'Richmond': '51.46589558333333, -0.29118758333333333', 'Rio Tinto': '41.17428545, -8.57541255', 'Riolobos': '39.920938, -6.3041279', 'Rioseco de Soria': '41.641136, -2.841124', 'Rioseco de Tapia': '42.690901, -5.768048', 'Risco Negro': '28.0225219, -15.3877878', 'Rivas-Vaciamadrid': '40.37430698, -3.54132404', 'Rocafort': '39.529135999999994, -0.41104074999999995', 'Rochela': '42.5225387, -8.7097275', 'Roma': '41.8931647, 12.616129166666667', 'Rome': '41.88734504241379, 12.482451813620688', 'Romford': '51.581448231578946, 0.1841655052631579', 'Rota': '36.6259462, -6.36413165', 'Ruidera': '38.976866, -2.8848125', 'Ruislip': '51.5741471, -0.42213944999999997', 'Rábade': '43.1214802, -7.6243621', 'S. Leonardo de Yagüe': '41.830837700000004, -3.07058', 'Sa Indioteria': '39.6056498, 2.676314', 'Sa Vileta-Son Rapinya': '39.59190903333333, 2.618109666666667', 'Sabadell': '41.547663493, 2.103674539', 'SabesteCoffee': '51.4804599, 0.0694859', 'Sabiote': '38.06875183333333, -3.3087551666666664', 'Sabiñánigo': '42.51552948571429, -0.36316301428571424', 'Sabucedo': '42.2405691, -7.9743506', 'Sacedón': '40.4815229, -2.7329614', 'Sagunto': '38.0939222, -3.6309298', 'Sainsbury': '51.4343552, -0.3756649', 'Salamanca': '40.968435578472224, -5.663365422916666', 'Saldaña': '42.52093013333333, -4.737020333333334', 'Salinetas': '27.9803146, -15.378428', 'Sallent de Gállego': '42.766635199999996, -0.3588906', 'Salt': '41.9762555, 2.7997223', 'Samos': '42.73055574999999, -7.32668815', 'San Andrés': '28.5021065, -16.1969285', 'San Andrés del Rabanedo': '42.60268706, -5.5965331', 'San Benito': '37.9526431, -1.1357185', 'San Carlos del Valle': '38.8449935, -3.2419238', 'San Cibrao das Viñas': '42.289999, -7.836059', 'San Cristóbal de Entreviñas': '42.04452933333334, -5.633809766666666', 'San Fernando': '36.46337692461539, -6.200236218461538', 'San Fernando de Henares': '40.42330539230769, -3.5310341230769233', 'San Ginés': '37.9523763, -1.1763218', 'San Gregorio': '41.69277355, -0.8619167', 'San Jose': '36.5330976, -6.2999232', 'San Juan': '38.3634265, -0.4295751', 'San Juan de Mozarrifar': '41.71811, -0.8409352', 'San Juan de Ortega': '42.3477195, -3.6687627', 'San Martín de Trevejo': '40.2126766, -6.8003535', 'San Matias': '28.4382711, -16.2985441', 'San Pedro Alcántara': '36.48587986904762, -4.990305754761905', 'San Pedro Bercianos': '42.3908365, -5.7148138', 'San Pedro de Ceque': '42.0403938, -6.0745282', 'San Pedro de Olleros': '42.6972728, -6.7187451', 'San Pedro.': '36.4842653, -4.9804073', 'San Román': '42.871536750000004, -7.0621015', 'San Roque': '36.20711433333333, -5.398185683333334', 'San Sebastián': '43.3230704, -1.9747176', 'San Sebastián de los Reyes': '40.54925025, -3.6365939000000003', 'San Vitero': '41.7793174, -6.3473629', 'San Xulián': '42.52646944999999, -7.5692505', 'San cristovo de cea': '42.466356, -7.9842984', 'Sancedo': '42.6658997, -6.6357472', 'Sande': '42.238057, -8.087471', 'Sandiás': '42.1098615, -7.7573122', 'Sangonera la Seca': '37.9578209, -1.2388705999999998', 'Sangonera la Verde': '37.929622875, -1.21130815', 'Sanlúcar de Barrameda': '36.778082635714284, -6.349609621428571', 'Sant Boi de Llobregat': '41.34503951290323, 2.0368827032258063', 'Sant Joan Despí': '41.36535365, 2.0663302', 'Sant Jordi': '39.5540552, 2.7779769', 'Sant Salvador': '41.1577143, 1.2410129', 'Sant Vicent del Raspeig': '38.38230736, -0.50921352', 'Santa Ana': '38.9026046, -1.9924419', 'Santa Coloma de Gramenet': '41.44995064074074, 2.211956114814815', 'Santa Cruz de Mudela': '38.5980763, -3.4704164', 'Santa Cruz de Tenerife': '28.460063417877095, -16.2673412', 'Santa Cruz de Yanguas': '42.0624391, -2.4487297', 'Santa Maria de': '42.3223544, -8.1210731', 'Santa María de Huerta': '41.2615831, -2.1779515', 'Santa María de Trassierra': '37.9268185, -4.8987469', 'Santa María del Mar': '28.426520474999997, -16.300382525', 'Santander': '43.461207507738095, -3.8160376904761906', 'Santiago de Compostela': '42.8788086, -8.540962632666666', 'Santiago del Campo': '39.6335233, -6.3614561', 'Santibañez de la Peña': '42.8022643, -4.7399009', 'Santibáñez de Vidriales': '42.0734907, -6.0123017', 'Santibáñez el Bajo': '40.17602915, -6.22457395', 'Santillana de Campos': '42.3629741, -4.3863552', 'Santo Tomé': '38.0292008, -3.1023913', 'Santo Ángel': '37.9422982, -1.1316082', 'Santovenia de la Valdoncina': '42.5394961, -5.5871711', 'Saravillo': '42.5542568, 0.2578626', 'Sarreaus': '42.0872132, -7.6045641', 'Sarria': '42.77931482083333, -7.412206729166667', 'Sarrión': '40.1405509, -0.8129972', 'Sedaví': '39.42479707, -0.38310646', 'Segovia': '40.943489794444446, -4.116228702777778', 'Segura de la Sierra': '38.2961636, -2.6507377', 'Selcetta': '41.7645838, 12.47715995', 'Serradilla': '39.905245666666666, -6.0129801333333335', 'Ses Cadenes': '39.5085907, 2.7506606', 'Sesué': '42.5503095, 0.4700485', 'Setenil de las Bodegas': '36.862741975, -5.178615425', 'Sevilla': '37.38350618552279, -5.971737966219839', 'Sidcup': '51.43048873, 0.10664172000000001', 'Sigüeiro': '42.9655031, -8.4476648', 'Sigüenza': '41.06976235, -2.6443132', 'Siles': '38.38920365, -2.58306155', 'Siresa': '42.7565567, -0.7548534', 'Sobradelo': '42.4158417, -6.9102171', 'Socuéllamos': '39.284768, -2.79566168', 'Son Castelló': '39.6001157, 2.6665265', 'Son Ferriol': '39.57437718333333, 2.7174278333333333', 'Son Sardina': '39.621399, 2.6548012', 'Son Serra Perera': '39.5973677, 2.6421866', 'Soria': '41.76694795, -2.4730200583333333', 'Sotiello': '43.3196321, -5.8028126', 'South Croydon': '51.34830231538462, -0.08406637692307693', 'Southall': '51.505661275, -0.377544875', 'Souto': '42.18766, -8.045', 'Sta Coloma de Gramanet': '41.4496757, 2.2183357', 'Stamford': '51.4936505, -0.2417005', 'Sucina': '37.8859253, -0.9446969666666667', 'Surbiton': '51.38817146153846, -0.29525561538461537', 'Surrey': '51.3641762, -0.1944799', 'Sutton': '51.36537725555556, -0.20648412222222223', 'Tabarca': '38.1663572, -0.48118115', 'Taboada': '42.71735, -7.7631631', 'Taboadela': '42.2424113, -7.8256634', 'Taco': '28.440391599999998, -16.30420445', 'Talavera de la Reina': '39.96184175538461, -4.832533472307692', 'Talayuela': '39.987005025, -5.60976825', 'Tamajón': '40.9986343, -3.2482479', 'Tangel': '38.4074909, -0.4726751', 'Taraguilla': '36.2137156, -5.4320244', 'Tardesillas': '41.8285571, -2.4589429', 'Tardienta': '41.9600466, -0.5394955', 'Tarifa': '36.021062154545454, -5.6155582636363635', 'Tarragona': '41.11999216492537, 1.2463097619402983', 'Tavernes Blanques': '39.508260433333334, -0.36407940000000005', 'Teddington': '51.422019125, -0.33260825', 'Tejina': '28.5337806, -16.361815366666665', 'Telde': '27.996769147222224, -15.406813934722221', 'Tendilla': '40.5442908, -2.9584848', 'Tenerife': '28.4489986, -16.2746825', 'Tercia': '37.6815416, -1.6499172', 'Terrassa': '41.56336119652174, 2.0170197269565215', 'Teruel': '40.33803205882353, -1.1047350676470589', 'Thornton Heath': '51.3938803, -0.1056688', 'Toledo': '39.864105225609755, -4.014731767073171', 'Tomelloso': '39.1558085275862, -3.0201895379310346', 'Toral de Merayo': '42.524548, -6.6316352', 'Toral de los Vados': '42.543269800000004, -6.77651655', 'Toreno': '42.72808805, -6.52238185', 'Torla-Ordesa': '42.62829776666667, -0.1122499', 'Toro': '41.523687360000004, -5.3931529000000005', 'Torquemada': '42.0319966, -4.2994192', 'Torre Guil': '37.9002286, -1.215821', 'Torre de Juan Abad': '38.5887025, -3.0646411', 'Torre del Bierzo': '42.6089179, -6.3651078', 'Torre-romeu': '41.54769335, 2.1281290999999998', 'Torreagüera': '37.976034399999996, -1.0588236', 'Torreblascopedro': '37.997533, -3.636194', 'Torrecera': '36.6098779, -5.9437529', 'Torredelcampo': '37.772094233333334, -3.89786475', 'Torredonjimeno': '37.76409775, -3.9533198333333335', 'Torrejoncillo': '39.89708483333333, -6.4681806', 'Torrejón de Ardoz': '40.45818753157894, -3.4699243245614033', 'Torrejón del Rey': '40.6435699, -3.3264322', 'Torrellano': '38.29312425714286, -0.5927858714285714', 'Torrelodones': '40.5755935, -3.93432858', 'Torremenga': '40.0475316, -5.7726906', 'Torrente de Cinca': '41.47407033333334, 0.33549086666666667', 'Torrenueva': '38.6400267, -3.3636143', 'Torreorgaz': '39.3838886, -6.2480458', 'Torreperogil': '38.0342731, -3.2904834333333333', 'Torres': '37.7852725, -3.5088368', 'Torres de Albánchez': '38.4142543, -2.6779255', 'Torrevieja': '37.98031777575758, -0.6828376313131314', 'Trabazos': '41.74408, -6.4964022', 'Tramacastilla': '40.4304559, -1.574313', 'Trasmiras': '42.02296783333333, -7.613820966666666', 'Trebujena': '36.8698177, -6.1766666', 'Triacastela': '42.7562005, -7.2356603', 'Trobajo del Camino': '42.5991329, -5.6045094', 'Trubia': '43.346108400000006, -5.9698100499999995', 'Trévago': '41.8729542, -2.1028928', 'Twickenham': '51.44953585555555, -0.34473841111111114', 'Ubrique': '36.673081700000004, -5.449305233333334', 'Upminster': '51.55234618181819, 0.2510604181818182', 'Urb. Cdad. del Golf': '42.0479309, -4.5780582', 'Urb. Novo Santi Petri': '36.3523978, -6.1642408', 'Urb. las Camaretas': '41.7732746, -2.5006141', 'Urb. los Vergeles': '37.1643295, -3.5723235', 'Usanos': '40.7140493, -3.2698298', 'Utebo': '41.6635802, -0.9307959', 'Utrillas': '40.8132688, -0.8472126333333333', 'Uxbridge': '51.520281499999996, -0.443919', 'Vadillo': '41.791119, -3.0081935', 'Valcabado': '41.5324333, -5.759853', 'Valdecabras': '40.206836, -2.004961', 'Valdepeñas': '38.767522757692305, -3.387183607692308', 'Valderas': '42.0794845, -5.4438741', 'Valderrobres': '40.8732302, 0.15425455', 'Valdesalor': '39.3833677, -6.348871', 'Valencia': '39.46725873569024, -0.3711913144781145', 'Valencia de Don Juan': '42.29302545, -5.5190747', 'Valladolid': '41.64477447202072, -4.730428651295337', 'Valladolises': '37.7771395, -1.1236248', 'Valverde de la Virgen': '42.5679847, -5.693247899999999', 'Valverde del Fresno': '40.2239395, -6.8782586666666665', 'Varea': '42.4621244, -2.4075755', 'Vega de Espinareda': '42.7254883, -6.655234266666667', 'Vegaviana': '40.0405486, -6.7170743', 'Veguellina de Órbigo': '42.43427035, -5.88523615', 'Vejer de la Frontera': '36.24789893, -5.97544388', 'Velamazán': '41.4489127, -2.6991578', 'Velilla del Río Carrión': '42.8274583, -4.8447984', 'Venta Gaspar': '36.8681493, -2.3861695', 'Venta de Baños': '41.922817980000005, -4.490435580000001', 'Venta de los Santos': '38.3613199, -3.0733106', 'Venta del Aire': '40.11305, -0.740004', 'Verín': '41.9378374, -7.437626638461539', 'Viana do Bolo': '42.18099281666667, -7.111865600000001', 'Vicolozano': '40.680937, -4.631762', 'Vigo': '42.22457425679013, -8.72090796728395', 'Vila Da Area': '43.5128333, -8.3100267', 'Vila-seca': '41.1191381, 1.150226', 'Vilachá': '42.7952113, -7.6043722', 'Vilagarcía de Arousa': '42.5916183, -8.768976599999998', 'Vilamartín de Valdeorras': '42.4144222, -7.061181599999999', 'Vilamor': '42.5688548, -7.2320631', 'Vilanova de Arousa': '42.566646899999995, -8.8188471', 'Vilar': '42.13157, -8.1338899', 'Vilarchao': '42.4115295, -7.840255', 'Vilasante': '42.5846635, -7.6391213', 'Vilches': '38.2079333, -3.5127447', 'Villablino': '42.93914253809524, -6.31914660952381', 'Villabuena del Puente': '41.3798101, -5.4084016', 'Villacarrillo': '38.11705045833333, -3.0816855666666663', 'Villadangos del Paramo': '42.5343964, -5.748541', 'Villaestrigo del Páramo': '42.2427532, -5.7159265', 'Villafranca del Bierzo': '42.607604, -6.810510366666667', 'Villafranca del Campo': '40.702929, -1.317613', 'Villafría': '42.3648686, -3.6155591', 'Villagarcía de la Vega': '42.3896497, -5.9258836', 'Villahibiera': '42.5783264, -5.261746', 'Villahán': '42.0505912, -4.1323951', 'Villalpando': '41.844244625, -5.397154825', 'Villamandos': '42.179005, -5.5912987', 'Villamañán': '42.322026575, -5.5878344250000005', 'Villamuriel de Cerrato': '41.9554276, -4.5188479', 'Villanueva de la Sierra': '40.2038576, -6.4082399', 'Villanueva de la Torre': '40.5836467, -3.29577905', 'Villanueva de los Infantes': '38.73498596666666, -3.0126415666666664', 'Villanueva del Arzobispo': '38.16724684285714, -3.0061866714285714', 'Villanueva del Campo': '41.9867833, -5.40715535', 'Villar del Cobo': '40.3948404, -1.6726', 'Villaralbo': '41.4911775, -5.6821613', 'Villardeciervos': '41.9413536, -6.2879376', 'Villarente': '42.546361000000005, -5.46034485', 'Villarramiel': '42.042904449999995, -4.91308655', 'Villarrubia de los Ojos': '39.19652611111111, -3.633085622222222', 'Villarta de San Juan': '39.24200196666667, -3.4248695833333334', 'Villasabariego': '42.5411059, -5.4492188', 'Villaseca de Laciana': '42.944215424999996, -6.250817475', 'Villel': '40.2340087, -1.1867276', 'Viloira': '42.4117279, -6.9783513', 'Vinalesa': '39.5351244, -0.3689175', 'Vinuesa': '41.9098911, -2.7639846', 'Viso del Marqués': '38.521683499999995, -3.5575878000000003', 'Vitinia': '41.7914383, 12.4074452', 'Vitoria-Gasteiz': '42.85090934021739, -2.677926666304348', 'Vivel del Río Martín': '40.8695293, -0.9408252', 'Vrins': '42.9249522, -8.5755265', 'Wallington': '51.361715583333336, -0.14850108333333334', 'Welling': '51.462393899999995, 0.10808636666666667', 'Wembley': '51.559100475, -0.29275545000000003', 'West Drayton': '51.50627862, -0.47563712', 'West Wickham': '51.37572771666667, -0.012769666666666667', 'Westerham': '51.31370206666667, 0.0340853', 'Woodford Green': '51.607331200000004, 0.03932385', 'Worcester Park': '51.379489899999996, -0.24344485', 'Xinzo de Limia': '42.062913378260866, -7.72572994347826', 'Xirivella': '39.463869538888886, -0.4291510333333333', 'Xunqueira de Ambía': '42.2052143, -7.7370057', 'Xàtiva': '38.991189223333336, -0.5234018166666667', 'Zahara de los Atunes': '36.1330091, -5.8419253', 'Zamora': '41.504066815277774, -5.737835669444444', 'Zaragoza': '41.65224518603175, -0.8914068428571429', 'Zarcilla de Ramos': '37.84327115, -1.8737557', 'Zarza de Granadilla': '40.2378354, -6.0466743', 'Zeneta': '38.009575399999996, -0.9991711333333333', 'Zubieta': '43.2665209, -2.0250724', 'Ágreda': '41.8543059, -1.9200764', 'Ávila': '40.65386369111111, -4.692828448888889', 'Ólvega': '41.778947966666664, -1.9842296333333334', 'Úbeda': '38.01346316410256, -3.3737565179487174'}
    
    st.write('')
    if st.checkbox('📍 Usar mi ubicación'):
        try:
            location = [loc]
            latitud = location[0]['coords']['latitude']
            longitud = location[0]['coords']['longitude']
            # st.write(10/0) # Provocamos el error
        except:
            st.error('No hemos podido acceder a tu ubicación. Selecciona tu municipio en el siguiente desplegable para buscar tu cafetería ideal:', icon="⚠️")
            ciudad_seleccionada = st.selectbox('Selecciona una ciudad', options=list(dictio_coords_saviour.keys()),placeholder="Busca tu ubicación más cercana para un relaxing cup of café con leche", index=945)
            if ciudad_seleccionada:
                latitud = round(float(dictio_coords_saviour[ciudad_seleccionada].split(', ')[0]), 4)
                longitud = round(float(dictio_coords_saviour[ciudad_seleccionada].split(', ')[1]), 4)
    else:
        ciudad_seleccionada = st.selectbox('Selecciona una ciudad o marca "📍 Usar mi ubicación" para encontrar tu cafetería ideal', options=list(dictio_coords_saviour.keys()),placeholder="Busca tu ubicación más cercana para un relaxing cup of café con leche", index=945)
        if ciudad_seleccionada:
            latitud = round(float(dictio_coords_saviour[ciudad_seleccionada].split(', ')[0]), 4)
            longitud = round(float(dictio_coords_saviour[ciudad_seleccionada].split(', ')[1]), 4)
    try:
        latitud = round(float(latitud), 4)
        longitud = round(float(longitud), 4)
    except:
        latitud = 40.4336
        longitud = -3.7043
    
    if latitud == 40.4336 and longitud == -3.7043:
        st.warning('Estás utilizando la ubicación predeterminada en Glorieta de Quevedo (Madrid). Para usar tu ubicación, marca la casilla de "📍 Usar mi ubicación"')
    
    latitude = latitud
    longitude = longitud
    
    m = folium.Map(location=[latitude, longitude], zoom_start=15)
    red_icon = folium.Icon(color='red')
    folium.Marker(
        [latitude, longitude], popup='<div style="white-space: nowrap;">Tu ubicación</div>', tooltip="Tu ubicación", icon=red_icon
    ).add_to(m)
    
    df['lat_dif'] = [abs(float(lt) - latitude) for i,lt in enumerate(df['Latitud'])]
    df['lon_dif'] = [abs(float(lg) - longitude) for i,lg in enumerate(df['Longitud'])]
    df['dif_sum'] = df['lat_dif'] + df['lon_dif']
    
    sorted_df = df.sort_values(by='dif_sum', ascending=True) #[:num_cafeterias]
    sorted_df = sorted_df.reset_index(drop=True)
    sorted_df['Metros'] = [haversine_distance(latitude, longitude, e, sorted_df['Longitud'][i]) for i,e in enumerate(sorted_df['Latitud'])]
    #sorted_df = sorted_df.sort_values(by='Metros', ascending=True)
    
    sorted_df_show = sorted_df
    sorted_df = sorted_df[:num_cafeterias]
    
    coords = []
    for i,e in enumerate(sorted_df['Latitud']):
        coords.append(str(e) + ", " +str(sorted_df['Longitud'][i]))
    sorted_df['coords'] = coords
    # sorted_df['Cómo llegar'] = ['https://www.google.com/maps/search/'+convert_coordinates(e) for e in sorted_df['coords']]
    
    for index, row in sorted_df.iterrows():
        # Crea el popup con el enlace clickeable que se abrirá en una nueva ventana
        
        link = sorted_df["Link"][index].replace('"', '%22')
        popup_content = f'<div style="white-space: nowrap;">A {row["Metros"]} metros: <strong><a href="{link}" target="_blank" style="text-decoration: underline; cursor: pointer;">{row["☕ Nombre"]}</a></strong></div>'
    
        folium.Marker(
            location=[row["Latitud"], row["Longitud"]],
            popup=popup_content,
        ).add_to(m)
    
    if from_pc:
        folium_static(m, width=1025)
    else:
        folium_static(m, width=380)
    
    
    columnas_a_modificar = ['🔓 Abierto Ahora',
                      '🪑 Puedes sentarte', '☀️ Tiene terraza', '🍺 Sirve Cerveza', '🍷 Sirve vino', '🥪 Sirve desayunos/almuerzos', '🫒 Sirve aperitivos', '🍪 Sirve postres', '🚶‍♂️ Para llevar', 
                      '🙋‍♀️ Acepta reserva', '🐕‍🦺 Acepta perros', '🐕 Acepta perros fuera', '🛜 Tiene Wifi','🛜 Tiene Wifi Gratis', '🏳️‍🌈 LGBT+ friendly',
                     ]
    for columna in columnas_a_modificar:
        sorted_df_show[columna] = sorted_df_show[columna].apply(sustituir_valor_emoji)
    
    sorted_df_show = sorted_df_show[['Link', 'Metros', '☕ Nombre', '🏙️ Ciudad', '🔓 Abierto Ahora', '💲 Nivel de precios', '⭐ Puntuación', '💬 Nº Comentarios', '🕐 Horario hoy', '📊 % Ocupación Ahora', 
                      '🪑 Puedes sentarte', '☀️ Tiene terraza', '🍺 Sirve Cerveza', '🍷 Sirve vino', '🥪 Sirve desayunos/almuerzos', '🫒 Sirve aperitivos', '🍪 Sirve postres', '🚶‍♂️ Para llevar', 
                      '🙋‍♀️ Acepta reserva', '🐕‍🦺 Acepta perros', '🐕 Acepta perros fuera', '🛜 Tiene Wifi','🛜 Tiene Wifi Gratis', '🏳️‍🌈 LGBT+ friendly',
                     ]] #.sort_values(by='Metros', ascending=True)
    st.write('')
    st.markdown('#### Tabla detalle de las cafeterías')
    num_cafes_filtradas = len(sorted_df_show)
    with st.expander(f"👀 Ver {num_cafes_filtradas} cafeterías (por proximidad)"):
        st.data_editor(
            sorted_df_show,
            column_config={
                "Link": st.column_config.LinkColumn(
                    "🔗 Link", display_text = "🌐 Cómo llegar"
                ),
                "Metros": st.column_config.NumberColumn(
                "📏 Distancia",
                help="Medida en metros desde tu ubicación",
                format="%d m",
                ),
                "⭐ Puntuación": st.column_config.ProgressColumn(
                    "⭐ Puntuación",
                    help="Los valores a 0 son sitios sin votos",
                    format="%f",
                    min_value=0,
                    max_value=5,
                ),
                "📊 % Ocupación Ahora": st.column_config.ProgressColumn(
                    "📊 % Ocupación Ahora",
                    help="Los valores a 0 pueden ser sitios sin información de ocupación",
                    format="%f",
                    min_value=0,
                    max_value=100,
                ),
            },
            hide_index=True,
        )
    
    # with st.expander("👀 Ver detalle de todas las cafeterías por proximidad"):
    #     st.dataframe(sorted_df_show.drop(['Link', 'Latitud', 'Longitud', 'Cerrado permanentemene', 'Cerrado temporalmente', 'lat_dif', 'lon_dif', 'dif_sum', 'Metros'], axis=1))
        
    # ---------------------------------------------------------------------------------------UBI ⬆️-------------------------------------
    # --------------------------------------------------------------------------------------MAIL ⬇️-------------------------------------
    
    # st.write('')
    st.write('')
    st.write('')
    
    # ciudades = sorted(sorted_df_show['🏙️ Ciudad'].unique())
    # st.write(f'{ciudades}')
    
    # municipios_incluidos = ['A Arnoia', 'A Bergueira', 'A Coruña', 'A Groba', 'A Gudiña', 'A Manchica', 'A Pobra de Trives', 'A Pobra do Brollón', 'A Porriña', 'A Rúa', 'A Silva', 'A Valenza', 'Abejar', 'Acebo', 'Adahuesca', 'Aeropuerto de los Rodeos', 'Aguas Nuevas', 'Ágreda',
    #                         'Aguilar de Campoo', 'Aínsa', 'Alaquàs', 'Alar del Rey', 'Albacete', 'Albaladejo', 'Albalat dels Sorells', 'Albalate de Zorita', 'Albalate del Arzobispo', 'Albarellos', 'Albarracín', 'Albentosa', 'Alboraya', 'Alcalá de los Gazules', 'Alcalá del Obispo', 
    #                         'Alcalá del Valle', 'Alcaudete', 'Alcañices', 'Alcañiz', 'Alcobendas', 'Alcolea', 'Alcolea de Cinca', 'Alcolea del Pinar', "Alcora (L')", 'Alcorcón', 'Alcorisa', 'Alcántara', 'Alcázar de San Juan', 'Aldaia', 'Aldea del Rey', 'Alfafar', 
    #                         'Alfara del Patriarca', 'Algeciras', 'Algeciras, Cádiz', 'Algora', 'Algorta', 'Alhambra', 'Alicante', 'Alija del Infantado', 'Allariz', 'Almadrones', 'Almadén', 'Almagro', 'Almazcara', 'Almazán', 'Almería', 'Almodóvar del Campo', 
    #                         'Almonacid de Zorita', 'Almudévar', 'Almàssera', 'Alovera', 'Alquézar', 'Altafulla', 'Alumbres', 'Ampudia', 'Amusco', 'Andorra', 'Aneiros ,Ferrol', 'Ansoáin', 'Ansó', 'Antas de Ulla', 'Aranzueque', 'Arcenillas', 'Arcos de Jalón', 
    #                         'Arcos de la Frontera', 'Arcos de la Polvorosa', 'Ardea', 'Areeta (Getxo)', 'Arenals del Sol', 'Arenas de San Juan', 'Arenillas de Nuño Pérez', 'Argamasilla de Alba', 'Argamasilla de Calatrava', 'Armunia', 'Arnuíde', 'Arquillos', 
    #                         'Arroyo De La Vega', 'Arroyo Frio', 'Arroyo de la Luz', 'Arén', 'As Campiñas', 'As Nogais', 'Astorga', 'Astudillo', 'Astún', 'Atienza', 'Ávila', 'Avilés', 'Ayerbe', 'Ayoó de Vidriales', 'Azucaica', 'Azuqueca de Henares','Badajoz', 
    #                         'Badalona', 'Baeza', 'Bailén', 'Bajamar', 'Balcon de Telde', 'Baltanás', 'Bande', 'Baracaldo', 'Barajas', 'Barakaldo', 'Baralla', 'Barbadás', 'Barbastro', 'Barbate', 'Barcelona', 'Barco (O)', 'Barking', 'Barral', 'Barriada Río San Pedro', 
    #                         'Barrio', 'Barruelo de Santullán', 'Base Aerea Conjunta Torrejón', 'Baños de Montemayor', 'Beas de Segura', 'Becerreá', 'Beckenham', 'Begíjar', 'Bellavista', 'Belvedere', 'Belver de Cinca', 'Belvís de Monroy', 'Bembibre', 'Benabarre', 
    #                         'Benalup-Casas Viejas', 'Benasque', 'Benavente', 'Benavides de Órbigo', 'Benetússer', 'Benlloch', 'Berlanga de Duero', 'Bermillo de Sayago', 'Bernueces', 'Berriozar', 'Betote', 'Bexley', 'Bexleyheath', 'Bielsa', 'Biescas', 'Bilbao', 
    #                         'Binéfar', 'Boadilla del Monte', 'Bolaños de Calatrava', 'Boltaña', 'Bonanza', 'Bonavista', 'Bonfim', 'Bonrepòs i Mirambell', 'Boqueixon', 'Bornos', 'Boñar', 'Brentford', 'Bretó', 'Brihuega', 'Broadway', 'Bromley', 'Bronchales', 'Broto', 
    #                         'Brozas', 'Burgos', 'Burjassot', 'Burunchel', 'Bustillo del Páramo', 'Bóveda', "Ca'n Pastilla", 'Cabanillas del Campo', 'Cabezabellosa', 'Cabo de Gata', 'Cabo de Palos', 'Caboalles de Abajo', 'Cabrejas del Pinar', 'Cacabelos', 'Calaceite', 
    #                         'Calafell', 'Calamocha', 'Calanda', 'Calero (El)', 'Calvos de Randín', 'Calzada de Calatrava', 'Calzadilla', 'Calzadilla de la Cueza', 'Cambados', 'Caminomorisco', 'Caminreal', 'Campanhã', 'Campazas', 'Campillo de Arenas', 'Campo', 
    #                         'Campo de Criptana', 'Camponaraya', 'Canales', 'Canals', 'Candanchú', 'Candasnos', 'Canena', 'Canfranc-Estación', 'Canredondo', 'Canteras', 'Caraquiz', 'Carbajales de Alba', 'Carcaboso', 'Carrión de Calatrava', 'Carrión de los Condes', 
    #                         'Carrus', 'Carshalton', 'Cartagena', 'Cartagena, Murcia', 'Cartuja Baja', 'Carucedo', 'Casar de Cáceres', 'Casar de Talavera (El)', 'Casas Nuevas', 'Casas de Don Gómez', 'Casas del Castañar', 'Casaseca de las Chanas', 'Casatejada', 
    #                         'Cascón de la Nava', 'Castejón', 'Castejón de Sos', 'Castel Romano', 'Castellar de Santiago', 'Castellón de la Plana', 'Castillazuelo', 'Castrillo de Don Juan', 'Castrillo de la Ribera', 'Castro Caldelas', 'Castro de Ribeiras', 'Catarroja', 
    #                         'Cazorla', 'Ceclavín', 'Cedofeita', 'Cedrillas', 'Celanova', 'Cella', 'Cerro Muriano', 'Cervera de Pisuerga', 'Chantada', 'Chapela', 'Chessington', 'Chiclana de la Frontera', 'Chilluévar', 'Chillón', 'Chipiona', 'Chislehurst', 'Ciampino', 'Cifuentes', 'Cilleros', 'Cimanes de la Vega', 'Cisneros', 'Cistierna', 'Ciudad Quesada', 'Ciudad Real', 'Cogolludo', 'Coles', 'Collado Villalba', 'Collonades', 'Colloto', 'Colungo', 'Conchel', 'Congosto', 'Conil de la Frontera', 'Coria', 'Cornellà de Llobregat', 'Corredoria', 'Cortes', 'Cortijos Nuevos', 'Coslada', 'Coto de Bornos', 'Coto-Ríos', 'Coulsdon', 'Covaleda', 'Coy', 'Cp', 'Cretas', 'Croydon', 'Ctra. Acceso Central Térmica N: S/N', 'Cualedro', 'Cuenca', 'Cuesta Blanca', 'Cuevas de Almudén', 'Curbe', 'Cáceres', 'Cádiz', 'Córdoba', 'Dacón', 'Dagenham', 'Daimiel', 'Dartford', 'Donadío', 'Donostia-San Sebastian', 'Dos Hermanas', 'Duruelo de la Sierra', 'El Albujón', 'El Algar', 'El Alquián', 'El Arenal', 'El Burgo Ranero', 'El Burgo de Osma', 'El Casar', 'El Casar de Talavera', 'El Chaparral', 'El Cuervo', 'El Gastor', 'El Grado', 'El Grao de Castellón', 'El Higueron', 'El Pinar', 'El Poblenou', 'El Portal', 'El Poyo del Cid', 'El Puerto de Sta María', 'El Robledo', 'El Rosario', 'El Torno', 'El Zabal', 'El pilar', 'Elche', 'Elche Parque Industrial', 'Enfield', 'Entrimo', 'Erith', 'Es Pil·larí', 'Es Secar de la Real', 'Escarrilla', 'Esgos', 'Espera', 'Estación', 'Estación Linares-Baeza', 'Estación de Medinaceli', 'Estadilla', 'Estella del Marqués', 'Esteras de Medinaceli', 'Estrecho de San Gines', 'Fabero', 'Facinas', 'Fariza', 'Feltham', 'Fermoselle', 'Ferreira de Pantón', 'Ferrol', "Foia d'Elx", 'Foios', 'Fontanar', 'Formigal', 'Fortanete', 'Fraga', 'Fresno de la Ribera', 'Friamonde', 'Frómista', 'Fuenlabrada', 'Fuenllana', 'Fuente el Fresno', 'Fuentelahiguera de Albatages', 'Fuentelapeña', 'Fuentes de Nava', 'Galapagar', 'Galisteo', 'Galiñáns', 'Gargüera', 'Garrovillas', 'Gata', 'Germans Sàbat', 'Getafe', 'Getxo', 'Gijón', 'Girona', 'Godella', 'Golmayo', 'Gordoncillo', 'Granada', 'Graus', 'Grazalema', 'Grañén', 'Greater', 'Greenford', 'Guadacorte', 'Guadalajara', 'Guadalcacín', 'Guamasa', 'Guardo', 'Guarromán', 'Gustei', 'Hampton', 'Hanwell', 'Harrow', 'Hayes', 'Herencia', 'Herrera de Pisuerga', 'Hervás', 'Hinojares', 'Hontoria', 'Horcajo de los Montes', 'Hornchurch', 'Hornos', 'Hospital de Órbigo', "Hospitalet de Llobregat (L')", 'Hounslow', 'Huelva', 'Huergas de Babia', 'Huesca', 'Humanes', 'IMEPE', 'Ibros', 'Igüeña', 'Ilford', 'Isla Plana', 'Isla de', 'Isleworth', 'Iznatoraf', 'Jabalquinto', 'Jaca', 'Jadraque', 'Jarandilla de la Vera', 'Jaraíz de la Vera', 'Jarilla', 'Jaén', 'Jerez de la Frontera', 'Jerte', 'Josa', 'Jubilee', 'Jódar', 'Keston', 'Kingston upon Thames', "L'Altet", 'La Aljorra', 'La Aparecida', 'La Barca de la Florida', 'La Bañeza', 'La Bóveda de Toro', 'La Camocha', 'La Carolina', 'La Cañada', 'La Escucha', 'La Estación', 'La Fortuna', 'La Garita', 'La Herradura', 'La Hoya', 'La Iruela', 'La Laguna', 'La Línea de la Concepción', 'La Magdalena', 'La Manga', 'La Manga Club', 'La Martina', 'La Mata', 'La Palma', 'La Pardilla', 'La Puebla', 'La Puebla de Valverde', 'La Puerta de Segura', 'La Solana', 'La Virgen del Camino', 'Lampaza', 'Langa de Duero', 'Larouco', 'Las Campas', 'Las Huesas', 'Las Medianias', 'Las Mercedes', 'Las Palmas de Gran Canaria', 'Las Remudas', 'Las Rozas de Madrid', 'Laza', 'Leganés', 'Leiro', 'Les Baies', 'Leystonstone', 'León', 'Linares', 'Lincoln', 'Lleida', 'Lodares', 'Logroño', 'Lombillo de los Barrios', 'London', 'Londres', 'Loporzano', 'Lorca', 'Los Barrios', 'Los Belones', 'Los Cortijillos', 'Los Moriscos', 'Los Nietos', 'Los Rábanos', 'Los Villares', 'Losar de la Vera', 'Lubián', 'Lugo', 'Láncara', 'Lérida', 'Línea De La Concepción ( La )', 'Maceda', 'Madrid', 'Madridanos', 'Madrigal de la Vera', 'Majadahonda', 'Malagón', 'Maliaño', 'Malpartida de Plasencia', 'Mancha Real', 'Manises', 'Mansilla de las Mulas', 'Mantiel', 'Manzanal del Puerto', 'Manzanares', 'Manzaneda', 'Maqueda', 'Marbella', 'Marchamalo', 'Marpequeña', 'Martos', 'Martín del Río', 'Marín', 'Mas de las Matas', 'Masegoso de Tajuña', 'Maside', 'Massanassa', 'Matarrosa del Sil', 'Mataró', 'Matas-Pinar-Monte Rozas ( Las )', 'Matola', 'Medina-Sidonia', 'Medinaceli', 'Meliana', 'Membrilla', 'Membrío', 'Mengíbar', 'Miajadas', 'Middlesex', 'Miguelturra', 'Mirabel', 'Miranda', 'Mislata', 'Mitcham', 'Mogón', 'Mohedas de Granadilla', 'Molina de Aragón', 'Moncada', 'Mondéjar', 'Monfarracinos', 'Monforte de Lemos', 'Monreal del Campo', 'Montalbán', 'Montamarta', 'Monteagudo de las Vicarías', 'Montehermoso', 'Montejos del Camino', 'Montequinto', 'Monterde de Albarracín', 'Monterroso', 'Montiel', 'Monzón', 'Mora de Rubielos', 'Moraleja', 'Moraleja del Vino', 'Morales de Toro', 'Morales del Vino', 'Moralina', 'Morden', 'Moreiras', 'Morón de Almazán', 'Mugueimes', 'Murcia', 'Museros', 'Mutilva', 'Málaga', 'Mérida', 'Móstoles', 'Narón', 'Navalmoral de la Mata', 'Navas de San Juan', 'Navas del Madroño', 'New Malden', 'Noceda', 'Northwood', 'Nueno', 'Nueva Jarilla', 'Nuñomoral', 'O Barco', 'O Carballiño', 'O Corgo', 'O Cotón', 'Ofra', 'Oia', 'Ojos Negros', 'Ojos de Garza', 'Olleros de Sabero', 'Olvera','Ólvega', 'Onzonilla', 'Oporto', 'Orbón', 'Orcera', 'Orpington', 'Ortigal', 'Osorno', 'Ostia', 'Ostia Antica', 'Otero de Bodas', 'Ourense', 'Outeiro de Rei', 'Outomuro', 'Oviedo', 'Padornelo', 'Padrenda', 'Padrenda de Abaixo', 'Paiporta', 'Palas de Rei', 'Palencia', 'Palma', 'Palmones', 'Pamplona', 'Panticosa', 'Paradela', 'Paredes de Nava', 'Pareja', 'Parla', 'Parque de La Laguna', 'Parquelagos', 'Pastrana', 'Paterna', 'Peal de Becerro', 'Pedrafita do Cebreiro', 'Pedro Muñoz', 'Peque', 'Peracense', 'Peraleda de San Román', 'Peralejos', 'Perales de Tajuña', 'Perazancas', 'Perleta', 'Peñarroya de Tastavíns', 'Picanya', 'Piedrabuena', 'Pielas', 'Pinner', 'Pinofranqueado', 'Piornal', 'Pioz', 'Plasencia', 'Plasencia del Monte', 'Poblado de Sancti Petri', 'Pobladura de Pelayo Garcia, Leon', 'Pobladura del Valle', 'Poblete', 'Pol. Ind. El Goro', 'Pol. Ind. Pla de la Vallonga', 'Poligono Industrial de Constantí', 'Ponferrada', 'Ponte Galeria-la Pisana', 'Pontevedra', 'Port Saplaya', 'Porto', 'Portomarín', 'Porzuna', 'Pozo Alcón', 'Pozo Estrecho', 'Pozuelo de Alarcón', 'Pozuelo de Calatrava', 'Pozuelo de Vidriales', 'Prado del Rey', 'Puebla de Sanabria', 'Puebla de Trives', 'Puebla del Príncipe', 'Puente Villarente', 'Puente de Domingo Flórez', 'Puente de Génave', 'Puenteareas', 'Puerto Lápice', 'Puerto Real', 'Puerto Serrano', 'Puerto de la Cruz', 'Puertollano', 'Pumarejo de Tera', 'Punta Prima', 'Punta del Hidalgo', 'Purias', 'Purley', 'Quart de Poblet', 'Quesada', 'Quintana del Marco', 'Quintela', 'Quiroga', 'Rabanal de Arriba', 'Rafal', 'Rainham', 'Raíces Nuevo', 'Real', 'Reboredo', 'Retamar', 'Reus', 'Ribadavia', 'Ribadelago Nuevo', 'Ribadumia', 'Richmond', 'Rio Tinto', 'Riolobos', 'Rioseco de Soria', 'Rioseco de Tapia', 'Risco Negro', 'Rivas-Vaciamadrid', 'Rocafort', 'Rochela', 'Roma', 'Rome', 'Romford', 'Rota', 'Ruidera', 'Ruislip', 'Rábade', 'S. Leonardo de Yagüe', 'Sa Indioteria', 'Sa Vileta-Son Rapinya', 'Sabadell', 'SabesteCoffee', 'Sabiote', 'Sabiñánigo', 'Sabucedo', 'Sacedón', 'Sagunto', 'Sainsbury', 'Salamanca', 'Saldaña', 'Salinetas', 'Sallent de Gállego', 'Salt', 'Samos', 'San Andrés', 'San Andrés del Rabanedo', 'San Carlos del Valle', 'San Cibrao das Viñas', 'San Cristóbal de Entreviñas', 'San Fernando', 'San Fernando de Henares', 'San Gregorio', 'San Jose', 'San Juan', 'San Juan de Mozarrifar', 'San Juan de Ortega', 'San Martín de Trevejo', 'San Matias', 'San Pedro Alcántara', 'San Pedro Bercianos', 'San Pedro de Ceque', 'San Pedro de Olleros', 'San Pedro', 'San Román', 'San Roque', 'San Sebastián', 'San Sebastián de los Reyes', 'San Vitero', 'San Xulián', 'San cristovo de cea', 'Sancedo', 'Sande', 'Sandiás', 'Sanlúcar de Barrameda', 'Sant Boi de Llobregat', 'Sant Joan Despí', 'Sant Jordi', 'Sant Salvador', 'Sant Vicent del Raspeig', 'Santa Ana', 'Santa Coloma de Gramenet', 'Santa Cruz de Mudela', 'Santa Cruz de Tenerife', 'Santa Cruz de Yanguas', 'Santa María de Huerta', 'Santa María de Trassierra', 'Santa María del Mar', 'Santander', 'Santiago de Compostela', 'Santiago del Campo', 'Santibañez de la Peña', 'Santibáñez de Vidriales', 'Santibáñez el Bajo', 'Santillana de Campos', 'Santo Tomé', 'Santovenia de la Valdoncina', 'Saravillo', 'Sarreaus', 'Sarria', 'Sarrión', 'Sedaví', 'Segovia', 'Segura de la Sierra', 'Selcetta', 'Serradilla', 'Ses Cadenes', 'Sesué', 'Setenil de las Bodegas', 'Sevilla', 'Sidcup', 'Sigüeiro', 'Sigüenza', 'Siles', 'Siresa', 'Sobradelo', 'Socuéllamos', 'Son Castelló', 'Son Ferriol', 'Son Sardina', 'Son Serra Perera', 'Soria', 'Sotiello', 'South Croydon', 'Southall', 'Souto', 'Sta Coloma de Gramanet', 'Stamford', 'Surbiton', 'Surrey', 'Sutton', 'Tabarca', 'Taboada', 'Taboadela', 'Taco', 'Talavera de la Reina', 'Talayuela', 'Tamajón', 'Tangel', 'Taraguilla', 'Tardesillas', 'Tardienta', 'Tarifa', 'Tarragona', 'Tavernes Blanques', 'Teddington', 'Tejina', 'Telde', 'Tendilla', 'Tenerife', 'Tercia', 'Terrassa', 'Teruel', 'Thornton Heath', 'Toledo', 'Tomelloso', 'Toral de Merayo', 'Toral de los Vados', 'Toreno', 'Torla-Ordesa', 'Toro', 'Torquemada', 'Torre de Juan Abad', 'Torre del Bierzo', 'Torre-romeu', 'Torreblascopedro', 'Torrecera', 'Torredelcampo', 'Torredonjimeno', 'Torrejoncillo', 'Torrejón de Ardoz', 'Torrejón del Rey', 'Torrellano', 'Torrelodones', 'Torremenga', 'Torrente de Cinca', 'Torrenueva', 'Torreorgaz', 'Torreperogil', 'Torres', 'Torres de Albánchez', 'Torrevieja', 'Trabazos', 'Tramacastilla', 'Trasmiras', 'Trebujena', 'Triacastela', 'Trobajo del Camino', 'Trubia', 'Trévago', 'Twickenham', 'Úbeda', 'Ubrique', 'Upminster', 'Urb. Cdad. del Golf', 'Urb. Novo Santi Petri', 'Urb. las Camaretas', 'Urb. los Vergeles', 'Usanos', 'Utebo', 'Utrillas', 'Uxbridge', 'Vadillo', 'Valcabado', 'Valdecabras', 'Valdepeñas', 'Valderas', 'Valderrobres', 'Valdesalor', 'Valencia', 'Valencia de Don Juan', 'Valladolid', 'Valverde de la Virgen', 'Valverde del Fresno', 'Varea', 'Vega de Espinareda', 'Vegaviana', 'Veguellina de Órbigo', 'Vejer de la Frontera', 'Velamazán', 'Velilla del Río Carrión', 'Venta Gaspar', 'Venta de Baños', 'Venta de los Santos', 'Venta del Aire', 'Verín', 'Viana do Bolo', 'Vicolozano', 'Vigo', 'Vila Da Area', 'Vila-seca', 'Vilachá', 'Vilagarcía de Arousa', 'Vilamartín de Valdeorras', 'Vilamor', 'Vilanova de Arousa', 'Vilar', 'Vilarchao', 'Vilasante', 'Vilches', 'Villablino', 'Villabuena del Puente', 'Villacarrillo', 'Villadangos del Paramo', 'Villaestrigo del Páramo', 'Villafranca del Bierzo', 'Villafranca del Campo', 'Villafría', 'Villagarcía de la Vega', 'Villahibiera', 'Villahán', 'Villalpando', 'Villamandos', 'Villamañán', 'Villamuriel de Cerrato', 'Villanueva de la Sierra', 'Villanueva de la Torre', 'Villanueva de los Infantes', 'Villanueva del Arzobispo', 'Villanueva del Campo', 'Villar del Cobo', 'Villaralbo', 'Villardeciervos', 'Villarente', 'Villarramiel', 'Villarrubia de los Ojos', 'Villarta de San Juan', 'Villasabariego', 'Villaseca de Laciana', 'Villel', 'Viloira', 'Vinalesa', 'Vinuesa', 'Viso del Marqués', 'Vitinia', 'Vitoria-Gasteiz', 'Vivel del Río Martín', 'Vrins', 'Wallington', 'Welling', 'Wembley', 'West Drayton', 'West Wickham', 'Westerham', 'Woodford Green', 'Worcester Park', 'Xinzo de Limia', 'Xirivella', 'Xunqueira de Ambía', 'Xàtiva', 'Zahara de los Atunes', 'Zamora', 'Zaragoza', 'Zarcilla de Ramos', 'Zarza de Granadilla', 'Zubieta']
    
    # municipios_incluidos = ['A Coruña', 'Albacete', 'Alcázar de San Juan', 'Alcobendas', 'Alcorcón', 'Algeciras', 'Alicante', 'Almería', 'Ávila', 'Avilés', 'Badajoz', 'Badalona', 'Barakaldo', 'Barcelona', 'Bilbao', 'Burgos', 'Cáceres', 'Cádiz', 'Canals', 'Cartagena', 'Castelló de la Plana', 'Ciudad Real', 'Córdoba', 'Cornellà de Llobregat', 'Coslada', 'Cuenca', 'Donosti', 'Dos Hermanas', 'Elche', 'Ferrol', 'Fuenlabrada', 'Getafe', 'Gijón', 'Girona', 'Granada', 'Guadalajara', 'Getxo', 'Herencia', 'Huelva', 'Huesca', 'Jaén', 'Jerez de la Frontera', 'Las Palmas de Gran Canaria', 'Leganés', 'León', 'Lincoln (UK)', 'Lleida', 'Logroño', 'Londres (UK)', 'Lorca', 'Lugo', 'Madrid', 'Málaga', 'Marbella', 'Mataró', 'Mérida', 'Móstoles', 'Oporto (PT)', 'Ourense', 'Oviedo', 'Palencia', 'Palma de Mallorca', 'Pamplona', 'Parla', 'Pontevedra', 'Reus', 'Roma (IT)', 'Sabadell', 'Salamanca', 'San Fernando', 'Santander', 'Sant Boi de Llobregat', 'Santiago de Compostela', 'Santa Cruz de Tenerife', 'Santa Coloma de Gramanet', 'San Cristóbal de la Laguna', 'Segovia', 'Sevilla', 'Soria', 'Tarragona', 'Talavera de la Reina', 'Telde', 'Terrassa', 'Teruel', 'Toledo', 'Torrejón de Ardoz', 'Torrevieja', 'València', 'Valladolid', 'Vigo', 'Vitoria-Gasteiz', 'Xàtiva', 'Zamora', 'Zaragoza']
    
    st.write('## 🏙️ Información sobre los datos')
    st.write('###### En el mapa encontrarás datos de diferentes municipios. Principalmente se han seleccionado aquellas localidades con más de 75.000 habitantes en España (y sus alrrededores). Los municipios incluidos se muestran en el siguiente desplegable:')
    st.selectbox('Busca tu municipio 👇',(list(dictio_coords_saviour.keys())), index=None, placeholder='Encuéntralo aquí')
    
    
    st.write('')
    st.write('###### Si tu pueblo o ciudad no se encuentra en la lista (o echas de menos más datos), puedes enviarnos un mensaje con la petición para incluirlo en el siguiente recuadro:')
    
        
    # email_sender = st.text_input('From', 'cafes.mailer@gmail.com', disabled=True)
    email_sender = st.secrets["email_sender"]
    
    # email_receiver = st.text_input('To')
    email_receiver = st.secrets["email_receiver"]
    
    # subject = st.text_input('Asunto')
    
    body = st.text_area('Petición de inclusión de pueblo/ciudad 📥')
    
    # Hide the password input
    password = st.secrets["password"]
    
    if st.button("✉️ Enviar petición"):
        try:
            msg = MIMEText(body)
            msg['From'] = email_sender
            msg['To'] = email_receiver
            try:
                msg['Subject'] = f"Petición desde {loc['coords']['latitude']}, {loc['coords']['longitude']}"
            except:
                msg['Subject'] = "Desconocido"
    
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_sender, password)
            server.sendmail(email_sender, email_receiver, msg.as_string())
            server.quit()
    
            st.success('Enviado con éxito! 🚀')
        except Exception as e:
            st.error(f"Error al enviar tu petición: {e}")


with tab2:
    st.write('')

    hora_actual = datetime.now().time()
    hora_actual_dt = datetime.combine(datetime.today(), hora_actual)
    hora_sumada = hora_actual_dt + timedelta(hours=2)
    
    hora_actual = hora_sumada.time()
    hora_objetivo = time(12, 00)
    primer_cafe = time(12, 00)
    segundo_cafe = time(14, 00)
    
    if hora_actual < hora_objetivo:
        tiempo_restante = datetime.combine(datetime.today(), hora_objetivo) - datetime.combine(datetime.today(), hora_actual)
    else:
        # Sumamos un día al tiempo objetivo para obtener la próxima ocurrencia
        tiempo_restante = datetime.combine(datetime.today() + timedelta(days=1), hora_objetivo) - datetime.combine(datetime.today(), hora_actual)
    
    horas_restantes = tiempo_restante.seconds // 3600
    minutos_restantes = (tiempo_restante.seconds % 3600) // 60
    
    if hora_actual < segundo_cafe:
        tiempo_restante2 = datetime.combine(datetime.today(), segundo_cafe) - datetime.combine(datetime.today(), hora_actual)
    else:
        # Sumamos un día al tiempo objetivo para obtener la próxima ocurrencia
        tiempo_restante2 = datetime.combine(datetime.today() + timedelta(days=1), segundo_cafe) - datetime.combine(datetime.today(), hora_actual)
    
    horas_restantes2 = tiempo_restante2.seconds // 3600
    minutos_restantes2 = (tiempo_restante2.seconds % 3600) // 60

    st.sidebar.write('')
    if hora_actual > time(18, 00):
        st.sidebar.write(f'¿Un ☕ calentito para una tarde intensa?')
    elif hora_actual < primer_cafe:
        st.sidebar.write(f"Aún tienes {horas_restantes} horas y {minutos_restantes} minutos para el ☕ de la mañana (12:00)")
    elif hora_actual < time(12, 00):
        st.sidebar.write('¿Aún no te has tomado tu café matutino?')
    elif hora_actual < segundo_cafe:
        st.sidebar.write(f"Quedan {horas_restantes2} horas y {minutos_restantes2} minutos para el ☕ post-comida (14:00)")
    else:
        st.sidebar.write('Nunca es mala hora para un ☕')

    st.header("¿Quién quiere café?")
    user_input = st.text_input("Nombres aquí (separados por , )", "")
    user_input = user_input.split(',')
    
    def clean_user_input():
        patron = r'[a-zA-Z]'
        clean = []
        for persona in user_input:
            if re.search(patron, persona) and persona.strip() != "":
                if persona.strip() in ['Adrián', 'Álvaro D.', 'Álvaro S.', 'Ana G.', 'Ana M.', 'Dani A.', 'Dani S.', 'Dasha', 'Inés MG', 'Inés ML', 'Javi B.', 'Javi N.', 'Lucas', 'Lucía', 'María E.', 'María L.', 'Maxi', 'Mercedes', 'Rafa', 'Rosalía', 'Rubén C.', 'Rubén I.', 'Sergio', 'Víctor' ]:
                    clean.append(persona.strip().title().replace('  ',' ')+" ")
                else:
                    clean.append(persona.strip().title().replace('  ',' '))
    
        return clean
        
    st.write('')
    bebidas = ['Café ☕',  'Descafeinado ☕', 'Té Rojo 🔴', 'Té Verde 🟢', 'Té Negro ⚫', 'Manzanilla 🍵', 'Zumo 🍊', 'Cola Cao 🥜', 'Otro 🤔']
    con = ['Leche 🥛', 'Sin Lactosa 🆓', 'Leche Soja 🌿', 'Leche Almendra 🌰','Leche Avena 🥣','Cortado ✂️', 'Solo ❌', '']
    tostadas = ['', 'Cereales 🌾', 'Blanco 🥖', 'Integral 🥔']
    
    x_bebidas = []
    x_con = []
    x_extras = []
    x_tostadas = []
    
    seleccionados = []
    
    # try:
    
    for persona2 in clean_user_input():
    
        try:
    
            col10, col20, col30, col40, col50 = st.columns(5)
            st.write('-----------------')
    
            seleccion2 = col10.checkbox(persona2)
    
            if seleccion2:
                seleccionados.append(persona2)
    
                bebida_seleccionada = col20.selectbox(f"Bebida de {persona2}", bebidas)
                con_seleccionada = col30.selectbox(f"'Con' de {persona2}", con)
                extras = col40.text_input(f"Extras de {persona2}")
                barrita = col50.selectbox(f"Tostada de {persona2}", tostadas)
    
                x_bebidas.append(bebida_seleccionada)
                x_con.append(con_seleccionada)
                x_extras.append(extras)
                x_tostadas.append(barrita)
    
        except:
            st.warning(f'**{persona2.strip()}** ya ha sido añadido a la lista previamente. Prueba con otro nombre.')
    
    st.write('')
    st.write('')

    # Inyectar CSS personalizado para ajustar el margen
    st.markdown("""
    <style>
    # /* Reducir el margen inferior del título Markdown */
    # div[data-testid="stMarkdownContainer"] {
    #     margin-bottom: -20px !important;
    # }
    /* Reducir el margen superior del widget radio para acercarlo al título */
    .stRadio > div {
        margin-top: -30px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Utilizando Markdown para añadir estilo al título
    st.markdown('#### ¿Para llevar?')
    
    # Widget de selección sin formato específico en la pregunta
    para_llevar = st.radio(" ", ["Sí, el trabajo nos reclama 💻", "No, necesitamos un descanso 🤯"], index=1)
    
    st.write('-------------------')
    
    # st.write(x_bebidas, x_con, x_extras)
    
    coffees = []
    for i,e in enumerate(x_bebidas):
        if e == 'Café ☕' and x_con[i] == '':
            coffees.append(f'{e} Solo {x_extras[i]}')
        
        elif x_con[i] != 'Cortado ✂️' and x_con[i] != 'Solo ❌' and x_con[i] != '' and x_extras[i] != '':
            coffees.append(f'{e} con {x_con[i]} {x_extras[i]}')
    
        elif x_con[i] != 'Cortado ✂️' and x_con[i] != 'Solo ❌' and x_con[i] != '':
            coffees.append(f'{e} con {x_con[i]} {x_extras[i]}')
    
        elif e == 'Otro 🤔':
            coffees.append(f'{x_extras[i]}')
    
        else:
            coffees.append(f'{e} {x_con[i]} {x_extras[i]}')
            
    
    # st.write(sorted(coffees))
    
    # st.write(seleccionados)

    if len(seleccionados) > 0:
    
        st.write('')
        st.write('')
        st.markdown('##### 📝 Comanda Versión Emoji')
        conteo = Counter(coffees)
        conteo = dict(sorted(conteo.items()))
        n_tostadas = Counter(x_tostadas)
        n_tostadas = dict(sorted(n_tostadas.items()))
        n_tostadas = {clave: valor for clave, valor in n_tostadas.items() if clave != ""}
    
        # st.write(n_tostadas)
    
        pedido_str = 'Hola! Os hago un pedido:\n\n'
    
        for key, value in conteo.items():
            pedido_str += "• {} {}\n".format(value, key)
            
        if len(n_tostadas) > 0:
            pedido_str +='\nBarritas de pan:\n'
            for key, value in n_tostadas.items():
                pedido_str += "• {} {}\n".format(value, key)
    
        if para_llevar == "Sí, el trabajo nos reclama 💻":
            pedido_str += '\n(Todos para llevar y con leche templada)\n'
        else:
            pedido_str += '\n(Todos con leche templada)\n'
    
        pedido_str += 'Muchas gracias! 🙂'
    
        st.code(pedido_str)
    
    # ---------------------------------------------------------------------------
    
        st.write('')
        st.write('')
        st.markdown('##### 📑 Comanda Versión Esquema')
    
        ccl = 0
        ccl_sinlact = 0
        ccl_soja = 0
        ccl_almendra = 0
        ccl_avena = 0
        ccl_desnat = 0
    
        dcl = 0
        dcl_sinlact = 0
        dcl_soja = 0
        dcl_almendra = 0
        dcl_avena = 0
        dcl_desnat = 0
    
        solo = 0
        lardob = 0
        largo = 0
        doble = 0
    
        te = 0
        rojo = 0
        rojo_leche = 0
        rojo_sinlac= 0
        rojo_soja = 0
        rojo_almendra = 0
        rojo_avena = 0
        verde = 0
        verde_leche = 0
        verde_sinlac= 0
        verde_soja = 0
        verde_almendra = 0
        verde_avena = 0
        negro = 0
        negro_leche = 0
        negro_sinlac = 0
        negro_soja = 0
        negro_almendra = 0
        negro_avena = 0
    
        colacao = 0
        colacao_sinlact = 0
        colacao_soja = 0
        colacao_almendra = 0
        colacao_avena = 0
        colacao_desnat = 0
        
        zumo = 0
        
        manzanilla = 0
    
        otros = 0
    
        que = {}
    
    
        for k, v in conteo.items():
    
            if "Café" in k and ("Leche 🥛" in k or "Sin Lactosa" in k or "Leche Soja" in k or "Leche Almendra" in k or "Leche Avena" in k):
                ccl += v
                if "Sin Lactosa" in k:
                    ccl_sinlact += v
                elif "Desnatada" in k:
                    ccl_desnat += v
                elif "Leche Soja" in k:
                    ccl_soja += v   
                elif "Leche Almendra" in k:
                    ccl_almendra += v   
                elif "Leche Avena" in k:
                    ccl_avena += v   
    
            elif "Descafeinado" in k:
                dcl += v
                if "Sin Lactosa" in k:
                    dcl_sinlact += v
                elif "Desnatada" in k:
                    dcl_desnat += v
                elif "Leche Soja" in k:
                    dcl_soja += v  
                elif "Leche Almendra" in k:
                    dcl_almendra += v   
                elif "Leche Avena" in k:
                    dcl_avena += v   
    
            elif ("Café" in k or "Descafeinado" in k) and ("Solo" in k or '  ' in k):
                solo += v
                if "Largo" in k and "Doble" in k:
                    lardob += v
                elif "Largo" in k:
                    largo += v
                elif "Doble" in k:
                    doble += v
                                       
            elif "Té" in k:
                te += v
                if "Rojo" in k:
                    if "Leche 🥛" in k:
                        rojo_leche += v
                    elif "Sin Lactosa" in k:
                        rojo_sinlac += v
                    elif "Leche Soja" in k:
                        rojo_soja += v
                    elif "Leche Almendra" in k:
                        rojo_almendra += v
                    elif "Leche Avena" in k:
                        rojo_avena += v
                    else:
                        rojo += v
                    
                if "Verde" in k:
                    if "Leche 🥛" in k:
                        verde_leche += v
                    elif "Sin Lactosa" in k:
                        verde_sinlac += v
                    elif "Leche Soja" in k:
                        verde_soja += v
                    elif "Leche Almendra" in k:
                        verde_almendra += v
                    elif "Leche Avena" in k:
                        verde_avena += v
                    else:
                        verde += v
                    
                if "Negro" in k:
                    if "Leche 🥛" in k:
                        negro_leche += v
                    elif "Sin Lactosa" in k:
                        negro_sinlac += v
                    elif "Leche Soja" in k:
                        negro_soja += v
                    elif "Leche Almendra" in k:
                        negro_almendra += v
                    elif "Leche Avena" in k:
                        negro_Avena += v
                    else:
                        negro += v
    
            elif "Cola Cao" in k:
                colacao += v
                if "Sin Lactosa" in k:
                    colacao_sinlact += v
                elif "Desnatada" in k:
                    colacao_desnat += v
                elif "Leche Soja" in k:
                    colacao_soja += v   
                elif "Leche Almendra" in k:
                    colacao_almendra += v   
                elif "Leche Avena" in k:
                    colacao_avena += v   
    
            elif "Zumo" in k:
                zumo += v
                
            elif "Manzanilla 🍵" in k:
                manzanilla += v
    
            else:
                otros += v
                que[k] = v
                
        cereal = 0
        blanco = 0
        integral = 0
    
        for k, v in n_tostadas.items():
            if "Cereales" in k:
                cereal += v
            elif "Blanco" in k:
                blanco += v
            elif "Integral" in k:
                integral += v
    
        # ----------------------------------------------------------------------------------------
    
        output = []
    
        output.append('Hola! Os hago un pedido:\n')
        
        ccl_normales = ccl - ccl_sinlact - ccl_desnat - ccl_soja - ccl_almendra - ccl_avena
        dcl_normales = dcl - dcl_sinlact - dcl_desnat - dcl_soja - dcl_almendra - dcl_avena
        solo_normales = solo - lardob - largo - doble
    
        
        if ccl > 0:
            if ccl > 1:
                if ccl_sinlact > 0 and (ccl_desnat + ccl_soja + ccl_almendra + ccl_avena + ccl_normales == 0):
                    output.append(f'• {ccl_sinlact} café con leche sin lactosa')
    
                elif ccl_desnat > 0 and (ccl_sinlact + ccl_soja + ccl_almendra + ccl_avena + ccl_normales == 0):
                    output.append(f'• {ccl_desnat} café con leche desnatada')
    
                elif ccl_soja > 0 and (ccl_desnat + ccl_almendra + ccl_sinlact + ccl_avena + ccl_normales == 0):
                    output.append(f'• {ccl_soja} café con leche de soja')
                    
                elif ccl_almendra > 0 and (ccl_desnat + ccl_soja + ccl_sinlact + ccl_avena + ccl_normales == 0):
                    output.append(f'• {ccl_almendra} café con leche de almendra')
    
                elif ccl_avena > 0 and (ccl_desnat + ccl_sinlact + ccl_soja + ccl_almendra + ccl_normales == 0):
                    output.append(f'• {ccl_avena} café con leche de avena')
                    
                elif ccl_sinlact > 0 or ccl_desnat > 0 or ccl_soja > 0 or ccl_almendra > 0 or ccl_avena > 0:
                    output.append(f'• {ccl} cafés con leche, de los cuales:')
                    if ccl_normales > 0:
                        output.append(f'   - {ccl_normales} normal')
                    if ccl_sinlact > 0:
                        output.append(f'   - {ccl_sinlact} sin lactosa')
                    if ccl_desnat > 0:
                        output.append(f'   - {ccl_desnat} desnatada')
                    if ccl_soja > 0:
                        output.append(f'   - {ccl_soja} soja')
                    if ccl_almendra > 0:
                        output.append(f'   - {ccl_almendra} almendra')
                    if ccl_avena > 0:
                        output.append(f'   - {ccl_avena} avena')
                else:
                    output.append(f'• {ccl} café con leche')
    
            else:
                if ccl_normales > 0 or ccl_sinlact > 0 or ccl_desnat > 0 or ccl_soja > 0 or ccl_almendra > 0 or ccl_avena > 0:
                    if ccl_normales > 0:
                        output.append(f'• {ccl_normales} café con leche')
                    if ccl_sinlact > 0:
                        output.append(f'• {ccl_sinlact} café con leche sin lactosa')
                    if ccl_desnat > 0:
                        output.append(f'• {ccl_desnat} café con leche desnatada')
                    if ccl_soja > 0:
                        output.append(f'• {ccl_soja} café con leche de soja')
                    if ccl_almendra > 0:
                        output.append(f'• {ccl_almendra} café con leche de almendra')
                    if ccl_avena > 0:
                        output.append(f'• {ccl_avena} café con leche de avena')
        
    
        if dcl > 0:
            if dcl > 1:
                if dcl_sinlact > 0 and (dcl_desnat + dcl_soja + dcl_almendra + dcl_avena + dcl_normales == 0):
                    output.append(f'• {dcl_sinlact} descafeinado con leche sin lactosa')
    
                elif dcl_desnat > 0 and (dcl_sinlact + dcl_soja + dcl_almendra + dcl_avena + dcl_normales == 0):
                    output.append(f'• {dcl_desnat} descafeinado con leche desnatada')
    
                elif dcl_soja > 0 and (dcl_desnat + dcl_almendra + dcl_sinlact + dcl_avena + dcl_normales == 0):
                    output.append(f'• {dcl_soja} descafeinado con leche de soja')
                    
                elif dcl_almendra > 0 and (dcl_desnat + dcl_soja + dcl_sinlact + dcl_avena + dcl_normales == 0):
                    output.append(f'• {dcl_almendra} descafeinado con leche de almendra')
    
                elif dcl_avena > 0 and (dcl_desnat + dcl_soja + dcl_sinlact + dcl_almendra + dcl_normales == 0):
                    output.append(f'• {dcl_avena} descafeinado con leche de avena')
                    
                elif dcl_sinlact > 0 or dcl_desnat > 0 or dcl_soja > 0 or dcl_almendra > 0 or dcl_avena > 0:
                    output.append(f'• {dcl} descafeinados con leche, de los cuales:')
                    if dcl_normales > 0:
                        output.append(f'   - {dcl_normales} normal')
                    if dcl_sinlact > 0:
                        output.append(f'   - {dcl_sinlact} sin lactosa')
                    if dcl_desnat > 0:
                        output.append(f'   - {dcl_desnat} desnatada')
                    if dcl_soja > 0:
                        output.append(f'   - {dcl_soja} soja')
                    if dcl_almendra > 0:
                        output.append(f'   - {dcl_almendra} almendra')
                    if dcl_avena > 0:
                        output.append(f'   - {dcl_avena} avena')
                else:
                    output.append(f'• {dcl} descafeinado con leche')
    
            else:
                if dcl_normales > 0 or dcl_sinlact > 0 or dcl_desnat > 0 or dcl_soja > 0 or dcl_almendra > 0 or dcl_avena > 0:
                    if dcl_normales > 0:
                        output.append(f'• {dcl_normales} descafeinado con leche')
                    if dcl_sinlact > 0:
                        output.append(f'• {dcl_sinlact} descafeinado con leche sin lactosa')
                    if dcl_desnat > 0:
                        output.append(f'• {dcl_desnat} descafeinado con leche desnatada')
                    if dcl_soja > 0:
                        output.append(f'• {dcl_soja} descafeinado con leche de soja')
                    if dcl_almendra > 0:
                        output.append(f'• {dcl_almendra} descafeinado con leche de almendra')
                    if dcl_avena > 0:
                        output.append(f'• {dcl_avena} descafeinado con leche de avena')
    
    # --------------- solos ----------------------------------------------------------------------------------------
        
        solos_normales = solo - lardob - largo - doble
        
        if solo > 0:
            if solo > 1:
                if lardob > 0 and (largo + doble + solos_normales == 0):
                    output.append(f'• {lardob} café solo largo doble')
    
                elif largo > 0 and (lardob + doble + solos_normales == 0):
                    output.append(f'• {largo} café solo largo')
                    
                elif doble > 0 and (largo + lardob + solos_normales == 0):
                    output.append(f'• {doble} café solo doble')
                    
                elif lardob > 0 or largo > 0 or doble > 0:
                    output.append(f'• {solo} cafés solo, de los cuales:')
                    if solos_normales > 0:
                        output.append(f'   - {solos_normales} normal')
                    if lardob > 0:
                        output.append(f'   - {lardob} largo doble')
                    if largo > 0:
                        output.append(f'   - {largo} largo')
                    if doble > 0:
                        output.append(f'   - {doble} doble')
                else:
                    output.append(f'• {solo} café solo')
    
            else:
                if solos_normales > 0 or lardob > 0 or largo > 0 or doble > 0:
                    if solos_normales > 0:
                        output.append(f'• {solos_normales} café solo')
                    if lardob > 0:
                        output.append(f'• {lardob} café solo largo doble')
                    if largo > 0:
                        output.append(f'• {largo} café largo')
                    if doble > 0:
                        output.append(f'• {doble} café doble')
    
    
        if te > 0:
            if te > 1:
                if rojo > 0 and (rojo_leche + rojo_sinlac + rojo_soja + rojo_almendra + rojo_avena + verde + verde_leche + verde_sinlac + verde_soja + verde_almendra + verde_avena + negro + negro_leche + negro_sinlac + negro_soja + negro_almendra + negro_avena == 0):
                    output.append(f'• {rojo} té rojo')
    
                elif rojo_leche > 0 and (rojo + rojo_sinlac + rojo_soja + rojo_almendra + rojo_avena + verde + verde_leche + verde_sinlac + verde_soja + verde_almendra + verde_avena + negro + negro_leche + negro_sinlac + negro_soja + negro_almendra + negro_avena == 0):
                    output.append(f'• {rojo_leche} té rojo con leche')
                    
                elif rojo_sinlac > 0 and (rojo + rojo_leche + rojo_soja + rojo_almendra + rojo_avena + verde + verde_leche + verde_sinlac + verde_soja + verde_almendra + verde_avena + negro + negro_leche + negro_sinlac + negro_soja + negro_almendra + negro_avena == 0):
                    output.append(f'• {rojo_sinlac} té rojo con leche sin lactosa')
    
                elif rojo_soja > 0 and (rojo + rojo_leche + rojo_sinlac + rojo_almendra + rojo_avena + verde + verde_leche + verde_sinlac + verde_soja + verde_almendra + verde_avena + negro + negro_leche + negro_sinlac + negro_soja + negro_almendra + negro_avena == 0):
                    output.append(f'• {rojo_soja} té rojo con leche de soja')
    
                elif rojo_almendra > 0 and (rojo + rojo_leche + rojo_sinlac + rojo_soja + rojo_avena + verde + verde_leche + verde_sinlac + verde_soja + verde_almendra + verde_avena + negro + negro_leche + negro_sinlac + negro_soja + negro_almendra + negro_avena == 0):
                    output.append(f'• {rojo_almendra} té rojo con leche de almendra')
    
                elif rojo_avena > 0 and (rojo + rojo_leche + rojo_sinlac + rojo_soja + rojo_almendra + verde + verde_leche + verde_sinlac + verde_soja + verde_almendra + verde_avena + negro + negro_leche + negro_sinlac + negro_soja + negro_almendra + negro_avena == 0):
                    output.append(f'• {rojo_avena} té rojo con leche de avena')
    
                elif verde > 0 and (rojo + rojo_leche + rojo_sinlac + rojo_soja + rojo_almendra + rojo_avena + verde_leche + verde_sinlac + verde_soja + verde_almendra + verde_avena + negro + negro_leche + negro_sinlac + negro_soja + negro_almendra + negro_avena == 0):
                    output.append(f'• {verde} té verde')
    
                elif verde_leche > 0 and (rojo + rojo_leche + rojo_sinlac + rojo_soja + rojo_almendra + rojo_avena + verde + verde_sinlac + verde_soja + verde_almendra + verde_avena + negro + negro_leche + negro_sinlac + negro_soja + negro_almendra + negro_avena == 0):
                    output.append(f'• {verde_leche} té verde con leche')
                    
                elif verde_sinlac > 0 and (rojo + rojo_leche + rojo_sinlac + rojo_soja + rojo_almendra + rojo_avena + verde + verde_leche + verde_soja + verde_almendra + verde_avena + negro + negro_leche + negro_sinlac + negro_soja + negro_almendra + negro_avena == 0):
                    output.append(f'• {verde_sinlac} té verde con leche sin lactosa')
    
                elif verde_soja > 0 and (rojo + rojo_leche + rojo_sinlac + rojo_soja + rojo_almendra + rojo_avena + verde + verde_leche + verde_sinlac + verde_almendra +  verde_avena + negro + negro_leche + negro_sinlac + negro_soja + negro_almendra + negro_avena == 0):
                    output.append(f'• {verde_soja} té verde con leche de soja')
    
                elif verde_almendra > 0 and (rojo + rojo_leche + rojo_sinlac + rojo_soja + rojo_almendra + rojo_avena + verde + verde_leche + verde_sinlac + verde_soja + verde_avena + negro + negro_leche + negro_sinlac + negro_soja + negro_almendra + negro_avena == 0):
                    output.append(f'• {verde_almendra} té verde con leche de almendra')
    
                elif verde_avena > 0 and (rojo + rojo_leche + rojo_sinlac + rojo_soja + rojo_almendra + rojo_avena + verde + verde_leche + verde_sinlac + verde_soja + verde_almendra + negro + negro_leche + negro_sinlac + negro_soja + negro_almendra + negro_avena == 0):
                    output.append(f'• {verde_avena} té verde con leche de avena')
    
                elif negro > 0 and (rojo + rojo_leche + rojo_sinlac + rojo_soja + rojo_almendra + rojo_avena + verde + verde_leche + verde_sinlac + verde_soja + verde_almendra + verde_avena + negro_leche + negro_sinlac + negro_soja + negro_almendra + negro_avena == 0):
                    output.append(f'• {negro} té negro')
    
                elif negro_leche > 0 and (rojo + rojo_leche + rojo_sinlac + rojo_soja + rojo_almendra + rojo_avena + verde + verde_leche + verde_sinlac + verde_soja + verde_almendra + verde_avena + negro + negro_sinlac + negro_soja + negro_almendra + negro_avena == 0):
                    output.append(f'• {negro_leche} té negro con leche')
                    
                elif negro_sinlac > 0 and (rojo + rojo_leche + rojo_sinlac + rojo_soja + rojo_almendra + rojo_avena + verde + verde_leche + verde_sinlac + verde_soja + verde_almendra + verde_avena + negro + negro_leche + negro_soja + negro_almendra + negro_avena == 0):
                    output.append(f'• {negro_sinlac} té negro con leche sin lactosa')
    
                elif negro_soja > 0 and (rojo + rojo_leche + rojo_sinlac + rojo_soja + rojo_almendra + rojo_avena + verde + verde_leche + verde_sinlac + verde_soja + verde_almendra + verde_avena + negro + negro_leche + negro_sinlac + negro_almendra + negro_avena == 0):
                    output.append(f'• {negro_soja} té negro con leche de soja')
    
                elif negro_almendra > 0 and (rojo + rojo_leche + rojo_sinlac + rojo_soja + rojo_almendra + rojo_avena + verde + verde_leche + verde_sinlac + verde_soja + verde_almendra + verde_avena + negro + negro_leche + negro_sinlac + negro_soja + negro_avena == 0):
                    output.append(f'• {negro_almendra} té negro con leche de almendra')
    
                elif negro_avena > 0 and (rojo + rojo_leche + rojo_sinlac + rojo_soja + rojo_almendra + rojo_avena + verde + verde_leche + verde_sinlac + verde_soja + verde_almendra + verde_avena + negro + negro_leche + negro_sinlac + negro_soja + negro_almendra == 0):
                    output.append(f'• {negro_avena} té negro con leche de avena')
                    
                elif rojo > 0 or rojo_leche > 0 or rojo_sinlac > 0 or rojo_almendra > 0 or rojo_soja > 0 or rojo_avena > 0 or verde > 0 or verde_leche > 0 or verde_sinlac > 0 or verde_almendra > 0 or verde_soja > 0 or verde_avena > 0 or negro > 0 or negro_leche > 0 or negro_sinlac > 0 or negro_almendra > 0 or negro_soja > 0 or negro_avena > 0:
                    output.append(f'• {te} tés, de los cuales:')
    
                    if rojo > 0:
                        output.append(f'   - {rojo} té rojo')
                    if rojo_leche > 0:
                        output.append(f'   - {rojo_leche} té rojo con leche')
                    if rojo_sinlac > 0:
                        output.append(f'   - {rojo_sinlac} té rojo con leche sin lactosa')
                    if rojo_soja > 0:
                        output.append(f'   - {rojo_soja} té rojo con leche de soja')
                    if rojo_almendra > 0:
                        output.append(f'   - {rojo_almendra} té rojo con leche de almendra')
                    if rojo_avena > 0:
                        output.append(f'   - {rojo_avena} té rojo con leche de avena')
                    if verde > 0:
                        output.append(f'   - {verde} té verde')
                    if verde_leche > 0:
                        output.append(f'   - {verde_leche} té verde con leche')
                    if verde_sinlac > 0:
                        output.append(f'   - {verde_sinlac} té verde con leche sin lactosa')
                    if verde_soja > 0:
                        output.append(f'   - {verde_soja} té verde con leche de soja')
                    if verde_almendra > 0:
                        output.append(f'   - {verde_almendra} té verde con leche de almendra')
                    if verde_avena > 0:
                        output.append(f'   - {verde_avena} té verde con leche de avena')
                    if negro > 0:
                        output.append(f'   - {negro} té negro')
                    if negro_leche > 0:
                        output.append(f'   - {negro_leche} té negro con leche')
                    if negro_sinlac > 0:
                        output.append(f'   - {negro_sinlac} té negro con leche sin lactosa')
                    if negro_soja > 0:
                        output.append(f'   - {negro_soja} té negro con leche de soja')
                    if negro_almendra > 0:
                        output.append(f'   - {negro_almendra} té negro con leche de almendra')
                    if negro_avena > 0:
                        output.append(f'   - {negro_avena} té negro con leche de avena')
            
            else:
                 if rojo > 0 or rojo_leche > 0 or rojo_sinlac > 0 or rojo_soja > 0  or rojo_almendra > 0 or rojo_avena > 0 or verde > 0 or verde_leche > 0 or verde_sinlac > 0 or verde_soja > 0 or verde_almendra > 0 or verde_avena > 0 or negro > 0 or negro_leche > 0 or negro_sinlac > 0  or negro_soja > 0  or negro_almendra > 0  or negro_avena > 0:
                    if rojo > 0:
                        output.append(f'• {rojo} té rojo')
                    if rojo_leche > 0:
                        output.append(f'• {rojo_leche} té rojo con leche')
                    if rojo_sinlac > 0:
                        output.append(f'• {rojo_sinlac} té rojo con leche sin lactosa')
                    if rojo_soja > 0:
                        output.append(f'• {rojo_soja} té rojo con leche de soja')
                    if rojo_almendra > 0:
                        output.append(f'• {rojo_almendra} té rojo con leche de almendra')
                    if rojo_avena > 0:
                        output.append(f'• {rojo_avena} té rojo con leche de avena')
                    if verde > 0:
                        output.append(f'• {verde} té verde')
                    if verde_leche > 0:
                        output.append(f'• {verde_leche} té verde con leche')
                    if verde_sinlac > 0:
                        output.append(f'• {verde_sinlac} té verde con leche sin lactosa')   
                    if verde_soja > 0:
                        output.append(f'• {verde_soja} té verde con leche de soja')
                    if verde_almendra > 0:
                        output.append(f'• {verde_almendra} té verde con leche de almendra')
                    if verde_avena > 0:
                        output.append(f'• {verde_avena} té verde con leche de avena')
                    if negro > 0:
                        output.append(f'• {negro} té negro')
                    if negro_leche > 0:
                        output.append(f'• {negro_leche} té negro con leche')
                    if negro_sinlac > 0:
                        output.append(f'• {negro_sinlac} té negro con leche sin lactosa')
                    if negro_soja > 0:
                        output.append(f'• {negro_soja} té negro con leche de soja')
                    if negro_almendra > 0:
                        output.append(f'• {negro_almendra} té negro con leche de almendra')
                    if negro_avena > 0:
                        output.append(f'• {negro_avena} té negro con leche de avena')
    
    
        # if colacao > 0:
        #     output.append(f'• {colacao} cola cao')
    
        colacao_normales = colacao - colacao_sinlact - colacao_desnat - colacao_soja + colacao_almendra - colacao_avena
    
        if colacao > 0:
            if colacao > 1:
                if colacao_sinlact > 0 and (colacao_desnat + colacao_soja + colacao_almendra + colacao_avena + colacao_normales == 0):
                    output.append(f'• {colacao_sinlact} Cola Cao con leche sin lactosa')
    
                elif colacao_desnat > 0 and (colacao_sinlact + colacao_soja + colacao_almendra + colacao_avena + colacao_normales == 0):
                    output.append(f'• {colacao_desnat} Cola Cao con leche desnatada')
    
                elif colacao_soja > 0 and (colacao_desnat + colacao_sinlact + colacao_almendra + colacao_avena + colacao_normales == 0):
                    output.append(f'• {colacao_soja} Cola Cao con leche de soja')
                    
                elif colacao_almendra > 0 and (colacao_desnat + colacao_sinlact + colacao_soja + colacao_avena + colacao_normales == 0):
                    output.append(f'• {colacao_almendra} Cola Cao con leche de almendra')
    
                elif colacao_avena > 0 and (colacao_desnat + colacao_sinlact + colacao_soja + colacao_almendra + colacao_normales == 0):
                    output.append(f'• {colacao_avena} Cola Cao con leche de avena')
                    
                elif colacao_sinlact > 0 or colacao_desnat > 0 or colacao_soja > 0 or colacao_almendra > 0 or colacao_avena > 0:
                    output.append(f'• {colacao} Cola Cao, de los cuales:')
                    if colacao_normales > 0:
                        output.append(f'   - {colacao_normales} leche normal')
                    if colacao_sinlact > 0:
                        output.append(f'   - {colacao_sinlact} sin lactosa')
                    if colacao_desnat > 0:
                        output.append(f'   - {colacao_desnat} desnatada')
                    if colacao_soja > 0:
                        output.append(f'   - {colacao_soja} soja')
                    if colacao_almendra > 0:
                        output.append(f'   - {colacao_almendra} almendra')
                    if colacao_avena > 0:
                        output.append(f'   - {colacao_avena} avena')
                else:
                    output.append(f'• {colacao} Cola Cao')
    
            else:
                if colacao > 0 or colacao_sinlact > 0 or colacao_desnat > 0 or colacao_soja > 0 or colacao_almendra > 0 or colacao_avena > 0:
                    if colacao_normales > 0:
                        output.append(f'• {colacao_normales} Cola Cao con leche normal')
                    if colacao_sinlact > 0:
                        output.append(f'• {colacao_sinlact} Cola Cao con leche sin lactosa')
                    if colacao_desnat > 0:
                        output.append(f'• {colacao_desnat} Cola Cao con leche desnatada')
                    if colacao_soja > 0:
                        output.append(f'• {colacao_soja} Cola Cao con leche de soja')
                    if colacao_almendra > 0:
                        output.append(f'• {colacao_almendra} Cola Cao con leche de almendra')
                    if colacao_avena > 0:
                        output.append(f'• {colacao_avena} Cola Cao con leche de avena')
    
        if zumo > 0:
            output.append(f'• {zumo} zumo de naranja')
            
        if manzanilla > 0:
            output.append(f'• {manzanilla} manzanilla')
    
        if otros > 0:
            info = str(tuple([f'{v} {k}' for k, v in que.items()])).replace("'", "")
            if len(que) < 2:
                info = info.replace(',','')
            output.append(f'• {otros} otros: {info}')
            
        if len(n_tostadas) > 0:
            output.append('\nBarritas de pan:')
            if cereal > 0:
                output.append(f'• {cereal} de cereales')
            if blanco > 0:
                output.append(f'• {blanco} blanco')
            if integral > 0:
                output.append(f'• {integral} integral')
    
        if para_llevar == "Sí, el trabajo nos reclama 💻":
            output.append('\n(Todos para llevar y con leche templada)')
        else:
            output.append('\n(Todos con leche templada)')
    
        output.append('Muchas gracias! 🙂')
    
        st.code('\n'.join(output), language='plaintext')
    
        st.write('----------------')
    
    # except: 
    #     pass
    
    st.write('')
    st.write('')
    
    if len(seleccionados) > 0:
        st.markdown('#### 🙋‍♀️🙋‍♂️ Los cafeteros de hoy son:')
    s = ''
    for n in seleccionados:
        s += "- " + n.replace('*','') + "\n"
    st.markdown(s)
    st.write('')
    # st.write('')
    
    n_cafeteros = len(seleccionados)
    
    col1, col2, col3, col4 = st.columns(4)
    media_habitual = col4.number_input('Media habitual: ', value=6)
    col1.metric("Cafeteros hoy", n_cafeteros, f"{n_cafeteros-media_habitual} de lo habitual")
    
    try:
        perc_total = int((len(seleccionados)/len(clean_user_input()))*100)
        col2.metric("% Hoy vs Total", f'{perc_total}%', f"{perc_total-100}% del total")
    except:
        # perc_total = 1
        # col2.metric("% Hoy vs Total", f'{perc_total}%', f"Métrica no disponible")
        col2.warning('Métrica no disponible')
    
    perc_hab = int((len(seleccionados)/media_habitual)*100)
    col3.metric("% Hoy vs Habitual", f'{perc_hab}%', f"{perc_hab-100}% de lo habitual")
