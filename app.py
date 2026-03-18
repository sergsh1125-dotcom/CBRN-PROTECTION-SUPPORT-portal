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
.block-container { padding: 1rem !important; max-width: 100% !important; }
#MainMenu, footer, header {visibility: hidden;}
.stApp {background-color: #0e1117; color: #e0e0e0;}
.main-title { color: #ffcc00 !important; text-align: center !important; font-size: 23px !important; font-weight: bold !important; margin-top: -30px !important; margin-bottom: 15px !important; text-transform: uppercase !important;}
.module-header { color: #ffcc00 !important; border-bottom: 1px solid #ffcc00 !important; margin-top: 10px !important; margin-bottom: 8px !important; font-weight: bold !important; font-size: 14px !important; text-transform: uppercase !important;}
div[data-testid="stButton"] button, div[data-testid="stLinkButton"] a { background-color: #ffcc00 !important; color: #000000 !important; border: none !important; width: 100% !important; font-weight: bold !important; font-size: 12px !important; border-radius: 4px !important; padding: 8px 12px !important; display: block !important; text-decoration: none !important; line-height: 1.2 !important;}
.stExpander { background-color: #ffcc00 !important; border: none !important; border-radius: 4px !important; }
.stExpander summary { color: #000000 !important; font-weight: bold !important; }
.stExpander summary svg { fill: #000000 !important; }
div[data-testid="stButton"] button:hover, div[data-testid="stLinkButton"] a:hover { background-color: #e6b800 !important; }
iframe { border: 1px solid #3d444d !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. ЗАГОЛОВОК ---
st.markdown('<p class="main-title">Платформа підтримки прийняття рішення щодо реагування на РХБ інциденти</p>', unsafe_allow_html=True)

# --- 4. КОЛОНКИ ---
col_left, col_center, col_right = st.columns([1.2, 4.6, 1.2])

with col_left:
    st.markdown('<p class="module-header">МОДУЛЬ 1. РХБ ОБСТАНОВКА</p>', unsafe_allow_html=True)
    st.link_button("1.1. Карта радіаційного моніторингу (SaveEcoBot)", "https://www.saveecobot.com/radiation-maps")
    st.link_button("1.2. Карта радіаційного моніторингу країн ЄС", "https://remap.jrc.ec.europa.eu/Advanced.aspx")
    st.link_button("1.3. Карта прогнозу хімічної обстановки", "http://forecast.inf.ua/")
    st.link_button("1.4. Карта фактичної радіаційної обстановки", "https://radiation-situation-mt5eyizylhpa7sxaltawpk.streamlit.app/")
    st.link_button("1.5. Карта фактичної хімічної обстановки", "https://chemical-map-6refroql3kghrhuh7tzdma.streamlit.app/")
    st.info("💡 Клікніть на карту, щоб скопіювати координати.")

with col_center:
    map_html = """
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.js"></script>

<div id="map" style="height: 750px; border-radius: 8px;"></div>
<br>
<button onclick="saveMap()" style="width:100%;padding:10px;font-weight:bold;background:#ffcc00;border:none;border-radius:6px;">ЗБЕРЕГТИ КАРТУ У HTML</button>

<script>
var map = L.map('map').setView([48.3794, 31.1656], 6);

// --- OSM ---
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// --- стартовий маркер ---
var startMarker = L.marker([48.3794, 31.1656]).addTo(map);
startMarker.bindPopup("Стартова точка").openPopup();

// --- група для малювання ---
var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

var textMode = false;

// --- кнопка тексту ---
var textControl = L.control({position: 'topleft'});
textControl.onAdd = function () {
    var div = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
    div.innerHTML = '<a href="#" title="Текст">T</a>';
    div.style.background = "white"; div.style.textAlign = "center"; div.style.fontWeight = "bold"; div.style.fontSize = "18px";
    div.onclick = function(e){ e.preventDefault(); textMode = !textMode; div.style.background = textMode ? "#ffcc00" : "white"; };
    return div;
};
textControl.addTo(map);

// --- панель малювання ---
var drawControl = new L.Control.Draw({
    edit: { featureGroup: drawnItems },
    draw: { polygon:true, rectangle:true, circle:true, polyline:true, marker:true, circlemarker:false }
});
map.addControl(drawControl);

// --- стиль зон ---
function setStyle(layer) {
    layer.setStyle({ color: "black", weight: 2, fillColor: "yellow", fillOpacity: 0.4 });
}

// --- додавання об'єктів ---
map.on(L.Draw.Event.CREATED, function (e) {
    var layer = e.layer;
    var type = e.layerType;
    if(type === "marker") {
        layer.on('click', function() {
            var coords = layer.getLatLng().lat.toFixed(6) + ", " + layer.getLatLng().lng.toFixed(6);
            layer.bindPopup("Координати:<br>" + coords).openPopup();
        });
    } else {
        setStyle(layer);
        var popupContent = `<b>Тип зони:</b><br><br>
            <button onclick="this.closest('.leaflet-popup-content').innerHTML='🟡 Хімічне';">Хімічне</button><br><br>
            <button onclick="this.closest('.leaflet-popup-content').innerHTML='🔴 Радіація';">Радіація</button>`;
        layer.bindPopup(popupContent);
    }
    drawnItems.addLayer(layer);
});

// --- текст ---
map.on('click', function(e) {
    if(textMode) {
        var text = prompt("Введіть текст:");
        if(text) { L.marker(e.latlng, {icon: L.divIcon({html:'<div style="background:white;padding:4px;border-radius:4px;">'+text+'</div>'})}).addTo(map); }
    }
});

// --- легенда ---
var legend = L.control({position: 'bottomleft'});
legend.onAdd = function () {
    var div = L.DomUtil.create('div');
    div.style.background="white"; div.style.padding="10px"; div.style.border="2px solid gray";
    div.innerHTML += "<b>Легенда</b><br><br>";
    div.innerHTML += "<div style='background:yellow;width:20px;height:10px;display:inline-block'></div> Хімічне забруднення<br>";
    div.innerHTML += "<div style='background:#ff6666;width:20px;height:10px;display:inline-block'></div> Радіоактивне забруднення";
    return div;
};
legend.addTo(map);

// --- збереження карти ---
function saveMap() {
    var data = drawnItems.toGeoJSON();
    var htmlContent = `<html><head><meta charset="utf-8"/><link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/><script src="https://unpkg.com/leaflet/dist/leaflet.js"></script></head><body><div id="map" style="width:100%;height:100vh;"></div><script>
        var map = L.map('map').setView([48.3794, 31.1656],6);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
        L.geoJSON(${JSON.stringify(data)}).addTo(map);
    </script></body></html>`;
    var blob = new Blob([htmlContent], {type:"text/html"});
    var link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "rhb_map.html";
    link.click();
}
</script>
"""
    components.html(map_html, height=760)

with col_right:
    st.markdown('<p class="module-header">МОДУЛЬ 3. РОЗРАХУНКИ</p>', unsafe_allow_html=True)
    st.link_button("3.1. Калькулятор дози опромінення при ядерному вибуху", "https://sergsh1125-dotcom.github.io/radiation-calculator/")
    st.link_button("3.2. Калькулятор дози опромінення при аварії на АЕС", "https://sergsh1125-dotcom.github.io/radiation-doza/")
    st.link_button("3.3. Калькулятор часу перебування у зоні забруднення", "https://sergsh1125-dotcom.github.io/calculator-time/")

    st.markdown('<p class="module-header">МОДУЛЬ 4. ДОВІДКОВА ІНФОРМАЦІЯ</p>', unsafe_allow_html=True)
    st.link_button("4.1. Метеообстановка", "https://www.meteo.gov.ua/")
    with st.expander("📄 4.2. Методичні матеріали"):
        st.link_button("📜 Управління РХБ захисту ДСНС", "https://dsns.gov.ua/zakonodavstvo/perelik-normativno-pravovix-dokumentiv-shho-reglamentuyut-diyalnist-pidrozdiliv-dsns-ukrayini/upravlinnia-organizaciyi-radiaciinogo-ximicnogo-ta-biologicnogo-zaxistu")
        st.link_button("📚 Методичні рекомендації", "https://dsns.gov.ua/metodichni-rekomendaciyi")

st.sidebar.caption("ОФІС CBRN v3.8")
