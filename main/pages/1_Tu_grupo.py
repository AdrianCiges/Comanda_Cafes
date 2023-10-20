import streamlit as st
from collections import Counter
from PIL import Image
import base64
import io
import datetime
from datetime import datetime, time, timedelta
import re
import streamlit.components.v1 as components
import time as timee
#import pywhatkit

st.set_page_config(layout="wide", page_title="Coffees", page_icon="./img/cafe5.png")

# Cambiar el tema de la página principal
st.markdown(
    """
    <style>
    .stApp {
        background-color: #e9ecef;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Texto principal
texto_principal = '<h1 style="text-align:center"><span style="font-size: 40px;">☕</span> <u>LA RUTA DEL CAFÉ</u></h1>'

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


# Ruta de la imagen del logo
LOGO_IMAGE = "./img/granos.png"

# Texto principal
texto_principal = '<h1 style="text-align:center"><span style="font-size: 40px;">☕</span> <u>LA RUTA DEL CAFÉ</u></h1>'
    
# Leer la imagen del logo y codificarla en base64
with open(LOGO_IMAGE, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# Mostrar el texto principal y el logo
st.markdown(estilos_css, unsafe_allow_html=True)
st.markdown(
    f'<div class="logo-container">{texto_principal}<img src="data:image/png;base64,{encoded_image}" class="logo-img"></div>',
    unsafe_allow_html=True
)

st.header("¿Quién quiere café?")
user_input = st.text_input("Nombres aquí", "")
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
para_llevar = st.radio('¿PARA LLEVAR? ', ["Sí, el trabajo nos reclama 💻", "No, necesitamos un descanso 🤯"], index=1)

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
st.write('')

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

# col4.metric("Media habitual", 6)
# col4.metric("Media habitual", insert_number)
