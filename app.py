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

.stExpander {
    background-color:#ffcc00 !important;
    border:none !important;
    border-radius:4px !important;
}
.stExpander summary { color:#000 !important; font-weight:bold !important; }
.stExpander summary svg { fill:#000 !important; }

@media print {
    .stColumn:first-child, .stColumn:last-child, button, .main-title, .module-header {
        display: none !important;
    }
    .block-container { padding: 0 !important; }
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">Платформа підтримки заходів реагування на ХБРЯ інциденти</p>', unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1.3, 4.4, 1.3])

# -------- ЛІВА ПАНЕЛЬ --------
with col_left:
    st.markdown('<p class="module-header">МОДУЛЬ 1. РХБ ОБСТАНОВКА</p>', unsafe_allow_html=True)
    st.link_button("1.1. Карта радіаційного моніторингу (SaveEcoBot)", "https://www.saveecobot.com/radiation-maps")
    st.link_button("1.2. Карта радіаційного моніторингу країн ЄС", "https://remap.jrc.ec.europa.eu/Advanced.aspx")
    st.link_button("1.3. Карта прогнозу хімічної обстановки", "http://forecast.inf.ua/")
    st.link_button("1.4. Карта фактичної радіаційної обстановки", "https://radiation-situation-mt5eyizylhpa7sxaltawpk.streamlit.app/")
    st.link_button("1.5. Карта фактичної хімічної обстановки", "https://chemical-map-dgtnhrsz7azy3epkzid2g2.streamlit.app/")
    st.link_button("1.6. Карта фактичної радіаційної та хімічної обстановки","https://map-obstanovka-vuvukyx4vwu9jrhuv68vcg.streamlit.app/")
    st.info("💡 На картах 1.4; 1.5; 1.6 координати завантажуються кліком мишки.")

    st.markdown('<p class="module-header">МОДУЛЬ 2. БАЗИ ДАНИХ</p>', unsafe_allow_html=True)
    st.link_button("2.1. Аварійні картки НХР", "https://sergsh1125-dotcom.github.io/emergency-cards/")
    st.link_button("2.2. Токсодози бойових ОР", "https://sergsh1125-dotcom.github.io/toxicdoze/")

# -------- ЦЕНТР (РОБОЧА КАРТА) --------
with col_center:
    map_html = """
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css"/>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.js"></script>
<script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>

<div id="capture_area" style="background:#0e1117; padding:5px; border-radius:8px;">
    <div id="map" style="height:680px; width:100%; border-radius:8px;"></div>
</div>

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 5px; margin-top: 10px;">
    <button onclick="addText()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer; font-size:11px;">ВСТАВИТИ ТЕКСТ</button>
    <button onclick="clearMap()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer; font-size:11px;">ОЧИСТИТИ КАРТУ</button>
    <button onclick="downloadPNG()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer; font-size:11px;">ЕКСПОРТ PNG</button>
    <button onclick="window.print()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer; font-size:11px;">ДРУК / PDF</button>
</div>

<script>
var map = L.map('map',{attributionControl:false, preferCanvas: true}).setView([48.3794,31.1656],6);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
    crossOrigin: 'anonymous'
}).addTo(map);

var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

// 1. ІКОНКА РАДІАЦІЇ (для кнопки Marker)
var radIcon = L.divIcon({
    html: '<div style="background:#ffcc00; border:2px solid black; border-radius:50%; width:24px; height:24px; display:flex; align-items:center; justify-content:center; font-size:16px; color:black;">☢️</div>',
    className: '',
    iconSize: [24, 24],
    iconAnchor: [12, 12]
});

// 2. СТИЛЬ ЖОВТОЇ ТОЧКИ (для кнопки CircleMarker)
var yellowCircleStyle = {
    color: 'black',
    fillColor: 'yellow',
    fillOpacity: 0.9,
    weight: 2,
    radius: 8  // Фіксований розмір
};

// НАЛАШТУВАННЯ ПАНЕЛІ
var drawControl = new L.Control.Draw({
    draw:{ 
        polygon: { shapeOptions: { color: 'black', fillColor: 'yellow', fillOpacity: 0.5, weight: 2 } },
        rectangle: { shapeOptions: { color: 'black', fillColor: 'yellow', fillOpacity: 0.5, weight: 2 } },
        circle: { shapeOptions: { color: 'black', fillColor: 'yellow', fillOpacity: 0.5, weight: 2 } },
        polyline: { shapeOptions: { color: 'black', weight: 3 } },
        // ПЕРША КНОПКА (Маркер) -> Радіація
        marker: { icon: radIcon },
        // ДРУГА КНОПКА (Коло-маркер) -> Жовта точка
        circlemarker: yellowCircleStyle 
    },
    edit:{ featureGroup: drawnItems }
});
map.addControl(drawControl);

map.on(L.Draw.Event.CREATED, function(e){
    var layer = e.layer;
    var type = e.layerType;

    if (type === 'marker') {
        layer.setIcon(radIcon);
    } else if (type === 'circlemarker') {
        layer.setStyle(yellowCircleStyle);
    } else {
        layer.setStyle({color:'black', fillColor:'yellow', fillOpacity:0.5, weight:2});
    }

    drawnItems.addLayer(layer);
    
    // Автоматичне завершення операції (щоб не малювало серією)
    drawControl._toolbars.draw._modes[type].handler.disable();
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

function clearMap() {
    if(confirm("Очистити всі нанесені дані?")) {
        drawnItems.clearLayers();
    }
}

function downloadPNG(){
    const area = document.getElementById("capture_area");
    // Фіксація координат для PNG без зміщення
    html2canvas(area, {
        useCORS: true,
        allowTaint: false,
        backgroundColor: "#0e1117",
        scale: 2,
        scrollX: 0,
        scrollY: -window.scrollY,
        windowWidth: document.documentElement.offsetWidth,
        windowHeight: document.documentElement.offsetHeight
    }).then(function(canvas){
        var link = document.createElement("a");
        link.download = "CBRN_Report_Map.png";
        link.href = canvas.toDataURL("image/png");
        link.click();
    });
}
</script>
"""
    components.html(map_html, height=780)

# -------- ПРАВА ПАНЕЛЬ --------
with col_right:
    st.markdown('<p class="module-header">МОДУЛЬ 3. РОЗРАХУНКИ</p>', unsafe_allow_html=True)
    st.link_button("3.1. Калькулятор дози при ядерному вибуху", "https://sergsh1125-dotcom.github.io/radiation-calculator/")
    st.link_button("3.2. Калькулятор дози при аварії на АЕС", "https://sergsh1125-dotcom.github.io/radiation-doza/")
    st.link_button("3.3. Розрахунок часу перебування у зоні", "https://sergsh1125-dotcom.github.io/calculator-time/")
    st.markdown('<p class="module-header">МОДУЛЬ 4. ДОВІДКОВА ІНФОРМАЦІЯ</p>', unsafe_allow_html=True)
    st.link_button("4.1. Укргідрометеоцентр", "https://www.meteo.gov.ua/")
    st.link_button("4.2. Карти Windy","https://www.windy.com/?47.446,30.223,6") 
    with st.expander("📚 4.3. Методичні матеріали"):
        st.info("Нормативно-правова база та СОП (стандартні операційні процедури)")
    
        st.link_button(
        "🌐 Управління РХБ захисту ДСНС", 
        "https://dsns.gov.ua/zakonodavstvo/perelik-normativno-pravovix-dokumentiv-shho-reglamentuyut-diyalnist-pidrozdiliv-dsns-ukrayini/upravlinnia-organizaciyi-radiaciinogo-ximicnogo-ta-biologicnogo-zaxistu",
        use_container_width=True
        )
    
        st.link_button(
        "📖 Методичні рекомендації", 
        "https://dsns.gov.ua/metodichni-rekomendaciyi",
        use_container_width=True
        )
    
        st.link_button(
        "🧪 СОП 1.1/РХБЗ: Демеркуризація (Ртуть)", 
        "https://kyiv.dsns.gov.ua/upload/2/5/3/3/4/4/3/sop-demerkurizaciia-11-rxbz-dsns.pdf",
        use_container_width=True
        )
    
    # Виправлено посилання (прибрано зайву дужку в кінці)
        st.link_button(
        "⚠️ СОП 1.2/РХБЗ: Дії при НС з НХР", 
        "https://kyiv.dsns.gov.ua/upload/2/5/3/3/4/4/4/sop-poriadok-dii-12-rxbz-dsns.pdf",
        use_container_width=True
        )
