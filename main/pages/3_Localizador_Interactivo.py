import streamlit as st
import requests
import json


def get_ip_address():
    try:
        # Utilizando un servicio externo para obtener la dirección IP del usuario
        ip_address = requests.get('https://api64.ipify.org?format=json').json()['ip']
        return ip_address
    except:
        return "No se pudo obtener la dirección IP"


# def get_location():
#     ip_address = get_ip()
#     response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
#     location_data = {
#         "ip": ip_address,
#         "city": response.get("city"),
#         "region": response.get("region"),
#         "country": response.get("country_name")
#     }
#     return location_data


if st.button('Mi ubicación'):
    # st.write(get_location())

    ip_address = get_ip_address()
    request_url = 'https://geolocation-db.com/jsonp/' + ip_address
    response = requests.get(request_url)
    result = response.content.decode()
    result = result.split("(")[1].strip(")")
    result  = json.loads(result)
    st.write(result)
