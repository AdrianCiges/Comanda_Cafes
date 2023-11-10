import geocoder
import folium

def obtener_ubicacion_actual():
    # Obtener la ubicación basada en la dirección IP
    g = geocoder.ip('me')
    return g.latlng

def mostrar_mapa(ubicacion):
    # Crear un mapa centrado en la ubicación actual
    mapa = folium.Map(location=ubicacion, zoom_start=15)

    # Agregar un marcador para la ubicación actual
    folium.Marker(ubicacion, popup='Ubicación Actual').add_to(mapa)

    # Mostrar el mapa
    display(mapa)

# Obtener la ubicación actual
ubicacion_actual = obtener_ubicacion_actual()

# Mostrar el mapa con la ubicación actual
if ubicacion_actual:
    mostrar_mapa(ubicacion_actual)
else:
    print("No se pudo obtener la ubicación actual.")
