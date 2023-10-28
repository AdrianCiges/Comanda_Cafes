import streamlit as st
import requests


def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]


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

    ip_address = get_ip()
    request_url = 'https://geolocation-db.com/jsonp/' + ip_address
    response = requests.get(request_url)
    result = response.content.decode()
    result = result.split("(")[1].strip(")")
    result  = json.loads(result)
    st.write(result)
