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
    font-size:20px !important;
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
    text-decoration: none !important;
    text-align: center;
}

/* Стилізація заголовка вибору маркера */
.selection-label {
    color: #ffcc00;
    font-weight: bold;
    font-size: 16px;
    margin-bottom: 5px;
}

div[data-testid="stRadio"] > label { display: none; } /* Приховуємо стандартний лейбл */
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">Платформа підтримки прийняття рішення щодо реагування на РХБ інциденти</p>', unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1.3, 4.4, 1.3])

with col_left:
    st.markdown('<p class="module-header">МОДУЛЬ 1. РХБ ОБСТАНОВКА</p>', unsafe_allow_html=True)
    st.link_button("1.1. Карта моніторингу (SaveEcoBot)", "https://www.saveecobot.com/radiation-maps")
    st.link_button("1.2. Карта країн ЄС (REMAP)", "https://remap.jrc.ec.europa.eu/Advanced.aspx")
    st.link_button("1.4. Фактична радіаційна обстановка", "https://radiation-situation-mt5eyizylhpa7sxaltawpk.streamlit.app/")
    st.link_button("1.5. Фактична хімічна обстановка", "https://chemical-map-6refroql3kghrhuh7tzdma.streamlit.app/")

    st.markdown('<p class="module-header">МОДУЛЬ 2. БАЗИ ДАНИХ</p>', unsafe_allow_html=True)
    st.link_button("2.1. Аварійні картки НХР", "https://sergsh1125-dotcom.github.io/emergency-cards/")
    st.link_button("2.2. Токсодози бойових ОР", "https://sergsh1125-dotcom.github.io/toxicdoze/")

