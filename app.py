import streamlit as st
import streamlit.components.v1 as components
import os

# --- 1. НАЛАШТУВАННЯ СТОРІНКИ ---
st.set_page_config(
    page_title="ОФІС CBRN",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ГЛОБАЛЬНІ СТИЛІ (CSS) ---
st.markdown("""
<style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden; display: none !important;}
    .block-container {padding:1rem !important; max-width:100% !important; padding-top: 1.5rem !important;}
    .stApp {background-color:#0e1117; color:#e0e0e0;}

    .main-title {
        color:#ffcc00 !important;
        text-align:center !important;
        font-size:25px !important;
        font-weight:bold !important;
        margin-top:-20px !important;
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

    div.stLinkButton > a {
        background-color:#ffcc00 !important;
        color:#000 !important;
        border:none !important;
        width:100% !important;
        font-weight:bold !important;
        font-size:12px !important;
        border-radius:4px !important;
        padding:8px 12px !important;
        display:flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        text-decoration: none !important;
        white-space: pre-wrap !important;
        height: auto !important;
        min-height: 3em !important;
        line-height: 1.2 !important;
    }

    div.stExpander {
        background-color: transparent !important;
        border: 1px solid #ffcc00 !important;
        border-radius:4px !important;
    }
    div.stExpander summary { color:#ffcc00 !important; font-weight:bold !important; }

    @media print {
        .stColumn:first-child, .stColumn:last-child, button, .main-title, .module-header {
            display: none !important;
        }
    }

    div[data-testid="stDownloadButton"] > button {
        background-color:#ffcc00 !important;
        color:black !important;
        border:none !important;
        width:100% !important;
        font-weight:bold !important;
        font-size:11px !important;
        border-radius:4px !important;
        padding:8px 10px !important;
        margin-bottom:5px !important;
    }

    div[data-testid="stDownloadButton"] > button:hover {
        background-color:#ffd633 !important;
        color:black !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">Платформа підтримки заходів реагування на ХБРЯ інциденти</p>', unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1.3, 4.4, 1.3])

# -------- ЛІВА ПАНЕЛЬ --------
with col_left:
    st.markdown('<p class="module-header">МОДУЛЬ 1. РХБ ОБСТАНОВКА</p>', unsafe_allow_html=True)
    st.link_button("1.1. Карта радіаційного моніторингу (SaveEcoBot)", "https://www.saveecobot.com/radiation-maps")
    st.link_button("1.2. Карта Укргідромету", "https://www.meteo.gov.ua/#RADIO")
    st.link_button("1.3. Карта ЄС", "https://remap.jrc.ec.europa.eu/Advanced.aspx")
    st.link_button("1.4. Прогноз хімічної обстановки", "http://forecast.inf.ua/")
    st.link_button("1.5. Фактична РХ обстановка", "https://map-obstanovka-vuvukyx4vwu9jrhuv68vcg.streamlit.app/")

    st.markdown('<p class="module-header">МОДУЛЬ 2. БАЗИ ДАНИХ</p>', unsafe_allow_html=True)
    st.link_button("2.1. Аварійні картки НХР", "https://sergsh1125-dotcom.github.io/emergency-cards/")
    st.link_button("2.2. Токсодози", "https://sergsh1125-dotcom.github.io/toxicdoze/")

# -------- ЦЕНТР (КАРТА) --------
with col_center:
    map_html = """
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css"/>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.js"></script>
    <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>

    <div id="capture_area" style="background:#0e1117; padding:5px;">
        <div id="map" style="height:650px;"></div>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:5px;margin-top:10px;">
        <button onclick="addText()">ТЕКСТ</button>
        <button onclick="clearMap()">ОЧИСТИТИ</button>
        <button onclick="downloadPNG()">PNG</button>
        <button onclick="window.print()">PDF</button>
    </div>

    <script>
    var map = L.map('map').setView([48.3794,31.1656],6);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    var drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);

    map.on(L.Draw.Event.CREATED, function(e){
        drawnItems.addLayer(e.layer);
    });

    function addText(){
        var text = prompt("Текст:");
        if(text){
            map.once('click', function(e){
                L.marker(e.latlng).addTo(drawnItems)
                    .bindTooltip(text,{permanent:true});
            });
        }
    }

    function clearMap(){ drawnItems.clearLayers(); }

    function downloadPNG(){
        html2canvas(document.getElementById("capture_area")).then(canvas=>{
            var a=document.createElement("a");
            a.download="map.png";
            a.href=canvas.toDataURL();
            a.click();
        });
    }
    </script>
    """
    components.html(map_html, height=750)

# -------- ПРАВА ПАНЕЛЬ --------
with col_right:

    with st.expander("🌤️ ВІТЕР", expanded=False):
        components.html("""
        <iframe width="100%" height="300"
        src="https://embed.windy.com/embed2.html?lat=49.0&lon=31.0&zoom=5&level=surface&overlay=wind&product=ecmwf"
        frameborder="0"></iframe>
        """, height=310)

    st.markdown('<p class="module-header">МОДУЛЬ 3</p>', unsafe_allow_html=True)
    st.link_button("3.1 Доза ядерна", "https://sergsh1125-dotcom.github.io/radiation-calculator/")
    st.link_button("3.2 Доза АЕС", "https://sergsh1125-dotcom.github.io/radiation-doza/")
    st.link_button("3.3 Час опромінення", "https://sergsh1125-dotcom.github.io/calculator-time/")

    st.markdown('<p class="module-header">МОДУЛЬ 4</p>', unsafe_allow_html=True)
    st.link_button("4.1 Укргідромет", "https://www.meteo.gov.ua/")

    DOCS_FOLDER = "docs"

    with st.expander("4.4 ДОКУМЕНТИ", expanded=False):

        if os.path.isdir(DOCS_FOLDER):
            files = [f for f in os.listdir(DOCS_FOLDER) if f.endswith((".pdf",".docx",".xlsx",".csv",".txt",".pptx"))]

            if files:
                for f in files:
                    path = os.path.join(DOCS_FOLDER, f)
                    with open(path,"rb") as file:
                        st.download_button(f"📄 {f}", file, file_name=f)
            else:
                st.warning("Папка порожня")
        else:
            st.error("docs не знайдено")
