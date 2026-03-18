import streamlit as st
import streamlit.components.v1 as components

# --- 1. НАЛАШТУВАННЯ СТОРІНКИ ---
st.set_page_config(
    page_title="ОФІС CBRN",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. СТИЛІ ---
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

.main-title {
    color: #ffcc00 !important;
    text-align: center !important;
    font-size: 23px !important;
    font-weight: bold !important;
    margin-top: -30px !important;
    margin-bottom: 15px !important;
    text-transform: uppercase !important;
}

.module-header {
    color: #ffcc00 !important;
    border-bottom: 1px solid #ffcc00 !important;
    margin-top: 10px !important;
    margin-bottom: 8px !important;
    font-weight: bold !important;
    font-size: 14px !important;
    text-transform: uppercase !important;
}

div[data-testid="stButton"] button,
div[data-testid="stLinkButton"] a {
    background-color: #ffcc00 !important;
    color: #000 !important;
    width: 100% !important;
    font-weight: bold !important;
    font-size: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# --- 3. ЗАГОЛОВОК ---
st.markdown('<p class="main-title">Платформа підтримки прийняття рішення щодо реагування на РХБ інциденти</p>', unsafe_allow_html=True)

# --- 4. РОБОЧИЙ ПРОСТІР ---
col_left, col_center, col_right = st.columns([1.2, 4.6, 1.2])

with col_left:
    st.markdown('<p class="module-header">МОДУЛЬ 1</p>', unsafe_allow_html=True)
    st.link_button("Карта радіації", "https://www.saveecobot.com/radiation-maps")

with col_center:

    map_html = """
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css"/>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.js"></script>

<div id="map" style="height: 750px;"></div>
<br>
<button onclick="saveMap()" style="width:100%;padding:10px;font-weight:bold;background:#ffcc00;">
ЗБЕРЕГТИ КАРТУ У HTML
</button>

<script>

var map = L.map('map').setView([48.3794, 31.1656], 6);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// --- ГРУПА ---
var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

// --- СХОВИЩЕ ОБ'ЄКТІВ ---
var layersMap = {};

// --- РЕЖИМ ТЕКСТУ ---
var textMode = false;

// --- КНОПКА ТЕКСТУ ---
var textControl = L.control({position: 'topleft'});
textControl.onAdd = function () {
    var div = L.DomUtil.create('div');
    div.innerHTML = 'T';
    div.style.background = "white";
    div.style.padding = "5px";
    div.style.cursor = "pointer";

    div.onclick = function(e){
        e.preventDefault();
        textMode = !textMode;
        div.style.background = textMode ? "#ffcc00" : "white";
    };

    return div;
};
textControl.addTo(map);

// --- DRAW ---
var drawControl = new L.Control.Draw({
    edit: { featureGroup: drawnItems },
    draw: {
        polygon: true,
        rectangle: true,
        circle: true,
        polyline: true,
        marker: true,
        circlemarker: false
    }
});
map.addControl(drawControl);

// --- СТВОРЕННЯ ---
map.on(L.Draw.Event.CREATED, function (e) {

    var layer = e.layer;
    var type = e.layerType;

    var id = L.stamp(layer);
    layersMap[id] = layer;

    if (type === "marker") {

        var blueIcon = L.icon({
            iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png",
            shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png"
        });

        layer.setIcon(blueIcon);

        layer.on('click', function() {
            var c = layer.getLatLng();
            layer.bindPopup("Координати:<br>" + c.lat.toFixed(6)+", "+c.lng.toFixed(6)).openPopup();
        });

    } else {

        layer.setStyle({
            color: "black",
            fillColor: "yellow",
            fillOpacity: 0.4
        });

        var popup = `
        <b>Тип зони</b><br><br>
        <button onclick="setChemical(${id})">🟡 Хімічне</button><br><br>
        <button onclick="setRadiation(${id})">🔴 Радіація</button>
        `;

        layer.bindPopup(popup);
    }

    drawnItems.addLayer(layer);
});

// --- ФУНКЦІЇ ---
function setChemical(id){
    var l = layersMap[id];
    if(!l) return;
    l.setStyle({color:"black", fillColor:"yellow", fillOpacity:0.4});
}

function setRadiation(id){
    var l = layersMap[id];
    if(!l) return;
    l.setStyle({color:"black", fillColor:"#ff6666", fillOpacity:0.4});
}

// --- ТЕКСТ ---
map.on('click', function(e){
    if(textMode){
        var t = prompt("Текст:");
        if(t){
            var icon = L.divIcon({html:'<div style="background:white;padding:4px;">'+t+'</div>'});
            L.marker(e.latlng,{icon:icon}).addTo(map);
        }
    }
});

// --- ЛЕГЕНДА ---
var legend = L.control({position:'bottomleft'});
legend.onAdd = function(){
    var d = L.DomUtil.create('div');
    d.style.background="white";
    d.style.padding="10px";

    d.innerHTML="<b>Легенда</b><br><br>";
    d.innerHTML+="<div style='background:yellow;width:20px;height:10px;display:inline-block'></div> Хімічне<br>";
    d.innerHTML+="<div style='background:#ff6666;width:20px;height:10px;display:inline-block'></div> Радіація";

    return d;
};
legend.addTo(map);

// --- ЗБЕРЕЖЕННЯ ---
function saveMap(){
    var data = drawnItems.toGeoJSON();

    var html = `
    <html>
    <head>
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    </head>
    <body>
    <div id="map" style="height:100vh;"></div>
    <script>
    var map = L.map('map').setView([48.3,31.1],6);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    L.geoJSON(${JSON.stringify(data)}).addTo(map);
    <\/script>
    </body>
    </html>
    `;

    var blob = new Blob([html], {type:"text/html"});
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "map.html";
    a.click();
}

</script>
"""

    components.html(map_html, height=760)

with col_right:
    st.markdown('<p class="module-header">МОДУЛЬ 3</p>', unsafe_allow_html=True)

st.sidebar.caption("ОФІС CBRN v4.0")
