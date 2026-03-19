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
#MainMenu, footer, header, .stDeployButton {visibility: hidden; display: none !important;}
.block-container {padding:1rem !important; max-width:100% !important;}
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
    font-size:18px !important;
    text-transform:uppercase !important;
}

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
    text-align: center;
    text-decoration: none !important;
}

/* Стилізація радіокнопок */
div[data-testid="stRadio"] label {
    color: #e0e0e0 !important;
    font-size: 14px !important;
}
div[data-testid="stRadio"] p {
    color: #ffcc00 !important;
    font-weight: bold !important;
    font-size: 16px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">Платформа підтримки прийняття рішення щодо реагування на РХБ інциденти</p>', unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1.6, 4.2, 1.2])

# -------- ЛІВА ПАНЕЛЬ (МОДУЛІ ТА ВИБІР МАРКЕРА) --------
with col_left:
    st.markdown('<p class="module-header">МОДУЛЬ 1. РХБ ОБСТАНОВКА</p>', unsafe_allow_html=True)
    st.link_button("1.1. Карта моніторингу (SaveEcoBot)", "https://www.saveecobot.com/radiation-maps")
    st.link_button("1.2. Карта країн ЄС (REMAP)", "https://remap.jrc.ec.europa.eu/Advanced.aspx")
    st.link_button("1.4. Радіаційна обстановка (Фактична)", "https://radiation-situation-mt5eyizylhpa7sxaltawpk.streamlit.app/")
    st.link_button("1.5. Хімічна обстановка (Фактична)", "https://chemical-map-6refroql3kghrhuh7tzdma.streamlit.app/")

    st.markdown('<p class="module-header">МОДУЛЬ 2. БАЗИ ДАНИХ</p>', unsafe_allow_html=True)
    st.link_button("2.1. Аварійні картки НХР", "https://sergsh1125-dotcom.github.io/emergency-cards/")
    st.link_button("2.2. Токсодози бойових ОР", "https://sergsh1125-dotcom.github.io/toxicdoze/")

    st.write("")
    # ПАНЕЛЬ ВИБОРУ МАРКЕРІВ (ЗА ЗАПИТОМ)
    st.markdown("---")
    draw_mode = st.radio(
        "Вибери тип маркера:",
        ("ХНО (Хімічно небезпечний об'єкт)", 
         "РНО (Радіаційно небезпечний об'єкт)", 
         "Зона забруднення (Жовте коло)", 
         "Прогноз (Прозоре коло)"),
        index=0
    )
    
    mode_map = {
        "ХНО (Хімічно небезпечний об'єкт)": "chem",
        "РНО (Радіаційно небезпечний об'єкт)": "rad",
        "Зона забруднення (Жовте коло)": "yellow_circle",
        "Прогноз (Прозоре коло)": "clear_circle"
    }
    active_mode = mode_map[draw_mode]

# -------- ЦЕНТР (КАРТА) --------
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
    <button onclick="clearMap()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer;">ОЧИСТИТИ КАРТУ</button>
    <button onclick="downloadPNG()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer;">PNG</button>
    <button onclick="window.print()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer;">PDF ЗВІТ</button>
</div>

<script>
var activeMode = "JS_MODE_VALUE";
var map = L.map('map',{attributionControl:false, preferCanvas: true}).setView([48.3794,31.1656],6);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{ crossOrigin: 'anonymous' }).addTo(map);

var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

// --- ІКОНКИ ТА СТИЛІ ---
var radIcon = L.divIcon({
    html: '<div style="background:#ffcc00; border:2px solid black; border-radius:50%; width:30px; height:30px; display:flex; align-items:center; justify-content:center; color:black; font-size:18px;">☢️</div>',
    className: 'c-rad', iconSize:[30,30], iconAnchor:[15,15]
});

var yellowIcon = L.divIcon({
    html: '<div style="background:#ffcc00; border:2px solid black; border-radius:50%; width:16px; height:16px;"></div>',
    className: 'c-yellow', iconSize:[16,16], iconAnchor:[8,8]
});

// Зменшена вдвічі синя точка (radius: 3)
var bluePointStyle = { radius: 3, fillColor: "#007bff", color: "#000", weight: 1, opacity: 1, fillOpacity: 0.9 };

