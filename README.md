# ☕ Comanda_Cafes
## CONTENIDO 📑
[1 - Objetivo 🎯](#O)<br />
[2 - Código ⚙️](#SRC) <br />
[3 - Web (Streamlit) 🌐](#WEB) <br />
 
## 1 - OBJETIVO 🎯<a name="O"/>   
💥 Crear una interfaz web capaz de geolocalizar al usuario y visualizar las opciones de cafeterías más cercanas a su ubicación.<br />

💥 Facilitar el filtrado de las opciones de cafeterías en función de diferentes variables.<br />
                          
💥 Simplificar y facilitar la comanda grupal de cafés al bajar a la cafetería elegida. <br />

💥 Agilizar el pedido pre-seleccionando la opción más habitual de cada "cafetero". <br />

## 2 - CÓDIGO ⚙️ <a name="SRC"/>

🤖 Scrappeamos la API de Google Maps, extrayendo todas las cafeterías posibles de España y sus características (principalmente municipios de más de 75.000 habitantes)<br />

⛏️ Limpiamos datos, estructuramos la información en días de la semana para filtrar dinámicamente por horario y % de ocupación en nustra interfaz en función del día de consulta<br />

📩 Programamos una opción de envío de correo electrónico para la inclusión de municipios adicionales que el usario desee visualizar en la interfaz<br />

🙋‍♀️ Detallamos las opciones de cada "cafetero" y programamos una opción por defecto (la más habitual: café con leche) con condicionales para las más específicas.<br />

🔠 Usamos python para tratar "strings" y crear 2 opciones de comanda: una en versión emojis y otra en versión esquema.<br />

✂ Programamos una opción de copiado para la comanda y la pegamos-enviamos como mensaje al WhatsApp de la cafetería (previa petición del teléfono y acuerdo para este procedimiento).<br />

⏫ Deployamos el código en Streamlit.app, con las liberías y dependencias necesarias y... ¡a disfrutar!

## 3 - WEB (STREAMLIT) 🌐 <a name="WEB"/>
👉🏼 https://la-ruta-del-cafe.streamlit.app/
