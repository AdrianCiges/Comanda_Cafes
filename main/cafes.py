import streamlit as st
from collections import Counter
from PIL import Image
import base64
import io

st.set_page_config(layout="wide", page_title="Coffees", page_icon="./img/cafe5.png")

# -------------------------------------------------------------------------------------------------------------------
from datetime import datetime, time, timedelta
hora_actual = datetime.now().time()
hora_actual_dt = datetime.combine(datetime.today(), hora_actual)
hora_sumada = hora_actual_dt + timedelta(hours=2)

hora_actual = hora_sumada.time()
hora_objetivo = time(10, 30)
primer_cafe = time(10, 30)
segundo_cafe = time(14, 45)

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
    st.sidebar.write(f'Mira que horas son, no deberías estar aquí, pero faltan {horas_restantes} horas y {minutos_restantes} minutos para el ☕ de las 10:30')
elif hora_actual < primer_cafe:
    st.sidebar.write(f"{horas_restantes} horas y {minutos_restantes} minutos para el ☕ de las 10:30")
elif hora_actual < time(11, 00):
    st.sidebar.write('Ya deberías estar tomándote un café con los compis')
elif hora_actual < segundo_cafe:
    st.sidebar.write(f"{horas_restantes2} horas y {minutos_restantes2} minutos para el ☕ de las 14:45")
else:
    st.sidebar.write('No hay más cafés hoy ☹')

# -------------------------------------------------------------------------------------------------------------------

# Cambiar el tema de la barra lateral
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

image_inicio = Image.open("./img/havas.png")
with io.BytesIO() as output:
    image_inicio.save(output, format="PNG")
    b64_1 = base64.b64encode(output.getvalue()).decode()
    
# st.image(f"data:image/png;base64,{b64_1}", use_column_width=False)
    
# st.markdown(f'<h1 style="text-align:center"><span style="font-size: 40px;">☕</span> <u>LA RUTA DEL BUEN CAFÉ</u></h1>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------------------

# # Ruta de la imagen del logo
# LOGO_IMAGE = "./img/havas.png"

# # Texto principal
# texto_principal = '<h1 style="text-align:center"><span style="font-size: 40px;">☕</span> <u>LA RUTA DEL BUEN CAFÉ</u></h1>'

# # Estilos CSS para el logo
# estilos_css = f"""
#     <style>
#     .logo-container {{
#         display: flex;
#         align-items: center;
#         justify-content: center;
#     }}

#     .logo-img {{
#         max-height: 100px;
#         margin-left: 20px;
#     }}
#     </style>
#     """

# # Mostrar el texto principal y el logo
# st.markdown(estilos_css, unsafe_allow_html=True)
# st.markdown(f'<div class="logo-container">{texto_principal}<img src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}" class="logo-img"></div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------------------


# Ruta de la imagen del logo
LOGO_IMAGE = "./img/havas.png"

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

