import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ОФІС CBRN",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Заголовок
st.markdown('<h1 style="color:#ffcc00;text-align:center;">Платформа підтримки прийняття рішення щодо реагування на РХБ інциденти</h1>', unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1.2, 4.6, 1.2])

with col_left:
    st.markdown("### МОДУЛЬ 1. РХБ ОБСТАНОВКА")
    st.link_button("1.1. Карта радіаційного моніторингу (SaveEcoBot)", "https://www.saveecobot.com/radiation-maps")
    st.link_button("1.2. Карта прогнозу хімічної обстановки", "http://forecast.inf.ua/")
    st.info("💡 Клік на маркері показує координати.")

with col_center:
    map_html = """
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <div id="map" style="height: 750px; border-radius: 8px;"></div>
    <script>
        var map = L.map('map').setView([48.3794, 31.1656], 6);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        // Стартовий маркер
        var marker = L.marker([48.3794, 31.1656]).addTo(map);
        marker.bindPopup("Стартовий маркер<br>Координати: 48.3794, 31.1656");

        // Копіювання координат при кліку
        marker.on('click', function(e) {
            var coords = e.latlng.lat.toFixed(6) + ", " + e.latlng.lng.toFixed(6);
            navigator.clipboard.writeText(coords);
            marker.bindPopup("Координати скопійовано:<br>" + coords).openPopup();
        });
    </script>
    """
    components.html(map_html, height=760)

with col_right:
    st.markdown("### МОДУЛЬ 3. РОЗРАХУНКИ")
    st.link_button("3.1. Калькулятор дози опромінення", "https://sergsh1125-dotcom.github.io/radiation-calculator/")

st.sidebar.caption("ОФІС CBRN v3.8")