with col_center:
    # Оновлений інтерфейс вибору
    st.markdown('<p class="selection-label">📍 Вибери тип маркера:</p>', unsafe_allow_html=True)
    draw_mode = st.radio(
        "label_hidden",
        ("Хімічно небезпечний об'єкт (Помаранчевий)", "Радіаційно небезпечний об'єкт (☢️)", "Зона забруднення (Жовте коло)", "Прогноз (Прозоре коло)"),
        horizontal=True,
        label_visibility="collapsed"
    )
    
    mode_map = {
        "Хімічно небезпечний об'єкт (Помаранчевий)": "chem_marker",
        "Радіаційно небезпечний об'єкт (☢️)": "rad_marker",
        "Зона забруднення (Жовте коло)": "yellow_circle",
        "Прогноз (Прозоре коло)": "clear_circle"
    }
    active_mode = mode_map[draw_mode]

    map_template = """
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.js"></script>
<script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>

<div id="capture_area" style="background:#0e1117; padding:5px; border-radius:8px;">
    <div id="map" style="height:600px; width:100%; border-radius:8px;"></div>
</div>

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 5px; margin-top: 10px;">
    <button onclick="addText()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer;">ТЕКСТ</button>
    <button onclick="clearMap()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer;">ОЧИСТИТИ</button>
    <button onclick="downloadPNG()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer;">PNG</button>
    <button onclick="window.print()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer;">PDF</button>
</div>

<script>
var activeMode = "JS_MODE_VALUE";
var map = L.map('map',{attributionControl:false, preferCanvas: true}).setView([48.3794,31.1656],6);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{ crossOrigin: 'anonymous' }).addTo(map);

var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

// 1. РАДІАЦІЙНИЙ ОБ'ЄКТ (Знак + надпис)
var radIcon = L.divIcon({
    html: '<div style="display:flex; align-items:center; gap:5px; white-space:nowrap;">' +
          '<div style="background:#ffcc00; border:2px solid black; border-radius:50%; width:30px; height:30px; display:flex; align-items:center; justify-content:center; color:black; font-size:18px;">☢️</div>' +
          '<span style="background:rgba(255,255,255,0.8); color:black; padding:2px 5px; border:1px solid black; border-radius:3px; font-weight:bold; font-size:10px;">Радіаційно небезпечний об’єкт</span></div>',
    className: 'c-rad', iconSize:[180,30], iconAnchor:[15,15]
});

// 2. ХІМІЧНИЙ ОБ'ЄКТ (Помаранчева точка + надпис)
var chemIcon = L.divIcon({
    html: '<div style="display:flex; align-items:center; gap:5px; white-space:nowrap;">' +
          '<div style="background:#ff6600; border:2px solid black; border-radius:50%; width:15px; height:15px;"></div>' +
          '<span style="background:rgba(255,255,255,0.8); color:black; padding:2px 5px; border:1px solid black; border-radius:3px; font-weight:bold; font-size:10px;">Хімічно небезпечний об’єкт</span></div>',
    className: 'c-chem', iconSize:[180,20], iconAnchor:[7,7]
});

var drawControl = new L.Control.Draw({
    draw:{
        polygon:true, rectangle:true, polyline:true,
        circle: {
            shapeOptions: {
                color: 'black',
                weight: 2,
                fillColor: (activeMode === 'clear_circle') ? 'transparent' : 'yellow',
                fillOpacity: (activeMode === 'clear_circle') ? 0 : 0.5
            }
        },
        marker: { icon: (activeMode === 'chem_marker') ? chemIcon : radIcon }
    },
    edit:{ featureGroup: drawnItems }
});
map.addControl(drawControl);

map.on(L.Draw.Event.CREATED, function(e){
    var layer = e.layer;
    if(e.layerType === 'marker') {
        layer.setIcon((activeMode === 'chem_marker') ? chemIcon : radIcon);
    } 
    else if(e.layerType === 'circle') {
        if(activeMode === 'clear_circle') {
            layer.setStyle({fillColor: 'transparent', fillOpacity: 0, color: 'black'});
        } else {
            layer.setStyle({fillColor: 'yellow', fillOpacity: 0.5, color: 'black'});
        }
    }
    else {
        layer.setStyle({color:'black', fillColor:'yellow', fillOpacity:0.5, weight:2});
    }
    drawnItems.addLayer(layer);
});

function addText(){
    var text = prompt("Введіть текст:");
    if(text){
        map.once('click', function(e){
            var icon = L.divIcon({
                html:'<div style="background:rgba(255,255,255,0.8); padding:2px 5px; border:1px solid black; border-radius:3px; font-weight:bold; color:black; white-space:nowrap;">'+text+'</div>',
                iconSize: null
            });
            L.marker(e.latlng,{icon:icon}).addTo(drawnItems);
        });
    }
}

function clearMap() { if(confirm("Очистити карту?")) drawnItems.clearLayers(); }

function downloadPNG(){
    html2canvas(document.getElementById("capture_area"), {useCORS: true, scale: 2}).then(canvas => {
        var link = document.createElement("a");
        link.download = "CBRN_Map.png";
        link.href = canvas.toDataURL();
        link.click();
    });
}
</script>
"""
    map_html = map_template.replace("JS_MODE_VALUE", active_mode)
    components.html(map_html, height=750)

with col_right:
    st.markdown('<p class="module-header">МОДУЛЬ 3. РОЗРАХУНКИ</p>', unsafe_allow_html=True)
    st.link_button("3.1. Доза при ядерному вибуху", "https://sergsh1125-dotcom.github.io/radiation-calculator/")
    st.link_button("3.2. Доза при аварії на АЕС", "https://sergsh1125-dotcom.github.io/radiation-doza/")
    st.link_button("3.3. Час перебування у зоні", "https://sergsh1125-dotcom.github.io/calculator-time/")

    st.markdown('<p class="module-header">МОДУЛЬ 4. ДОВІДКА</p>', unsafe_allow_html=True)
    st.link_button("4.1. Метеообстановка", "https://www.meteo.gov.ua/")
    with st.expander("📄 4.2. Методичні матеріали"):
        st.link_button("📜 Управління РХБЗ", "https://dsns.gov.ua/")

st.sidebar.caption("ОФІС CBRN v3.21")
