import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime

# --- 1. НАЛАШТУВАННЯ СТОРІНКИ ---
st.set_page_config(
    page_title="ОФІС CBRN",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ГЛОБАЛЬНІ СТИЛІ (CSS) ---
st.markdown("""
<style>
    /* Базові налаштування */
    #MainMenu, footer, header, .stDeployButton {visibility: hidden; display: none !important;}
    .block-container {padding:1rem !important; max-width:100% !important; padding-top: 1.5rem !important;}
    .stApp {background-color:#0e1117; color:#e0e0e0;}

    /* Заголовки */
    .main-title {
        color:#ffcc00 !important;
        text-align:center !important;
        font-size:25px !important;
        font-weight:bold !important;
        margin-top:-20px !important;
        margin-bottom:15px !important;
        text-transform:uppercase !important;
    }

    .module-header {
        color:#ffcc00 !important;
        border-bottom:1px solid #ffcc00 !important;
        margin-top:10px !important;
        margin-bottom:8px !important;
        font-weight:bold !important;
        font-size:18px !important;
        text-transform:uppercase !important;
    }

    /* СТИЛЬ ДЛЯ КНОПОК ТА ПОСИЛАНЬ */
    div[data-testid="stButton"] button,
    div.stLinkButton > a {
        background-color:#ffcc00 !important;
        color:#000 !important;
        border:none !important;
        width:100% !important;
        font-weight:bold !important;
        font-size:12px !important;
        border-radius:4px !important;
        padding:8px 12px !important;
        display:flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        text-decoration: none !important;
        white-space: pre-wrap !important; /* Дозволяє перенос рядка */
        height: auto !important;
        min-height: 3em !important;
        line-height: 1.2 !important;
    }

    div[data-testid="stButton"] button:hover,
    div.stLinkButton > a:hover {
        background-color: #ffea00 !important;
        border: 1px solid #4CAF50 !important;
    }

    /* Експандери */
    .stExpander {
        background-color: transparent !important;
        border: 1px solid #ffcc00 !important;
        border-radius:4px !important;
    }
    .stExpander summary { color:#ffcc00 !important; font-weight:bold !important; }

    @media print {
        .stColumn:first-child, .stColumn:last-child, button, .main-title, .module-header {
            display: none !important;
        }
        .block-container { padding: 0 !important; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">Платформа підтримки заходів реагування на ХБРЯ інциденти</p>', unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1.3, 4.4, 1.3])

# -------- ЛІВА ПАНЕЛЬ (МОДУЛІ 1 ТА 2) --------
with col_left:
    st.markdown('<p class="module-header">МОДУЛЬ 1. РХБ ОБСТАНОВКА</p>', unsafe_allow_html=True)
    st.link_button("1.1. Карта радіаційного моніторингу (SaveEcoBot)", "https://www.saveecobot.com/radiation-maps")
    st.link_button ("1.2. Карта радіаційного моніторингу Укргідромету", "https://www.meteo.gov.ua/#RADIO")
    st.link_button("1.3. Карта радіаційного моніторингу країн ЄС", "https://remap.jrc.ec.europa.eu/Advanced.aspx")
    st.link_button("1.4. Карта прогнозу хімічної обстановки", "http://forecast.inf.ua/")
    st.link_button("1.5. Карта фактичної радіаційної обстановки", "https://radiation-situation-mt5eyizylhpa7sxaltawpk.streamlit.app/")
    st.link_button("1.6. Карта фактичної хімічної обстановки", "https://chemical-map-dgtnhrsz7azy3epkzid2g2.streamlit.app/")
    st.link_button("1.7. Карта фактичної РХБ обстановки", "https://map-obstanovka-vuvukyx4vwu9jrhuv68vcg.streamlit.app/")
    st.info("💡 На картах 1.5; 1.6; 1.7 координати завантажуються кліком мишки.")

    st.markdown('<p class="module-header">МОДУЛЬ 2. БАЗИ ДАНИХ</p>', unsafe_allow_html=True)
    st.link_button("2.1. Аварійні картки НХР", "https://sergsh1125-dotcom.github.io/emergency-cards/")
    st.link_button("2.2. Токсодози бойових ОР", "https://sergsh1125-dotcom.github.io/toxicdoze/")

# -------- ЦЕНТР (РОБОЧА КАРТА З ІНСТРУМЕНТАМИ) --------
with col_center:
    map_html = """
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.js"></script>
<script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>

<div id="capture_area" style="background:#0e1117; padding:5px; border-radius:8px;">
    <div id="map" style="height:650px; width:100%; border-radius:8px;"></div>
</div>

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 5px; margin-top: 10px;">
    <button onclick="addText()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer; font-size:11px;">ВСТАВИТИ ТЕКСТ</button>
    <button onclick="clearMap()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer; font-size:11px;">ОЧИСТИТИ КАРТУ</button>
    <button onclick="downloadPNG()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer; font-size:11px;">ЕКСПОРТ PNG</button>
    <button onclick="window.print()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer; font-size:11px;">ДРУК / PDF</button>
</div>

<script>
var map = L.map('map',{attributionControl:false}).setView([48.3794,31.1656],6);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{crossOrigin: 'anonymous'}).addTo(map);

var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

var radIcon = L.divIcon({
    html: '<div style="background:#ffcc00; border:2px solid black; border-radius:50%; width:24px; height:24px; display:flex; align-items:center; justify-content:center; font-size:16px;">☢️</div>',
    className: '', iconSize: [24, 24], iconAnchor: [12, 12]
});

var drawControl = new L.Control.Draw({
    draw:{ 
        polygon: { shapeOptions: { color: 'black', fillColor: 'yellow', fillOpacity: 0.5 } },
        circlemarker: { color: 'black', fillColor: 'yellow', fillOpacity: 0.9, radius: 8 },
        marker: { icon: radIcon },
        polyline: { shapeOptions: { color: 'black', weight: 3 } },
        rectangle: true, circle: true
    },
    edit:{ featureGroup: drawnItems }
});
map.addControl(drawControl);

map.on(L.Draw.Event.CREATED, function(e){
    var layer = e.layer;
    drawnItems.addLayer(layer);
});

function addText(){
    var text = prompt("Введіть текст:");
    if(text){
        map.once('click', function(e){
            var icon = L.divIcon({
                html:'<div style="background:white; padding:2px 5px; border:1px solid black; border-radius:3px; font-weight:bold; color:black; white-space:nowrap;">'+text+'</div>',
                iconSize: null
            });
            L.marker(e.latlng,{icon:icon}).addTo(drawnItems);
        });
    }
}

function clearMap() { if(confirm("Очистити карту?")) drawnItems.clearLayers(); }

function downloadPNG(){
    html2canvas(document.getElementById("capture_area"), {useCORS:true, scale:2}).then(canvas => {
        var link = document.createElement("a");
        link.download = "CBRN_Map.png";
        link.href = canvas.toDataURL();
        link.click();
    });
}
</script>
"""
    components.html(map_html, height=750)

# -------- ПРАВА ПАНЕЛЬ (МОДУЛІ 3 ТА 4 + WINDY) --------
with col_right:
    # МОНІТОРИНГ ВІТРУ (WINDY)
    with st.expander("🌤️ МОНІТОРИНГ ВІТРУ", expanded=False):
        windy_html = """
        <iframe 
            width="100%" height="300" 
            src="https://embed.windy.com/embed2.html?lat=49.0&lon=31.0&zoom=5&level=surface&overlay=wind&product=ecmwf&metricWind=m%2Fs&metricTemp=%C2%B0C" 
            frameborder="0">
        </iframe>
        """
        components.html(windy_html, height=310)
        st.caption("Дані в реальному часі: Windy.com")

    st.markdown('<p class="module-header">МОДУЛЬ 3. РОЗРАХУНКИ</p>', unsafe_allow_html=True)
    st.link_button("3.1. Калькулятор дози (Ядерний вибух)", "https://sergsh1125-dotcom.github.io/radiation-calculator/")
    st.link_button("3.2. Калькулятор дози (Аварія на АЕС)", "https://sergsh1125-dotcom.github.io/radiation-doza/")
    st.link_button("3.3. Розрахунок часу перебування", "https://sergsh1125-dotcom.github.io/calculator-time/")

    st.markdown('<p class="module-header">МОДУЛЬ 4. ДОВІДКОВА ІНФОРМАЦІЯ </p>', unsafe_allow_html=True)
    st.link_button("4.1. Укргідрометеоцентр", "https://www.meteo.gov.ua/")
    with st.expander("4.2. Нормативно-правова база РХЗ":
         st.link_button(
            "Управління РХБ захисту ДСНС", 
            "https://dsns.gov.ua/zakonodavstvo/perelik-normativno-pravovix-dokumentiv-shho-reglamentuyut-diyalnist-pidrozdiliv-dsns-ukrayini/upravlinnia-organizaciyi-radiaciinogo-ximicnogo-ta-biologicnogo-zaxistu"
        )
        st.link_button(
            "СОП 1.1/РХБЗ: Демеркуризація\nСОП 1.2: Дії підрозділів при НС з НХР", 
            "https://kyiv.dsns.gov.ua/navchalniy-centr-gu/sluzhbova-pidgotovka/normativno-pravovi-akti"
        )
