import streamlit as st
import streamlit.components.v1 as components

# --- 1. Налаштування сторінки ---
st.set_page_config(
    page_title="ОФІС CBRN",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. Заголовок ---
st.markdown('<h2 style="color:#ffcc00;text-align:center;">Платформа підтримки прийняття рішення щодо реагування на РХБ інциденти</h2>', unsafe_allow_html=True)

# --- 3. Розділення на колонки ---
col_left, col_center, col_right = st.columns([1.2, 4.6, 1.2])

with col_left:
    st.markdown('<b style="color:#ffcc00;">МОДУЛЬ 1. РХБ ОБСТАНОВКА</b>', unsafe_allow_html=True)
    st.link_button("Карта радіаційного моніторингу (SaveEcoBot)", "https://www.saveecobot.com/radiation-maps")
    st.link_button("Карта прогнозу хімічної обстановки", "http://forecast.inf.ua/")

with col_center:
    map_html = """
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.js"></script>

<div id="map" style="height:750px;"></div>
<br>
<button onclick="saveMap()" style="width:100%;padding:10px;font-weight:bold;background:#ffcc00;border:none;border-radius:6px;">
ЗБЕРЕГТИ КАРТУ У HTML
</button>

<script>
window.onload = function(){

    var map = L.map('map').setView([48.3794,31.1656],6);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
        attribution:'© OpenStreetMap contributors'
    }).addTo(map);

    var drawnItems = new L.FeatureGroup().addTo(map);
    var layersMap = {};

    // --- Стартовий маркер ---
    var startMarker = L.marker([48.3794,31.1656], {
        icon: L.icon({
            iconUrl:'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png',
            shadowUrl:'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
            iconSize:[25,41],
            iconAnchor:[12,41]
        })
    }).addTo(map).bindPopup("Центр України").openPopup();

    drawnItems.addLayer(startMarker);
    layersMap[L.stamp(startMarker)] = startMarker;

    // --- Режим тексту ---
    var textMode = false;
    var textControl = L.control({position:'topleft'});
    textControl.onAdd = function(){
        var div = L.DomUtil.create('div');
        div.innerHTML = 'T';
        div.style.background='white';
        div.style.padding='5px';
        div.style.cursor='pointer';
        div.style.fontWeight='bold';
        div.onclick=function(e){
            e.preventDefault();
            textMode = !textMode;
            div.style.background = textMode ? "#ffcc00" : "white";
        };
        return div;
    };
    textControl.addTo(map);

    // --- Draw Control ---
    var drawControl = new L.Control.Draw({
        edit:{ featureGroup: drawnItems },
        draw:{
            polygon:true,
            rectangle:true,
            circle:true,
            polyline:true,
            marker:true,
            circlemarker:false
        }
    });
    map.addControl(drawControl);

    // --- Стиль об’єктів ---
    function setChemical(id){ var l=layersMap[id]; if(l) l.setStyle({color:"black",fillColor:"yellow",fillOpacity:0.4}); }
    function setRadiation(id){ var l=layersMap[id]; if(l) l.setStyle({color:"black",fillColor:"#ff6666",fillOpacity:0.4}); }

    map.on(L.Draw.Event.CREATED,function(e){
        var layer = e.layer;
        var type = e.layerType;
        var id = L.stamp(layer);
        layersMap[id] = layer;

        if(type==="marker"){
            var blueIcon = L.icon({
                iconUrl:'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png',
                shadowUrl:'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
                iconSize:[25,41],
                iconAnchor:[12,41]
            });
            layer.setIcon(blueIcon);
            layer.on('click',function(){
                var c=layer.getLatLng();
                layer.bindPopup("Координати:<br>"+c.lat.toFixed(6)+", "+c.lng.toFixed(6)).openPopup();
            });
        } else {
            layer.setStyle({color:"black",fillColor:"yellow",fillOpacity:0.4});
            var popup = `<b>Тип зони:</b><br><br>
                <button onclick="setChemical(${id})">🟡 Хімічне</button><br><br>
                <button onclick="setRadiation(${id})">🔴 Радіація</button>`;
            layer.bindPopup(popup);
        }
        drawnItems.addLayer(layer);
    });

    // --- Текст на карті ---
    map.on('click',function(e){
        if(textMode){
            var t = prompt("Введіть текст:");
            if(t){
                var icon = L.divIcon({html:'<div style="background:white;padding:4px;border-radius:4px;">'+t+'</div>'});
                L.marker(e.latlng,{icon:icon}).addTo(map);
            }
        }
    });

    // --- Легенда ---
    var legend = L.control({position:'bottomleft'});
    legend.onAdd=function(){
        var d=L.DomUtil.create('div');
        d.style.background='white';
        d.style.padding='10px';
        d.innerHTML="<b>Легенда</b><br><br>";
        d.innerHTML+="<div style='background:yellow;width:20px;height:10px;display:inline-block'></div> Хімічне забруднення<br>";
        d.innerHTML+="<div style='background:#ff6666;width:20px;height:10px;display:inline-block'></div> Радіоактивне забруднення";
        return d;
    };
    legend.addTo(map);

    // --- Збереження карти ---
    window.saveMap = function(){
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
        var map = L.map('map').setView([48.3794,31.1656],6);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
        L.geoJSON(${JSON.stringify(data)}).addTo(map);
        <\/script>
        </body>
        </html>`;
        var blob = new Blob([html],{type:"text/html"});
        var a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download="rhb_map.html";
        a.click();
    };

}
</script>
"""
    components.html(map_html, height=760)

with col_right:
    st.markdown('<b style="color:#ffcc00;">МОДУЛЬ 3. Розрахунки</b>', unsafe_allow_html=True)
    st.link_button("Калькулятор дози опромінення", "https://sergsh1125-dotcom.github.io/radiation-calculator/")

st.sidebar.caption("ОФІС CBRN v4.2")
