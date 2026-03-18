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
    .block-container {padding:1rem !important; max-width:100% !important;}
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0e1117; color: #e0e0e0;}
    .main-title {color:#ffcc00; text-align:center; font-size:45px; font-weight:bold; margin-top:-30px; margin-bottom:15px; text-transform:uppercase;}
    .module-header {color:#ffcc00; border-bottom:1px solid #ffcc00; margin-top:10px; margin-bottom:8px; font-weight:bold; font-size:14px; text-transform:uppercase;}
    div[data-testid="stButton"] button, div[data-testid="stLinkButton"] a {background-color:#ffcc00; color:#000; border:none; width:100%; font-weight:bold; font-size:12px; border-radius:4px; padding:8px 12px; display:block; text-decoration:none; line-height:1.2;}
    div[data-testid="stButton"] button:hover, div[data-testid="stLinkButton"] a:hover {background-color:#e6b800;}
    .stExpander {background-color:#ffcc00; border:none; border-radius:4px;}
    .stExpander summary {color:#000; font-weight:bold;}
    .stExpander summary svg {fill:#000;}
    iframe {border:1px solid #3d444d; border-radius:8px;}
    </style>
""", unsafe_allow_html=True)

# --- 3. ЗАГОЛОВОК ---
st.markdown('<p class="main-title">Платформа підтримки прийняття рішення щодо реагування на РХБ інциденти</p>', unsafe_allow_html=True)

# --- 4. РОБОЧИЙ ПРОСТІР ---
col_left, col_center, col_right = st.columns([1.2, 4.6, 1.2])

with col_left:
    st.markdown('<p class="module-header">МОДУЛЬ 1. РХБ ОБСТАНОВКА</p>', unsafe_allow_html=True)
    st.link_button("1.1. Карта радіаційного моніторингу (SaveEcoBot)", "https://www.saveecobot.com/radiation-maps")
    st.link_button("1.2. Карта радіаційного моніторингу країн ЄС", "https://remap.jrc.ec.europa.eu/Advanced.aspx")
    st.link_button("1.3. Карта прогнозу хімічної обстановки", "http://forecast.inf.ua/")
    st.link_button("1.4. Карта фактичної радіаційної обстановки", "https://radiation-situation-mt5eyizylhpa7sxaltawpk.streamlit.app/")
    st.link_button("1.5. Карта фактичної хімічної обстановки", "https://chemical-map-6refroql3kghrhuh7tzdma.streamlit.app/")
    st.info("💡 Додавайте маркери на карту для позначок.")

    st.markdown('<p class="module-header">МОДУЛЬ 2. БАЗИ ДАНИХ</p>', unsafe_allow_html=True)
    st.link_button("2.1. Аварійні картки НХР", "https://sergsh1125-dotcom.github.io/emergency-cards/")
    st.link_button("2.2. Токсодози бойових ОР", "https://sergsh1125-dotcom.github.io/toxicdoze/")

with col_center:
    # --- КАРТА ПО ЦЕНТРУ ---
    map_html = """
    <div style="width:100%; display:flex; justify-content:center;">
        <div id="map" style="height:750px; width:calc(100% - 6px); max-width:1000px; border-radius:8px;"></div>
    </div>

    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.js"></script>

    <script>
    var map = L.map('map').setView([48.3794,31.1656],6);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap contributors'}).addTo(map);

    var drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);

    function setStyle(layer){layer.setStyle({color:'orange',fillColor:'orange',fillOpacity:0.4,weight:2});}

    var drawControl = new L.Control.Draw({
        draw:{polygon:true,rectangle:true,circle:true,polyline:true,marker:true},
        edit:{featureGroup:drawnItems}
    });
    map.addControl(drawControl);

    map.on(L.Draw.Event.CREATED,function(e){
        var layer = e.layer;
        var type = e.layerType;
        if(type==="marker"){
            var blueIcon = L.icon({
                iconUrl:"https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png",
                shadowUrl:"https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
                iconSize:[25,41],
                iconAnchor:[12,41]
            });
            layer.setIcon(blueIcon);
            layer.on('click',function(){
                var coords = layer.getLatLng().lat.toFixed(6)+", "+layer.getLatLng().lng.toFixed(6);
                layer.bindPopup("Координати:<br>"+coords).openPopup();
            });
        } else if(type==="circle"){
            setStyle(layer);
        } else {
            setStyle(layer);
        }
        drawnItems.addLayer(layer);
    });

    </script>
    """
    components.html(map_html, height=760)

    # --- КНОПКА ДОДАВАННЯ ТЕКСТУ ---
    st.button("Додати текст на карту")

    # --- КНОПКА ЗАВАНТАЖЕННЯ КАРТИ ---
    st.download_button("Завантажити карту у HTML", map_html, file_name="map.html", mime="text/html")

with col_right:
    st.markdown('<p class="module-header">МОДУЛЬ 3. РОЗРАХУНКИ</p>', unsafe_allow_html=True)
    st.link_button("3.1. Калькулятор дози опромінення при ядерному вибуху", "https://sergsh1125-dotcom.github.io/radiation-calculator/")
    st.link_button("3.2. Калькулятор дози опромінення при аварії на АЕС", "https://sergsh1125-dotcom.github.io/radiation-doza/")
    st.link_button("3.3. Калькулятор розрахунку часу перебування у зоні радіоактивного забруднення", "https://sergsh1125-dotcom.github.io/calculator-time/")

    st.markdown('<p class="module-header">МОДУЛЬ 4. ДОВІДКОВА ІНФОРМАЦІЯ</p>', unsafe_allow_html=True)
    st.link_button("4.1. Метеообстановка", "https://www.meteo.gov.ua/")

    with st.expander("📄 4.2. Методичні матеріали"):
        st.link_button("📜 Управління РХБ захисту ДСНС", "https://dsns.gov.ua/zakonodavstvo/perelik-normativno-pravovix-dokumentiv-shho-reglamentuyut-diyalnist-pidrozdiliv-dsns-ukrayini/upravlinnia-organizaciyi-radiaciinogo-ximicnogo-ta-biologicnogo-zaxistu")
        st.link_button("📚 Методичні рекомендації", "https://dsns.gov.ua/metodichni-rekomendaciyi")

st.sidebar.caption("ОФІС CBRN v3.9")
