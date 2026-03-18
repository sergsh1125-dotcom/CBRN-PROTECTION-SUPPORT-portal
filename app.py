import streamlit as st
import streamlit.components.v1 as components

# --- 1. Налаштування сторінки ---
st.set_page_config(
    page_title="ОФІС CBRN",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. Заголовок ---
st.markdown('<h1 style="color:#ffcc00;text-align:center;">Платформа підтримки прийняття рішення щодо реагування на РХБ інциденти</h1>', unsafe_allow_html=True)

# --- 3. Колонки ---
col_left, col_center, col_right = st.columns([1.2, 4.6, 1.2])

# --- ЛІВА КОЛОНКА ---
with col_left:
    st.markdown('<p style="color:#ffcc00;font-weight:bold;">МОДУЛЬ 1. РХБ ОБСТАНОВКА</p>', unsafe_allow_html=True)
    st.link_button("1.1. Карта радіаційного моніторингу (SaveEcoBot)", "https://www.saveecobot.com/radiation-maps")
    st.link_button("1.2. Карта радіаційного моніторингу країн ЄС", "https://remap.jrc.ec.europa.eu/Advanced.aspx")
    st.link_button("1.3. Карта прогнозу хімічної обстановки", "http://forecast.inf.ua/")
    st.link_button("1.4. Карта фактичної радіаційної обстановки", "https://radiation-situation-mt5eyizylhpa7sxaltawpk.streamlit.app/")
    st.link_button("1.5. Карта фактичної хімічної обстановки", "https://chemical-map-6refroql3kghrhuh7tzdma.streamlit.app/")
    st.info("💡 Клік на маркері показує координати.")

    st.markdown('<p style="color:#ffcc00;font-weight:bold;">МОДУЛЬ 2. БАЗИ ДАНИХ</p>', unsafe_allow_html=True)
    st.link_button("2.1. Аварійні картки НХР", "https://sergsh1125-dotcom.github.io/emergency-cards/")
    st.link_button("2.2. Токсодози бойових ОР", "https://sergsh1125-dotcom.github.io/toxicdoze/")

# --- ЦЕНТРАЛЬНА КОЛОНКА (КАРТА) ---
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

# --- ПРАВА КОЛОНКА ---
with col_right:
    st.markdown('<p style="color:#ffcc00;font-weight:bold;">МОДУЛЬ 3. РОЗРАХУНКИ</p>', unsafe_allow_html=True)
    st.link_button("3.1. Калькулятор дози опромінення при ядерному вибуху", "https://sergsh1125-dotcom.github.io/radiation-calculator/")
    st.link_button("3.2. Калькулятор дози опромінення при аварії на АЕС", "https://sergsh1125-dotcom.github.io/radiation-doza/")
    st.link_button("3.3. Калькулятор часу перебування у зоні радіоактивного забруднення", "https://sergsh1125-dotcom.github.io/calculator-time/")

    st.markdown('<p style="color:#ffcc00;font-weight:bold;">МОДУЛЬ 4. ДОВІДКОВА ІНФОРМАЦІЯ</p>', unsafe_allow_html=True)
    st.link_button("4.1. Метеообстановка", "https://www.meteo.gov.ua/")

    with st.expander("📄 4.2. Методичні матеріали"):
        st.link_button("📜 Управління РХБ захисту ДСНС", "https://dsns.gov.ua/zakonodavstvo/perelik-normativno-pravovix-dokumentiv-shho-reglamentuyut-diyalnist-pidrozdiliv-dsns-ukrayini/upravlinnia-organizaciyi-radiaciinogo-ximicnogo-ta-biologicnogo-zaxistu")
        st.link_button("📚 Методичні рекомендації", "https://dsns.gov.ua/metodichni-rekomendaciyi")

# --- ПІДСВІТКА ---
st.sidebar.caption("ОФІС CBRN v3.8")
