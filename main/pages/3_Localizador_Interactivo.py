import streamlit.components.v1 as components

def get_location():
    # Tu código HTML/Javascript aquí
    html = """
    <script>
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition);
        } else {
            console.log("Geolocation is not supported by this browser.");
        }
    }
    function showPosition(position) {
        // Enviar posición a Python
    }
    getLocation();
    </script>
    """
    components.html(html, height=100)

get_location()
