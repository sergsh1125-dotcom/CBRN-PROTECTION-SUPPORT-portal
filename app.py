import streamlit as st
import streamlit.components.v1 as components

# --- 1. НАЛАШТУВАННЯ СТОРІНКИ ---
st.set_page_config(
    page_title="ОФІС CBRN",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. СТИЛІЗАЦІЯ ---
st.markdown("""
<style>
.block-container {
    padding: 1rem !important;
    max-width: 100% !important;
}
#MainMenu, footer, header {visibility: hidden;}
.stApp {background-color: #0e1117; color: #e0e0e0;}
/* Назва порталу */
.main-title {
    color: #ffcc00 !important; 
    text-align: center !important; 
    font-size: 25px !important;  /* +1 від назви модулів */
    font-weight: bold !important; 
    margin-top: -30px !important; 
    margin-bottom: 15px !important;
    text-transform: uppercase !important;
}
/* Назви модулів */
.module-header {
    color: #ffcc00 !important; 
    border-bottom: 1px solid #ffcc00 !important; 
    margin-top: 10px !important; 
    margin-bottom: 8px !important; 
    font-weight: bold !important; 
    font-size: 14px !important;
    text-transform: uppercase !important;
}
/* Кнопки */
div[data-testid="stButton"] button, div[data-testid="stLinkButton"] a {
    background-color: #ffcc00 !important;
    color: #000 !important;
    border: none !important;
    width: 100% !important;
    font-weight: bold !important;
    font-size: 12px !important;
    border-radius: 4px !important;
    padding: 8px 12px !important;
    display: block !important;
    text-decoration: none !important;
    line-height: 1.2 !important;
}
div[data-testid="stButton"] button:hover, div[data-testid="stLinkButton"] a:hover {
    background-color: #e6b800 !important;
}
/* Експандер */
.stExpander {
    background-color: #ffcc00 !important;
    border: none !important;
    border-radius: 4px !important;
}
.stExpander summary {
    color: #000 !important;
    font-weight: bold !important;
}
.stExpander summary svg { fill: #000 !important; }
/* iframe */
iframe { border: 1px solid #3d444d !important; border-radius: 8px !important;}
</style>
""", unsafe_allow_html=True)

# --- 3. Заголовок ---
st.markdown('<p class="main-title">Платформа підтримки прийняття рішення щодо реагування на РХБ інциденти</p>', unsafe_allow_html=True)

# --- 4. Колонки ---
col_left, col_center, col_right = st.columns([1.2, 4.6, 1.2])

with col_left:
    st.markdown('<p class="module-header">МОДУЛЬ 1. РХБ ОБСТАНОВКА</p>', unsafe_allow_html=True)
    st.link_button("1.1. Карта радіаційного моніторингу (SaveEcoBot)", "https://www.saveecobot.com/radiation-maps")
    st.link_button("1.2. Карта радіаційного моніторингу країн ЄС", "https://remap.jrc.ec.europa.eu/Advanced.aspx")
    st.link_button("1.3. Карта прогнозу хімічної обстановки", "http://forecast.inf.ua/")
    st.link_button("1.4. Карта фактичної радіаційної обстановки", "https://radiation-situation-mt5eyizylhpa7sxaltawpk.streamlit.app/")
    st.link_button("1.5. Карта фактичної хімічної обстановки", "https://chemical-map-6refroql3kghrhuh7tzdma.streamlit.app/")
    st.info("💡 На картах підмодулів 1.4; 1.5. Координати точки вимірювання завантажуються кліком мишки.")

    st.markdown('<p class="module-header">МОДУЛЬ 2. БАЗИ ДАНИХ</p>', unsafe_allow_html=True)
    st.link_button("2.1. Аварійні картки НХР", "https://sergsh1125-dotcom.github.io/emergency-cards/")
    st.link_button("2.2. Токсодози бойових ОР", "https://sergsh1125-dotcom.github.io/toxicdoze/")

with col_center:
    map_html = """
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.js"></script>

<div id="map" style="height: 750px; width: 100%; border-radius: 8px;"></div>

<script>
var map = L.map('map').setView([48.3794, 31.1656], 6);

// Базова карта
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: '© OpenStreetMap contributors'}).addTo(map);

// Шар для об'єктів
var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

// Стиль фігур
function setStyle(layer) {
    layer.setStyle({color:'black', fillColor:'yellow', fillOpacity:0.4, weight:2});
}

// Інструменти малювання
var drawControl = new L.Control.Draw({
    draw: {polygon:true, rectangle:true, circle:true, polyline:true, marker:true},
    edit: {featureGroup: drawnItems}
});
map.addControl(drawControl);

// Обробка створення
map.on(L.Draw.Event.CREATED, function (e) {
    var layer = e.layer;
    var type = e.layerType;

    if(type==='marker'){
        var blueIcon = L.icon({
            iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png",
            shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
            iconSize:[25,41], iconAnchor:[12,41]
        });
        layer.setIcon(blueIcon);
        layer.on('click', function() {
            var coords = layer.getLatLng().lat.toFixed(6) + ", " + layer.getLatLng().lng.toFixed(6);
            layer.bindPopup("Координати:<br>" + coords).openPopup();
        });
    } else {
        if(layer instanceof L.Circle && layer.options.radius>=50000){ // велике коло
            layer.setStyle({color:'black', fillColor:'yellow', fillOpacity:0.4, weight:2});
        } else if(layer instanceof L.Circle){ // мале коло
            layer.setStyle({color:'black', fillColor:'orange', fillOpacity:0.8, weight:2});
        } else { setStyle(layer);}
    }

    drawnItems.addLayer(layer);
});

// Кнопки для карти
function addText() {
    var textMarker = L.marker(map.getCenter(), {
        icon: L.divIcon({className: 'text-label', html: 'Текст на карті', iconSize:[100,20]})
    }).addTo(drawnItems);
}

function saveMap(){
    html2canvas(document.getElementById('map')).then(function(canvas){
        var link = document.createElement('a');
        link.download = 'map_snapshot.png';
        link.href = canvas.toDataURL();
        link.click();
    });
}
</script>

<button onclick="addText()">Додати текст на карту</button>
<button onclick="saveMap()">Завантажити карту у PNG</button>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
"""
    components.html(map_html, height=760)

with col_right:
    st.markdown('<p class="module-header">МОДУЛЬ 3. РОЗРАХУНКИ</p>', unsafe_allow_html=True)
    st.link_button("3.1. Калькулятор дози опромінення при ядерному вибуху","https://sergsh1125-dotcom.github.io/radiation-calculator/")
    st.link_button("3.2. Калькулятор дози опромінення при аварії на АЕС","https://sergsh1125-dotcom.github.io/radiation-doza/")
    st.link_button("3.3. Калькулятор розрахунку часу перебування у зоні радіоактивного забруднення","https://sergsh1125-dotcom.github.io/calculator-time/")

    st.markdown('<p class="module-header">МОДУЛЬ 4. ДОВІДКОВА ІНФОРМАЦІЯ</p>', unsafe_allow_html=True)
    st.link_button("4.1. Метеообстановка","https://www.meteo.gov.ua/")
    with st.expander("📄 4.2. Методичні матеріали"):
        st.link_button("📜 Управління РХБ захисту ДСНС","https://dsns.gov.ua/zakonodavstvo/perelik-normativno-pravovix-dokumentiv-shho-reglamentuyut-diyalnist-pidrozdiliv-dsns-ukrayini/upravlinnia-organizaciyi-radiaciinogo-ximicnogo-ta-biologicnogo-zaxistu")
        st.link_button("📚 Методичні рекомендації","https://dsns.gov.ua/metodichni-rekomendaciyi")

st.sidebar.caption("ОФІС CBRN v3.9")