// --- ВІДНОВЛЕННЯ ДАНИХ ПРИ ПЕРЕМИКАННІ (ПЕРСИСТЕНТНІСТЬ) ---
var storageKey = 'cbrn_v3_data';
var saved = localStorage.getItem(storageKey);
if (saved) {
    var json = JSON.parse(saved);
    L.geoJSON(json, {
        pointToLayer: function(feature, latlng) {
            if (feature.properties.cType === 'rad') return L.marker(latlng, {icon: radIcon});
            if (feature.properties.cType === 'chem') return L.marker(latlng, {icon: yellowIcon});
            if (feature.properties.cType === 'meas') return L.circleMarker(latlng, bluePointStyle);
            return L.marker(latlng);
        },
        style: function(feature) { return feature.properties.style || {}; },
        onEachLayer: function(layer, l) {
            if (layer instanceof L.Marker && !layer.options.icon) {
                 // Для текстових міток
            }
            drawnItems.addLayer(layer);
        }
    });
}

function saveData() {
    var data = drawnItems.toGeoJSON();
    drawnItems.eachLayer(function(layer, i) {
        if (layer instanceof L.Marker) {
            if (layer.options.icon === radIcon) data.features[i].properties.cType = 'rad';
            else if (layer.options.icon === yellowIcon) data.features[i].properties.cType = 'chem';
        } else if (layer instanceof L.CircleMarker && layer.options.radius === 3) {
            data.features[i].properties.cType = 'meas';
        } else if (layer.options.style || layer.options.fillColor) {
            data.features[i].properties.style = layer.options;
        }
    });
    localStorage.setItem(storageKey, JSON.stringify(data));
}

// --- КОНТРОЛЬ МАЛЮВАННЯ ---
var drawControl = new L.Control.Draw({
    draw:{
        polygon: { shapeOptions: { color: 'black', fillColor: 'yellow', fillOpacity: 0.5, weight: 2 } },
        rectangle: { shapeOptions: { color: 'black', fillColor: 'yellow', fillOpacity: 0.5, weight: 2 } },
        polyline: { shapeOptions: { color: 'black', weight: 3 } },
        circle: {
            shapeOptions: {
                color: 'black', weight: 2,
                fillColor: (activeMode === 'clear_circle') ? 'transparent' : 'yellow',
                fillOpacity: (activeMode === 'clear_circle') ? 0 : 0.5
            }
        },
        marker: { icon: (activeMode === 'chem') ? yellowIcon : radIcon },
        circlemarker: bluePointStyle
    },
    edit: { featureGroup: drawnItems }
});
map.addControl(drawControl);

map.on(L.Draw.Event.CREATED, function(e){
    var layer = e.layer;
    if (e.layerType === 'marker') {
        layer.setIcon((activeMode === 'chem') ? yellowIcon : radIcon);
    }
    drawnItems.addLayer(layer);
    saveData();
});

map.on(L.Draw.Event.EDITED, saveData);
map.on(L.Draw.Event.DELETED, saveData);

function addText(){
    var text = prompt("Назва об'єкту:");
    if(text){
        map.once('click', function(e){
            var tIcon = L.divIcon({
                html:'<div style="background:rgba(255,255,255,0.85); padding:1px 4px; border:1px solid black; border-radius:3px; font-weight:bold; color:black; white-space:nowrap; font-size:11px;">'+text+'</div>',
                iconSize: null
            });
            L.marker(e.latlng,{icon:tIcon}).addTo(drawnItems);
            saveData();
        });
    }
}

function clearMap() {
    if(confirm("Видалити всю обстановку з карти?")) {
        drawnItems.clearLayers();
        localStorage.removeItem(storageKey);
    }
}

function downloadPNG(){
    html2canvas(document.getElementById("capture_area"), {useCORS: true, scale: 2}).then(canvas => {
        var link = document.createElement("a");
        link.download = "CBRN_Map_Export.png";
        link.href = canvas.toDataURL();
        link.click();
    });
}
</script>
"""
    # Заміна для усунення SyntaxError та передачі стану
    map_html = map_template.replace("JS_MODE_VALUE", active_mode)
    components.html(map_html, height=730)

# -------- ПРАВА ПАНЕЛЬ (РОЗРАХУНКИ) --------
with col_right:
    st.markdown('<p class="module-header">МОДУЛЬ 3</p>', unsafe_allow_html=True)
    st.link_button("☢️ Доза (Ядерна)", "https://sergsh1125-dotcom.github.io/radiation-calculator/")
    st.link_button("⚛️ Доза (АЕС)", "https://sergsh1125-dotcom.github.io/radiation-doza/")
    st.link_button("⏳ Час роботи", "https://sergsh1125-dotcom.github.io/calculator-time/")

    st.markdown('<p class="module-header">МОДУЛЬ 4</p>', unsafe_allow_html=True)
    st.link_button("☁️ Метео", "https://www.meteo.gov.ua/")

st.sidebar.caption("ОФІС CBRN v3.23 | Нанесення обстановки")
