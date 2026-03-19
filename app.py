import streamlit as st
import streamlit.components.v1 as _components

# --- 1. НАЛАШТУВАННЯ СТОРІНКИ ---
st.set_page_config(page_title="ОФІС CBRN", page_icon="☢️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
#MainMenu, footer, header, .stDeployButton {visibility: hidden; display: none !important;}
.block-container {padding:1rem !important; max-width:100% !important;}
.stApp {background-color:#0e1117; color:#e0e0e0;}
.main-title {color:#ffcc00 !important; text-align:center !important; font-size:25px !important; font-weight:bold !important; margin-top:-30px !important; text-transform:uppercase !important;}
.module-header {color:#ffcc00 !important; border-bottom:1px solid #ffcc00 !important; margin-top:10px !important; font-weight:bold !important; font-size:18px !important; text-transform:uppercase !important;}
div[data-testid="stLinkButton"] a {background-color:#ffcc00 !important; color:#000 !important; font-weight:bold !important; font-size:12px !important; border-radius:4px !important; display:block !important; text-align: center; text-decoration: none !important; padding: 8px !important;}
div[data-testid="stRadio"] p {color: #ffcc00 !important; font-weight: bold !important; font-size: 16px !important;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">Платформа підтримки прийняття рішення щодо реагування на РХБ інциденти</p>', unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1.6, 4.2, 1.2])

with col_left:
    st.markdown('<p class="module-header">МОДУЛЬ 1. РХБ ОБСТАНОВКА</p>', unsafe_allow_html=True)
    st.link_button("1.1. Карта моніторингу (SaveEcoBot)", "https://www.saveecobot.com/radiation-maps")
    st.link_button("1.2. Карта країн ЄС (REMAP)", "https://remap.jrc.ec.europa.eu/Advanced.aspx")
    st.link_button("1.4. Радіаційна обстановка", "https://radiation-situation-mt5eyizylhpa7sxaltawpk.streamlit.app/")
    st.link_button("1.5. Хімічна обстановка", "https://chemical-map-6refroql3kghrhuh7tzdma.streamlit.app/")
    
    st.markdown('<p class="module-header">МОДУЛЬ 2. БАЗИ ДАНИХ</p>', unsafe_allow_html=True)
    st.link_button("2.1. Аварійні картки НХР", "https://sergsh1125-dotcom.github.io/emergency-cards/")
    st.link_button("2.2. Токсодози бойових ОР", "https://sergsh1125-dotcom.github.io/toxicdoze/")

    st.write("---")
    draw_mode = st.radio(
        "Вибери тип маркера:",
        ("ХНО", "РНО", "Зона забруднення (Жовта)", "Прогноз (Прозора)"),
        index=0
    )
    
    mode_map = {"ХНО": "chem", "РНО": "rad", "Зона забруднення (Жовта)": "yellow_circle", "Прогноз (Прозора)": "clear_circle"}
    active_mode = mode_map[draw_mode]

with col_center:
    map_template = """
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.js"></script>
<script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>

<div id="capture_area" style="background:#0e1117; padding:5px; border-radius:8px;">
    <div id="map" style="height:650px; width:100%; border-radius:8px;"></div>
</div>

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 5px; margin-top: 10px;">
    <button onclick="addText()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer;">ТЕКСТ</button>
    <button onclick="clearMap()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer;">ОЧИСТИТИ</button>
    <button onclick="downloadPNG()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer;">PNG</button>
    <button onclick="window.print()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer;">PDF</button>
</div>

<script>
var activeMode = "JS_MODE_VALUE";
var map = L.map('map',{attributionControl:false}).setView([48.3794,31.1656],6);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{crossOrigin:'anonymous'}).addTo(map);

var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

var radIcon = L.divIcon({html:'<div style="background:#ffcc00; border:2px solid black; border-radius:50%; width:18px; height:18px; display:flex; align-items:center; justify-content:center; font-size:12px;">☢️</div>', className:'', iconSize:[18,18], iconAnchor:[9,9]});
var yellowIcon = L.divIcon({html:'<div style="background:#ffcc00; border:2px solid black; border-radius:50%; width:18px; height:18px;"></div>', className:'', iconSize:[18,18], iconAnchor:[9,9]});
var blueStyle = {radius:3, fillColor:"#007bff", color:"#000", weight:1, fillOpacity:0.9};

// --- СТІЙКЕ ЗБЕРЕЖЕННЯ ---
var storageKey = 'cbrn_v27_stable';
var saved = localStorage.getItem(storageKey);
if(saved) {
    try {
        var json = JSON.parse(saved);
        L.geoJSON(json, {
            pointToLayer: function(f, l) {
                if(f.properties.t === 'rad') return L.marker(l, {icon: radIcon});
                if(f.properties.t === 'chem') return L.marker(l, {icon: yellowIcon});
                if(f.properties.t === 'blue') return L.circleMarker(l, blueStyle);
                return L.marker(l);
            },
            style: function(f) { return f.properties.s || {}; }
        }).eachLayer(l => drawnItems.addLayer(l));
    } catch(e) { console.log(e); }
}

function save() {
    var data = drawnItems.toGeoJSON();
    drawnItems.eachLayer((l, i) => {
        if(l instanceof L.Marker) {
            if(l.options.icon === radIcon) data.features[i].properties.t = 'rad';
            else if(l.options.icon === yellowIcon) data.features[i].properties.t = 'chem';
        } else if(l instanceof L.CircleMarker && l.options.radius === 3) {
            data.features[i].properties.t = 'blue';
        } else {
            data.features[i].properties.s = l.options;
        }
    });
    localStorage.setItem(storageKey, JSON.stringify(data));
}

// --- НАЛАШТУВАННЯ ПАНЕЛІ МАЛЮВАННЯ ---
var drawControl = new L.Control.Draw({
    draw:{
        polygon: {shapeOptions:{color:'black', fillColor:'yellow', fillOpacity:0.5, weight:2}},
        rectangle: {shapeOptions:{color:'black', fillColor:'yellow', fillOpacity:0.5, weight:2}},
        circle: {shapeOptions:{color:'black', fillColor:(activeMode==='clear_circle'?'transparent':'yellow'), fillOpacity:(activeMode==='clear_circle'?0:0.5), weight:2}},
        marker: {icon: (activeMode==='chem'?yellowIcon:radIcon)},
        circlemarker: blueStyle
    },
    edit: {featureGroup: drawnItems}
});
map.addControl(drawControl);

// --- ЛОГІКА ЗАВЕРШЕННЯ ОПЕРАЦІЇ ---
map.on(L.Draw.Event.CREATED, function(e){
    var layer = e.layer;
    if(e.layerType === 'marker') {
        layer.setIcon(activeMode==='chem'?yellowIcon:radIcon);
    }
    drawnItems.addLayer(layer);
    save();
    
    // ПРИМУСОВЕ ВИМКНЕННЯ ІНСТРУМЕНТУ ПІСЛЯ ОДНОГО НАНЕСЕННЯ
    var type = e.layerType;
    drawControl._toolbars.draw._modes[type].handler.disable();
});

map.on(L.Draw.Event.EDITED, save);
map.on(L.Draw.Event.DELETED, save);

function addText(){
    var t = prompt("Назва об'єкту:");
    if(t) {
        map.once('click', e => {
            L.marker(e.latlng, {icon: L.divIcon({html:'<div style="background:rgba(255,255,255,0.85); padding:1px 4px; border:1px solid black; font-weight:bold; color:black; white-space:nowrap; font-size:11px;">'+t+'</div>', className:''})}).addTo(drawnItems);
            save();
        });
    }
}

function clearMap() { 
    if(confirm("Видалити всю обстановку?")) { 
        drawnItems.clearLayers(); 
        localStorage.removeItem(storageKey); 
    } 
}

function downloadPNG(){
    html2canvas(document.getElementById("capture_area"), {useCORS:true, scale:2}).then(c => {
        var l = document.createElement("a"); l.download="CBRN_Map.png"; l.href=c.toDataURL(); l.click();
    });
}
</script>
"""
    st.components.v1.html(map_template.replace("JS_MODE_VALUE", active_mode), height=730)

with col_right:
    st.markdown('<p class="module-header">МОДУЛЬ 3</p>', unsafe_allow_html=True)
    st.link_button("☢️ Доза (ЯВ)", "https://sergsh1125-dotcom.github.io/radiation-calculator/")
    st.link_button("⚛️ Доза (АЕС)", "https://sergsh1125-dotcom.github.io/radiation-doza/")
    st.link_button("⏳ Час", "https://sergsh1125-dotcom.github.io/calculator-time/")
    st.markdown('<p class="module-header">МОДУЛЬ 4</p>', unsafe_allow_html=True)
    st.link_button("☁️ Метео", "https://www.meteo.gov.ua/")

st.sidebar.caption("ОФІС CBRN v3.27 | Стабільна обстановка")
