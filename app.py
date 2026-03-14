import streamlit as st
import streamlit.components.v1 as components

# --- 1. НАЛАШТУВАННЯ СТОРІНКИ ---
st.set_page_config(
    page_title="ОФІС CBRN",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. СТИЛІЗАЦІЯ (МАКСИМАЛЬНИЙ ЖОВТИЙ ФОН) ---
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0e1117; color: #e0e0e0;}
    
    /* НАЗВА ПОРТАЛУ */
    .main-title {
        color: #ffcc00 !important; 
        text-align: center !important; 
        font-size: 23px !important; 
        font-weight: bold !important; 
        margin-top: -30px !important; 
        margin-bottom: 15px !important;
        text-transform: uppercase !important;
    }
    
    /* НАЗВИ МОДУЛІВ */
    .module-header {
        color: #ffcc00 !important; 
        border-bottom: 1px solid #ffcc00 !important; 
        margin-top: 10px !important; 
        margin-bottom: 8px !important; 
        font-weight: bold !important; 
        font-size: 14px !important; 
        text-transform: uppercase !important;
    }

    /* ФАРБУВАННЯ ВСІХ КНОПОК ТА ПІДМОДУЛІВ */
    /* Цей блок знаходить стандартні контейнери Streamlit і робить їх жовтими */
    div[data-testid="stButton"] button, 
    div[data-testid="stLinkButton"] a,
    .stDownloadButton button {
        background-color: #ffcc00 !important;
        color: #000000 !important;
        border: none !important;
        width: 100% !important;
        font-weight: bold !important;
        font-size: 12px !important;
        border-radius: 4px !important;
        padding: 8px 12px !important;
        display: block !important;
        text-decoration: none !important;
    }

    /* СТИЛІЗАЦІЯ ЕКСПАНДЕРА (ПОЛЕ 4.2) */
    .stExpander {
        background-color: #ffcc00 !important;
        border: none !important;
        border-radius: 4px !important;
    }
    
    .stExpander summary {
        color: #000000 !important;
        font-weight: bold !important;
    }

    .stExpander summary svg {
        fill: #000000 !important;
    }

    /* Колір при наведенні */
    div[data-testid="stButton"] button:hover, 
    div[data-testid="stLinkButton"] a:hover {
        background-color: #e6b800 !important;
        color: #000000 !important;
    }

    iframe {
        border: 1px solid #3d444d !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. ЗАГОЛОВОК ---
st.markdown('<p class="main-title">Платформа підтримки прийняття рішення щодо реагування на РХБ інциденти</p>', unsafe_allow_html=True)

# --- 4. РОБОЧИЙ ПРОСТІР ---
col_left, col_center, col_right = st.columns([1.2, 4.6, 1.2])

with col_left:
    st.markdown('<p class="module-header">МОДУЛЬ 1. РХБ ОБСТАНОВКА</p>', unsafe_allow_html=True)
    st.link_button("1.1. Карта радіаційного моніторингу (SaveEcoBot)", "https://www.saveecobot.com/radiation-maps")
    st.link_button("1.2. Карта радіаційного моніторингу країн ЄС", "https://remap.jrc.ec.europa.eu/Advanced.aspx")
    st.link_button("1.3. Карта прогнозу хімічної обстановки", "http://forecast.inf.ua/")
    st.link_button("1.4. Карта фактичної радіаційної обстановки", "https://sergsh1125-dotcom-radiation-situation-app-vlg9fu.streamlit.app/")
    st.link_button("1.5. Карта фактичної хімічної обстановки", "https://sergsh1125-dotcom-chemical-map-app-rhopcd.streamlit.app/")
    
    st.info("💡 Клікніть на карті, щоб скопіювати координати.")
    
    st.markdown('<p class="module-header">МОДУЛЬ 2. БАЗИ ДАНИХ</p>', unsafe_allow_html=True)
    st.link_button("2.1. Аварійні картки НХР", "https://sergsh1125-dotcom.github.io/emergency-cards/")
    st.link_button("2.2. Токсодози бойових ОР", "https://sergsh1125-dotcom.github.io/toxicdoze/")

with col_center:
    map_html = """
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <div id="map" style="height: 750px; border-radius: 8px;"></div>
    <script>
        var map = L.map('map').setView([48.3794, 31.1656], 6);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);
        var popup = L.popup();
        function onMapClick(e) {
            var coords = e.latlng.lat.toFixed(6) + ", " + e.latlng.lng.toFixed(6);
            navigator.clipboard.writeText(coords).then(function() {
                popup.setLatLng(e.latlng).setContent("Координати скопійовано: <br>" + coords).openOn(map);
            });
        }
        map.on('click', onMapClick);
    </script>
    """
    components.html(map_html, height=760)

with col_right:
    st.markdown('<p class="module-header">МОДУЛЬ 3. РОЗРАХУНКИ</p>', unsafe_allow_html=True)
    st.link_button("3.1. Калькулятор дози опромінення при ядерному вибуху", "https://sergsh1125-dotcom.github.io/radiation-calculator/")
    st.link_button("3.2. Калькулятор розрахунку часу перебування у зоні радіоактивного забруднення", "https://sergsh1125-dotcom.github.io/calculator-time/")
    
    st.markdown('<p class="module-header">МОДУЛЬ 4. ДОВІДКОВА ІНФОРМАЦІЯ</p>', unsafe_allow_html=True)
    st.link_button("4.1. Метеообстановка", "https://www.meteo.gov.ua/")
    
    with st.expander("📄 4.2. Методичні матеріали"):
        st.link_button("📜 Управління РХБ захисту ДСНС", "https://dsns.gov.ua/zakonodavstvo/perelik-normativno-pravovix-dokumentiv-shho-reglamentuyut-diyalnist-pidrozdiliv-dsns-ukrayini/upravlinnia-organizaciyi-radiaciinogo-ximicnogo-ta-biologicnogo-zaxistu")
        st.link_button("📚 Методичні рекомендації", "https://dsns.gov.ua/metodichni-rekomendaciyi")

st.sidebar.caption("ОФІС CBRN v3.7")
