import streamlit as st
import streamlit.components.v1 as components

# --- Налаштування сторінки ---
st.set_page_config(
    page_title="ОФІС CBRN",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Стилізація ---
st.markdown("""
<style>
.block-container {
    padding:1rem !important;
    max-width:100% !important;
}
#MainMenu, footer, header {visibility:hidden;}
.stApp {background-color:#0e1117; color:#e0e0e0;}
.main-title {color:#ffcc00; text-align:center; font-size:23px; font-weight:bold; margin-top:-30px; margin-bottom:15px; text-transform:uppercase;}
.module-header {color:#ffcc00; border-bottom:1px solid #ffcc00; margin-top:10px; margin-bottom:8px; font-weight:bold; font-size:14px; text-transform:uppercase;}
div[data-testid="stButton"] button, div[data-testid="stLinkButton"] a {
    background-color:#ffcc00 !important; color:#000; border:none; width:100%; font-weight:bold; font-size:12px; border-radius:4px; padding:8px 12px; display:block; text-decoration:none; line-height:1.2;
}
div[data-testid="stButton"] button:hover, div[data-testid="stLinkButton"] a:hover {background-color:#e6b800 !important;}
.stExpander {background-color:#ffcc00; border:none; border-radius:4px;}
.stExpander summary {color:#000; font-weight:bold;}
.stExpander summary svg {fill:#000;}
iframe {border:1px solid #3d444d !important; border-radius:8px;}
</style>
""", unsafe_allow_html=True)

# --- Заголовок ---
st.markdown('<p class="main-title">Платформа підтримки прийняття рішення щодо реагування на РХБ інциденти</p>', unsafe_allow_html=True)

# --- Колонки ---
col_left, col_center, col_right = st.columns([1.2, 4.6, 1.2])

# --- Ліва колонка ---
with col_left:
    st.markdown('<p class="module-header">МОДУЛЬ 1. РХБ ОБСТАНОВКА</p>', unsafe_allow_html=True)
    st.link_button("1.1. Карта радіаційного моніторингу (SaveEcoBot)", "https://www.saveecobot.com/radiation-maps")
    st.link_button("1.2. Карта радіаційного моніторингу країн ЄС", "https://remap.jrc.ec.europa.eu/Advanced.aspx")
    st.link_button("1.3. Карта прогнозу хімічної обстановки", "http://forecast.inf.ua/")
    st.link_button("1.4. Карта фактичної радіаційної обстановки", "https://radiation-situation-mt5eyizylhpa7sxaltawpk.streamlit.app/")
    st.link_button("1.5. Карта фактичної хімічної обстановки", "https://chemical-map-6refroql3kghrhuh7tzdma.streamlit.app/")
    st.info("💡 Клікніть на карту фактичної радіаційної або хімічної обстановки, щоб скопіювати координати.")

    st.markdown('<p class="module-header">МОДУЛЬ 2. БАЗИ ДАНИХ</p>', unsafe_allow_html=True)
    st.link_button("2.1. Аварійні картки НХР", "https://sergsh1125-dotcom.github.io/emergency-cards/")
    st.link_button("2.2. Токсодози бойових ОР", "https://sergsh1125-dotcom.github.io/toxicdoze/")

# --- Центр: інтерактивна карта ---
with col_center:
    map_html = """
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.js"></script>

<div id="map" style="height:750px;"></div>
<br>
<button id="saveBtn" style="width:100%;padding:10px;font-weight:bold;background:#ffcc00;border:none;border-radius:6px;">
ЗБЕРЕГТИ КАРТУ У HTML
</button>

<script>
var map = L.map('map').setView([48.3794,31.1656],6);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap contributors'}).addTo(map);
var drawnItems = new L.FeatureGroup(); map.addLayer(drawnItems);
var layersMap = {};
var textMode = false;

// Текст кнопка
var textControl = L.control({position:'topleft'});
textControl.onAdd = function(){
    var div = L.DomUtil.create('div');
    div.innerHTML = 'T'; div.style.background='white'; div.style.padding='5px'; div.style.cursor='pointer'; div.style.fontWeight='bold';
    div.onclick=function(e){ e.preventDefault(); textMode=!textMode; div.style.background=textMode?"#ffcc00":"white"; };
    return div;
};
textControl.addTo(map);

// Draw Control
var drawControl = new L.Control.Draw({edit:{featureGroup:drawnItems}, draw:{polygon:true, rectangle:true, circle:true, polyline:true, marker:true, circlemarker:false}});
map.addControl(drawControl);

// Стилі
function styleLayer(layer,color){ layer.setStyle({color:"black", weight:2, fillColor:color, fillOpacity:0.4}); }

// Подія створення
map.on(L.Draw.Event.CREATED,function(e){
    var layer = e.layer; var type=e.layerType; var id=L.stamp(layer); layersMap[id]=layer;
    if(type==="marker"){
        var blueIcon = L.icon({iconUrl:'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png', shadowUrl:'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png', iconSize:[25,41], iconAnchor:[12,41]});
        layer.setIcon(blueIcon);
        layer.on('click',function(){ var c=layer.getLatLng(); layer.bindPopup("Координати:<br>"+c.lat.toFixed(6)+", "+c.lng.toFixed(6)).openPopup(); });
    } else {
        styleLayer(layer,"yellow");
        layer.bindPopup("<b>Тип зони:</b><br>"+
            "<button onclick='styleLayer(layersMap["+id+"],\"yellow\")'>🟡 Хімічне</button><br>"+
            "<button onclick='styleLayer(layersMap["+id+"],\"#ff6666\")'>🔴 Радіація</button>");
    }
    drawnItems.addLayer(layer);
});

// Додавання тексту
map.on('click',function(e){ if(textMode){ var t=prompt("Введіть текст:"); if(t){ var icon=L.divIcon({html:'<div style="background:white;padding:4px;border-radius:4px;">'+t+'</div>'}); L.marker(e.latlng,{icon:icon}).addTo(map); } } });

// Легенда
var legend=L.control({position:'bottomleft'});
legend.onAdd=function(){ var d=L.DomUtil.create('div'); d.style.background='white'; d.style.padding='10px';
d.innerHTML="<b>Легенда</b><br><br>";
d.innerHTML+="<div style='background:yellow;width:20px;height:10px;display:inline-block'></div> Хімічне забруднення<br>";
d.innerHTML+="<div style='background:#ff6666;width:20px;height:10px;display:inline-block'></div> Радіоактивне забруднення";
return d;};
legend.addTo(map);

// Збереження карти
document.getElementById("saveBtn").onclick=function(){
    var data=drawnItems.toGeoJSON();
    var html=`<html><head><link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/><script src="https://unpkg.com/leaflet/dist/leaflet.js"></script></head><body><div id="map" style="height:100vh;"></div><script>
    var map=L.map('map').setView([48.3794,31.1656],6);L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    L.geoJSON(${JSON.stringify(data)}).addTo(map);
    <\/script></body></html>`;
    var blob=new Blob([html],{type:"text/html"}); var a=document.createElement("a"); a.href=URL.createObjectURL(blob); a.download="rhb_map.html"; a.click();
};
</script>
"""
    components.html(map_html,height=760)

# --- Права колонка ---
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

st.sidebar.caption("ОФІС CBRN v4.2")