# Leer la imagen del logo y codificarla en base64
with open(LOGO_IMAGE, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# Mostrar el texto principal y el logo
st.markdown(estilos_css, unsafe_allow_html=True)
st.markdown(
    f'<div class="logo-container">{texto_principal}<img src="data:image/png;base64,{encoded_image}" class="logo-img"></div>',
    unsafe_allow_html=True
)

# ----------------------------------------------------------------------------------------

# Botón para añadir una persona más
col1, col2 = st.sidebar.columns(2)
# nuevos = st.sidebar.selectbox("¿Añadir gente nueva? ¿Cuántos?", [0,1,2,3,4,5,6,7,8,9,10])
nuevos = st.sidebar.number_input(label = '¿Añadir gente nueva? ¿Cuántos?', min_value=0, value=0, step=1)

col1, col2 = st.sidebar.columns(2)
if nuevos > 0:
    gente_nueva = []
    for i in range(nuevos):
        gente_nueva.append(col1.text_input(f'Nombre {i+1}'))
    gente_nueva = [g for g in gente_nueva if g != '']

def gente():
    personas = ['Adrián*', 'Álvaro Bayón', 'Álvaro Delgado*', 'Álvaro Saez', 'Ana García*', 'Ana Murillo', 'Dani A.', 'Dani S.', 'Dasha', 'Inés MG', 'Inés ML*', 'Iván', 'Javi Brenes', 'Javi Nieto*', 'Lucía', 'María', 'Maxi', 'Mercedes*', 'Rafa', 'Sergio*', 'Víctor' ]   
    try:
        return personas + gente_nueva
    except:
        return personas

st.header("¿Quiénes bajamos?")
st.write('')
bebidas = ['Café ☕',  'Descafeinado ☕', 'Té Rojo 🔴', 'Té Verde 🟢', 'Té Negro ⚫', 'Manzanilla 🍵', 'Zumo 🍊', 'Cola Cao 🥜', 'Otro']
con = ['Leche 🥛', 'Sin Lactosa', 'Cortado', 'Solo', '']
tostadas = ['', 'Cereales 🌾', 'Blanco 🥖', 'Integral 🥔']

x_bebidas = []
x_con = []
x_extras = []
x_tostadas = []

seleccionados = []

try:

    for persona in gente():

        col1, col2, col3, col4, col5 = st.columns(5)

        seleccion = col1.checkbox(persona)

        if seleccion:
            seleccionados.append(persona)

            if persona == 'Álvaro Delgado*':
                bebida_seleccionada = col2.selectbox(f"Bebida de {persona}", bebidas, index=bebidas.index('Café ☕'))
                con_seleccionada = col3.selectbox(f"'Con' de {persona}", con, index=con.index('Solo'))
                extras = col4.text_input(f"Extras de {persona}", 'Largo Doble') 
                barrita = col5.selectbox(f"Tostada de {persona}", tostadas)

            elif persona == 'Adrián*':
                bebida_seleccionada = col2.selectbox(f"Bebida de {persona}", bebidas, index=bebidas.index('Té Rojo 🔴'))
                con_seleccionada = col3.selectbox(f"'Con' de {persona}", con, index=con.index('Sin Lactosa'))
                extras = col4.text_input(f"Extras de {persona}")
                barrita = col5.selectbox(f"Tostada de {persona}", tostadas, index=tostadas.index('Cereales 🌾'))

            elif persona == 'Ana Murillo' or persona == 'Dasha' or persona == 'Inés MG' or persona == 'Inés ML*' or persona == 'María':
                bebida_seleccionada = col2.selectbox(f"Bebida de {persona}", bebidas, index=bebidas.index('Café ☕'))
                con_seleccionada = col3.selectbox(f"'Con' de {persona}", con, index=con.index('Leche 🥛'))
                extras = col4.text_input(f"Extras de {persona}", 'Desnatada') 
                barrita = col5.selectbox(f"Tostada de {persona}", tostadas)

            elif persona == 'Ana García*':
                bebida_seleccionada = col2.selectbox(f"Bebida de {persona}", bebidas, index=bebidas.index('Café ☕'))
                con_seleccionada = col3.selectbox(f"'Con' de {persona}", con, index=con.index('Sin Lactosa'))
                extras = col4.text_input(f"Extras de {persona}") 
                barrita = col5.selectbox(f"Tostada de {persona}", tostadas)

            elif persona == 'Carlos' or persona == 'Rafa':
                bebida_seleccionada = col2.selectbox(f"Bebida de {persona}", bebidas, index=bebidas.index('Café ☕'))
                con_seleccionada = col3.selectbox(f"'Con' de {persona}", con, index=con.index('Solo'))
                extras = col4.text_input(f"Extras de {persona}", 'Largo') 
                barrita = col5.selectbox(f"Tostada de {persona}", tostadas)

            elif persona == 'Dani S.':
                bebida_seleccionada = col2.selectbox(f"Bebida de {persona}", bebidas, index=bebidas.index('Manzanilla 🍵'))
                con_seleccionada = col3.selectbox(f"'Con' de {persona}", con, index=con.index(''))
                extras = col4.text_input(f"Extras de {persona}") 
                barrita = col5.selectbox(f"Tostada de {persona}", tostadas)

            elif persona == 'Mercedes':
                bebida_seleccionada = col2.selectbox(f"Bebida de {persona}", bebidas, index=bebidas.index('Cola Cao 🥜'))
                con_seleccionada = col3.selectbox(f"'Con' de {persona}", con, index=con.index(''))
                extras = col4.text_input(f"Extras de {persona}") 
                barrita = col5.selectbox(f"Tostada de {persona}", tostadas)
             
            elif persona == 'Javi Nieto*':
                bebida_seleccionada = col2.selectbox(f"Bebida de {persona}", bebidas, index=bebidas.index('Zumo 🍊'))
                con_seleccionada = col3.selectbox(f"'Con' de {persona}", con, index=con.index(''))
                extras = col4.text_input(f"Extras de {persona}") 
                barrita = col5.selectbox(f"Tostada de {persona}", tostadas)

            elif persona == 'Lucía':
                bebida_seleccionada = col2.selectbox(f"Bebida de {persona}", bebidas, index=bebidas.index('Descafeinado ☕'))
                con_seleccionada = col3.selectbox(f"'Con' de {persona}", con, index=con.index('Leche 🥛'))
                extras = col4.text_input(f"Extras de {persona}") 
                barrita = col5.selectbox(f"Tostada de {persona}", tostadas)
                
            elif persona == 'Sergio*':
                bebida_seleccionada = col2.selectbox(f"Bebida de {persona}", bebidas)
                con_seleccionada = col3.selectbox(f"'Con' de {persona}", con)
                extras = col4.text_input(f"Extras de {persona}")
                barrita = col5.selectbox(f"Tostada de {persona}", tostadas, index=tostadas.index('Cereales 🌾'))

            else:
                bebida_seleccionada = col2.selectbox(f"Bebida de {persona}", bebidas)
                con_seleccionada = col3.selectbox(f"'Con' de {persona}", con)
                extras = col4.text_input(f"Extras de {persona}")
                barrita = col5.selectbox(f"Tostada de {persona}", tostadas)

            x_bebidas.append(bebida_seleccionada)
            x_con.append(con_seleccionada)
            x_extras.append(extras)
            x_tostadas.append(barrita)

    st.write('')
    st.write('')
    para_llevar = st.radio('¿PARA LLEVAR?', ["Sí, el trabajo nos reclama 💻", "No, necesitamos un descanso 🤯"], index=1)

    # st.write(x_bebidas, x_con, x_extras)

    coffees = []
    for i,e in enumerate(x_bebidas):
        if x_con[i] != 'Cortado' and x_con[i] != 'Solo' and x_con[i] != '' and x_extras[i] != '':
            coffees.append(f'{e} con {x_con[i]} {x_extras[i]}')

        elif x_con[i] != 'Cortado' and x_con[i] != 'Solo' and x_con[i] != '':
            coffees.append(f'{e} con {x_con[i]} {x_extras[i]}')

        elif e == 'Otro':
            coffees.append(f'{x_extras[i]}')

        else:
            coffees.append(f'{e} {x_con[i]} {x_extras[i]}')
            

    # st.write(sorted(coffees))

    # st.write(seleccionados)

    if len(seleccionados) > 0:

        st.write('')
        st.write('')
        st.markdown('##### Comanda Versión Emoji')
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
        st.markdown('##### Comanda Versión Esquema')

        ccl = 0
        ccl_sinlact = 0
        ccl_desnat = 0

        dcl = 0
        dcl_sinlact = 0
        dcl_desnat = 0

        solo = 0
        lardob = 0
        largo = 0
        doble = 0

        te = 0
        rojo = 0
        verde = 0
        negro = 0

        tcl = 0
        tsl = 0

        colacao = 0

        zumo = 0
        
        manzanilla = 0

        otros = 0

        que = {}

        for k, v in conteo.items():

            if "Café" in k and ("Leche" in k or "Sin Lactosa" in k):
                ccl += v
                if "Sin Lactosa" in k:
                    ccl_sinlact += v
                elif "Desnatada" in k:
                    ccl_desnat += v

            elif "Descafeinado" in k:
                dcl += v
                if "Sin Lactosa" in k:
                    dcl_sinlact += v
                elif "Desnatada" in k:
                    dcl_desnat += v

            elif ("Café" in k or "Descafeinado" in k) and ("Solo" in k):
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
                    rojo += v
                if "Verde" in k:
                    verde += v
                if "Negro" in k:
                    negro += v 
                if "Sin Lactosa" in k:
                    tsl += v
                if "Leche" in k:
                    tcl += v

            elif "Cola Cao" in k:
                colacao += v

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

        if ccl > 0:

            if ccl_sinlact > 0 or ccl_desnat > 0:
                output.append(f'• {ccl} café con leche, de los cuales:')
                if ccl_sinlact > 0:
                    output.append(f'   - {ccl_sinlact} sin lactosa')
                if ccl_desnat > 0:
                    output.append(f'   - {ccl_desnat} desnatada')

            else:
                output.append(f'• {ccl} café con leche')

        if dcl > 0:

            if dcl_sinlact > 0 or dcl_desnat > 0:
                output.append(f'• {dcl} descafeinado con leche, de los cuales:')
                if dcl_sinlact > 0:
                    output.append(f'   - {dcl_sinlact} sin lactosa')
                if ccl_desnat > 0:
                    output.append(f'   - {dcl_desnat} desnatada')

            else:
                output.append(f'• {dcl} descafeinado con leche')

        if solo > 0:
            if lardob > 0 or largo > 0 or doble > 0:
                output.append(f'• {solo} café solo, de los cuales:')

                if lardob > 0:
                    output.append(f'   - {lardob} largo doble')
                if largo > 0:
                    output.append(f'   - {largo} largo')
                if doble > 0:
                    output.append(f'   - {doble} doble')

            else:
                output.append(f'• {solo} café solo')


        if te > 0:
            if te > 1:
                if rojo > 0 or verde > 0 or negro > 0:
                    output.append(f'• {te} té, de los cuales:')

                    if rojo > 0:
                        if tsl > 0:
                            output.append(f'   - {tsl} té rojo con leche sin lactosa')
                        elif tcl > 0:
                            output.append(f'   - {tcl} té rojo con leche')
                        else:
                            output.append(f'   - {rojo} té rojo')

                    if verde > 0:
                        output.append(f'   - {verde} té verde')
                    if negro > 0:
                        output.append(f'   - {negro} té negro')
            else:
                if rojo > 0 or verde > 0 or negro > 0:
                    if rojo > 0:
                        if tsl > 0:
                            output.append(f'• {tsl} té rojo con leche sin lactosa')
                        elif tcl > 0:
                            output.append(f'• {tcl} té rojo con leche')
                        else:
                            output.append(f'• {rojo} té rojo')

                    if verde > 0:
                        output.append(f'• {verde} té verde')
                    if negro > 0:
                        output.append(f'• {negro} té negro')


        if colacao > 0:
            output.append(f'• {colacao} cola cao')

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
    
except: 
    pass








