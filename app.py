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
.main-title {color:#ffcc00 !important; text-align:center !important; font-size:25px !important; font-weight:bold !important; margin-top:-30px !important; margin-bottom:15px !important; text-transform:uppercase !important;}
.module-header {color:#ffcc00 !important; border-bottom:1px solid #ffcc00 !important; margin-top:10px !important; margin-bottom:8px !important; font-weight:bold !important; font-size:22px !important; text-transform:uppercase !important;}
div[data-testid="stButton"] button, div[data-testid="stLinkButton"] a {background-color:#ffcc00 !important; color:#000 !important; border:none !important; width:100% !important; font-weight:bold !important; font-size:12px !important; border-radius:4px !important; padding:8px 12px !important; display:block !important; line-height:1.2 !important;}
div[data-testid="stButton"] button:hover, div[data-testid="stLinkButton"] a:hover {background-color:#e6b800 !important;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">Платформа підтримки прийняття рішення щодо реагування на РХБ інциденти</p>', unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1.2,4.6,1.2])

with col_left:
    st.markdown('<p class="module-header">МОДУЛЬ 1. РХБ ОБСТАНОВКА</p>', unsafe_allow_html=True)
    st.link_button("1.1. Карта радіаційного моніторингу (SaveEcoBot)", "https://www.saveecobot.com/radiation-maps")
    st.link_button("1.2. Карта радіаційного моніторингу країн ЄС", "https://remap.jrc.ec.europa.eu/Advanced.aspx")
    st.link_button("1.3. Карта прогнозу хімічної обстановки", "http://forecast.inf.ua/")
    st.link_button("1.4. Карта фактичної радіаційної обстановки", "https://radiation-situation-mt5eyizylhpa7sxaltawpk.streamlit.app/")
    st.link_button("1.5. Карта фактичної хімічної обстановки", "https://chemical-map-6refroql3kghrhuh7tzdma.streamlit.app/")
    st.info("💡 На картах підмодулів 1.4; 1.5 координати точки вимірювання завантажуються кліком мишки.")

with col_center:
    map_html = """
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.js"></script>
<script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>

<div id="map" style="height:750px; width:100%; border-radius:8px;"></div>

<br>
<button onclick="addText()" style="width:100%;padding:10px;margin-bottom:5px;background:#ffcc00;font-weight:bold;">Вставити текст</button>
<button onclick="downloadPNG()" style="width:100%;padding:10px;background:#ffcc00;font-weight:bold;">Завантажити карту PNG</button>

<script>
var map = L.map('map',{attributionControl:false}).setView([48.3794,31.1656],6);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
    crossOrigin:true
}).addTo(map);

var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

// --- СТИЛІ ---
function setStyle(layer){
    if(layer instanceof L.Circle){
        var radius = layer.getRadius();
        layer.setStyle({
            color:'black',
            fillColor: radius>5000?'yellow':'orange',
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
    draw:{polygon:true, rectangle:true, circle:true, polyline:true, marker:true},
    edit:{featureGroup: drawnItems}
});
map.addControl(drawControl);

// --- СТВОРЕННЯ ---
map.on(L.Draw.Event.CREATED, function(e){
    var layer = e.layer;

    // МАРКЕР
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
    } 
    else {
        setStyle(layer);
    }

    drawnItems.addLayer(layer);
});

// --- ТЕКСТ ---
function addText(){
    var text = prompt("Введіть текст:");
    if(text){
        var icon = L.divIcon({
            html:'<div style="background:white;padding:4px;border-radius:4px;">'+text+'</div>'
        });
        map.once('click', function(e){
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

with col_right:
    st.markdown('<p class="module-header">МОДУЛЬ 3. РОЗРАХУНКИ</p>', unsafe_allow_html=True)
    st.link_button("3.1. Калькулятор дози опромінення", "https://sergsh1125-dotcom.github.io/radiation-calculator/")
    st.link_button("3.2. Калькулятор аварії на АЕС", "https://sergsh1125-dotcom.github.io/radiation-doza/")
    st.link_button("3.3. Час перебування", "https://sergsh1125-dotcom.github.io/calculator-time/")

    st.markdown('<p class="module-header">МОДУЛЬ 4. ДОВІДКОВА ІНФОРМАЦІЯ</p>', unsafe_allow_html=True)
    st.link_button("4.1. Метеообстановка", "https://www.meteo.gov.ua/")

st.sidebar.caption("ОФІС CBRN v3.13")
