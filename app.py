import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ОФІС CBRN",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.block-container {padding:1rem !important; max-width:100% !important;}
#MainMenu, footer, header {visibility:hidden;}
.stApp {background-color:#0e1117; color:#e0e0e0;}

.main-title {
    color:#ffcc00 !important;
    text-align:center !important;
    font-size:25px !important;
    font-weight:bold !important;
    margin-top:-30px !important;
    margin-bottom:15px !important;
    text-transform:uppercase !important;
}

.module-header {
    color:#ffcc00 !important;
    border-bottom:1px solid #ffcc00 !important;
    margin-top:10px !important;
    margin-bottom:8px !important;
    font-weight:bold !important;
    font-size:22px !important;
    text-transform:uppercase !important;
}

/* КНОПКИ */
div[data-testid="stButton"] button,
div[data-testid="stLinkButton"] a {
    background-color:#ffcc00 !important;
    color:#000 !important;
    border:none !important;
    width:100% !important;
    font-weight:bold !important;
    font-size:12px !important;
    border-radius:4px !important;
    padding:8px 12px !important;
    display:block !important;
}

/* EXPANDER ЖОВТИЙ */
.stExpander {
    background-color:#ffcc00 !important;
    border:none !important;
    border-radius:4px !important;
}
.stExpander summary {
    color:#000 !important;
    font-weight:bold !important;
}
.stExpander summary svg {
    fill:#000 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">Платформа підтримки прийняття рішення щодо реагування на РХБ інциденти</p>', unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1.2,4.6,1.2])

# -------- LEFT --------
with col_left:
    st.markdown('<p class="module-header">МОДУЛЬ 1. РХБ ОБСТАНОВКА</p>', unsafe_allow_html=True)

    st.link_button("1.1. Карта радіаційного моніторингу (SaveEcoBot)", "https://www.saveecobot.com/radiation-maps")
    st.link_button("1.2. Карта радіаційного моніторингу країн ЄС", "https://remap.jrc.ec.europa.eu/Advanced.aspx")
    st.link_button("1.3. Карта прогнозу хімічної обстановки", "http://forecast.inf.ua/")
    st.link_button("1.4. Карта фактичної радіаційної обстановки", "https://radiation-situation-mt5eyizylhpa7sxaltawpk.streamlit.app/")
    st.link_button("1.5. Карта фактичної хімічної обстановки", "https://chemical-map-6refroql3kghrhuh7tzdma.streamlit.app/")

    st.info("💡 На картах підмодулів 1.4; 1.5 координати точки вимірювання завантажуються кліком мишки.")

    st.markdown('<p class="module-header">МОДУЛЬ 2. БАЗИ ДАНИХ</p>', unsafe_allow_html=True)
    st.link_button("2.1. Аварійні картки НХР", "https://sergsh1125-dotcom.github.io/emergency-cards/")
    st.link_button("2.2. Токсодози бойових ОР", "https://sergsh1125-dotcom.github.io/toxicdoze/")

# -------- CENTER --------
with col_center:

    map_html = """
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css"/>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.js"></script>
<script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>

<div id="map" style="height:750px; width:100%; border-radius:8px;"></div>

<br>

<button onclick="addText()" style="width:100%;padding:10px;margin-bottom:5px;background:#ffcc00;font-weight:bold;">
ВСТАВИТИ ТЕКСТ
</button>

<button onclick="downloadPNG()" style="width:100%;padding:10px;background:#ffcc00;font-weight:bold;">
ЗАВАНТАЖИТИ КАРТУ PNG
</button>

<script>

var map = L.map('map',{attributionControl:false}).setView([48.3794,31.1656],6);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
    crossOrigin:true
}).addTo(map);

var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

// --- СТИЛЬ ---
function setStyle(layer){
    if(layer instanceof L.Circle){
        var r = layer.getRadius();
        layer.setStyle({
            color:'black',
            fillColor: r>5000 ? 'yellow' : 'orange',
            fillOpacity:0.6,
            weight:2
        });
    } else {
        layer.setStyle({
            color:'black',
            fillColor:'yellow',
            fillOpacity:0.6,
            weight:2
        });
    }
}

// --- DRAW ---
var drawControl = new L.Control.Draw({
    draw:{
        polygon:true,
        rectangle:true,
        circle:true,
        polyline:true,
        marker:true
    },
    edit:{featureGroup: drawnItems}
});

map.addControl(drawControl);

// --- СТВОРЕННЯ ---
map.on(L.Draw.Event.CREATED, function(e){

    var layer = e.layer;

    if(e.layerType === "marker"){

        var blueIcon = L.icon({
            iconUrl:"https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png",
            shadowUrl:"https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
            iconSize:[25,41],
            iconAnchor:[12,41]
        });

        layer.setIcon(blueIcon);

        layer.on('click', function(){
            var c = layer.getLatLng();
            layer.bindPopup("Координати:<br>"+c.lat.toFixed(6)+", "+c.lng.toFixed(6)).openPopup();
        });

    } else {
        setStyle(layer);
    }

    drawnItems.addLayer(layer);
});

// --- ТЕКСТ ---
function addText(){
    var text = prompt("Введіть текст:");
    if(text){
        map.once('click', function(e){
            var icon = L.divIcon({
                html:'<div style="background:white;padding:4px;border-radius:4px;">'+text+'</div>'
            });
            L.marker(e.latlng,{icon:icon}).addTo(map);
        });
    }
}

// --- PNG ---
function downloadPNG(){
    html2canvas(document.getElementById("map")).then(function(canvas){
        var link = document.createElement("a");
        link.download = "map.png";
        link.href = canvas.toDataURL();
        link.click();
    });
}

</script>
"""
    components.html(map_html, height=820)

# -------- RIGHT --------
with col_right:
    st.markdown('<p class="module-header">МОДУЛЬ 3. РОЗРАХУНКИ</p>', unsafe_allow_html=True)
    st.link_button("3.1. Калькулятор дози опромінення при ядерному вибуху", "https://sergsh1125-dotcom.github.io/radiation-calculator/")
    st.link_button("3.2. Калькулятор дози опромінення при аварії на АЕС", "https://sergsh1125-dotcom.github.io/radiation-doza/")
    st.link_button("3.3. Калькулятор розрахунку часу перебування у зоні радіоактивного забруднення", "https://sergsh1125-dotcom.github.io/calculator-time/")

    st.markdown('<p class="module-header">МОДУЛЬ 4. ДОВІДКОВА ІНФОРМАЦІЯ</p>', unsafe_allow_html=True)
    st.link_button("4.1. Метеообстановка", "https://www.meteo.gov.ua/")

    with st.expander("📄 4.2. Методичні матеріали"):
        st.link_button("📜 Управління РХБ захисту ДСНС", "https://dsns.gov.ua/")
        st.link_button("📚 Методичні рекомендації", "https://dsns.gov.ua/metodichni-rekomendaciyi")

st.sidebar.caption("ОФІС CBRN v3.15")
