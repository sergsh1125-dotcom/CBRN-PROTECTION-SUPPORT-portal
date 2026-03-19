import streamlit as st
import streamlit.components.v1 as components

# --- 1. НАЛАШТУВАННЯ СТОРІНКИ ---
st.set_page_config(
    page_title="ОФІС CBRN",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. СТИЛІЗАЦІЯ ТА ПРИХОВУВАННЯ СЛУЖБОВИХ ЕЛЕМЕНТІВ ---
st.markdown("""
<style>
/* Повне приховування службових меню Streamlit */
#MainMenu, footer, header, .stDeployButton {visibility: hidden; display: none !important;}

.block-container {padding:1rem !important; max-width:100% !important;}
.stApp {background-color:#0e1117; color:#e0e0e0;}

/* НАЗВА ПОРТАЛУ */
.main-title {
    color:#ffcc00 !important;
    text-align:center !important;
    font-size:25px !important;
    font-weight:bold !important;
    margin-top:-30px !important;
    margin-bottom:15px !important;
    text-transform:uppercase !important;
}

/* ЗАГОЛОВКИ МОДУЛІВ */
.module-header {
    color:#ffcc00 !important;
    border-bottom:1px solid #ffcc00 !important;
    margin-top:10px !important;
    margin-bottom:8px !important;
    font-weight:bold !important;
    font-size:20px !important;
    text-transform:uppercase !important;
}

/* УНІФІКОВАНІ ЖОВТІ КНОПКИ ТА ПОСИЛАННЯ */
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

/* ЕКСПАНДЕР (ЖОВТИЙ) */
.stExpander {
    background-color:#ffcc00 !important;
    border:none !important;
    border-radius:4px !important;
}
.stExpander summary { color:#000 !important; font-weight:bold !important; }
.stExpander summary svg { fill:#000 !important; }

/* Стилізація радіокнопок для вибору маркера */
div[data-testid="stRadio"] > label { color:#ffcc00 !important; font-weight:bold !important; }
div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p { color:white !important; }

/* Приховування кнопок при друку */
@media print {
    .stColumn:first-child, .stColumn:last-child, button, .main-title, .module-header, div[data-testid="stRadio"] {
        display: none !important;
    }
    .block-container { padding: 0 !important; }
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">Платформа підтримки прийняття рішення щодо реагування на РХБ інциденти</p>', unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1.3, 4.4, 1.3])

# -------- ЛІВА ПАНЕЛЬ --------
with col_left:
    st.markdown('<p class="module-header">МОДУЛЬ 1. РХБ ОБСТАНОВКА</p>', unsafe_allow_html=True)
    st.link_button("1.1. Карта радіаційного моніторингу (SaveEcoBot)", "https://www.saveecobot.com/radiation-maps")
    st.link_button("1.2. Карта радіаційного моніторингу країн ЄС", "https://remap.jrc.ec.europa.eu/Advanced.aspx")
    st.link_button("1.3. Карта прогнозу хімічної обстановки", "http://forecast.inf.ua/")
    st.link_button("1.4. Карта фактичної радіаційної обстановки", "https://radiation-situation-mt5eyizylhpa7sxaltawpk.streamlit.app/")
    st.link_button("1.5. Карта фактичної хімічної обстановки", "https://chemical-map-6refroql3kghrhuh7tzdma.streamlit.app/")

    st.info("💡 На картах 1.4; 1.5 координати завантажуються кліком мишки.")
    
    # Нові інструкції
    st.success("💡 **Нові інструменти карти:** Оберіть тип маркера (праворуч), використовуйте `Marker` для точок та `Forecast Circle` для прогнозу (без заповнення).")

    st.markdown('<p class="module-header">МОДУЛЬ 2. БАЗИ ДАНИХ</p>', unsafe_allow_html=True)
    st.link_button("2.1. Аварійні картки НХР", "https://sergsh1125-dotcom.github.io/emergency-cards/")
    st.link_button("2.2. Токсодози бойових ОР", "https://sergsh1125-dotcom.github.io/toxicdoze/")

# -------- ЦЕНТР (РОБОЧА КАРТА) --------
with col_center:
    # Окремий блок для вибору типу маркера, який буде передано в JS
    marker_type = st.radio(
        "Оберіть тип маркера для нанесення:",
        ("Точка вимірювання (Синя)", "Знак радіації (Фіксований)"),
        horizontal=True
    )
    # Конвертація вибору в зрозумілий для JS формат
    js_marker_type = 'measurement' if marker_type == "Точка вимірювання (Синя)" else 'radiation'

    map_html = f"""
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.css"/>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/leaflet.draw.js"></script>
<script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>

<div id="capture_area" style="background:#0e1117; padding:5px; border-radius:8px;">
    <div id="map" style="height:650px; width:100%; border-radius:8px;"></div>
</div>

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 5px; margin-top: 10px;">
    <button onclick="addText()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer; font-size:11px;">ВСТАВИТИ ТЕКСТ</button>
    <button onclick="clearMap()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer; font-size:11px;">ОЧИСТИТИ КАРТУ</button>
    <button onclick="downloadPNG()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer; font-size:11px;">ЕКСПОРТ PNG</button>
    <button onclick="window.print()" style="padding:10px; background:#ffcc00; color:black; border:none; border-radius:4px; font-weight:bold; cursor:pointer; font-size:11px;">ДРУК / PDF</button>
</div>

<script>
// Змінна, що отримує тип маркера зі Streamlit
var currentMarkerType = '{js_marker_type}';

//preferCanvas: true вирішує проблему зміщення фігур при експорті
var map = L.map('map',{{attributionControl:false, preferCanvas: true}}).setView([48.3794,31.1656],6);

L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{
    crossOrigin: 'anonymous'
}}).addTo(map);

var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

// --- ДЕФІНІЦІЯ КАСТОМНИХ ІКОНОК ---

// 1. Знак радіації (Жовте коло, чорний ободок, фіксований розмір)
// Вставляємо стандартний знак радіації через HTML/SVG
var radiationIcon = L.divIcon({{
    html: '<div style="background:#ffcc00; border:2px solid black; border-radius:50%; width:30px; height:30px; display:flex; align-items:center; justify-content:center; color:black; font-size:18px; font-weight:bold;">☢️</div>',
    className: 'custom-radiation-icon',
    iconSize: [30, 30],
    iconAnchor: [15, 15] // Центр іконки
}});

// 2. Синя крапка вимірювання (Фіксований розмір)
var bluePointIcon = L.divIcon({{
    html: '<div style="background:#007bff; border:2px solid black; border-radius:50%; width:12px; height:12px;"></div>',
    className: 'custom-measurement-icon',
    iconSize: [12, 12],
    iconAnchor: [6, 6] // Центр іконки
}});

// --- ПАНЕЛЬ МАЛЮВАННЯ (Оновлена) ---
var drawControl = new L.Control.Draw({{
    draw:{{
        polygon:true,
        rectangle:true,
        polyline:true,
        circle:false, // Стандартне коло вимикаємо
        marker:{{
            icon: radiationIcon // Дефолтна іконка
        }},
        // Додаємо власні інструменти для прогнозного кола
        circlemarker: {{
            fillOpacity: 0, // Без заповнення (Прогноз)
            color: 'black',
            weight: 2,
            radius: 20, // Початковий радіус
            className: 'forecast-circle'
        }}
    }},
    edit:{{ featureGroup: drawnItems }}
}});
map.addControl(drawControl);

// Оновлюємо іконку маркера при старті на основі вибору користувача
if(currentMarkerType === 'measurement') {{
    drawControl.setDrawingOptions({{ marker: {{ icon: bluePointIcon }} }});
}} else {{
    drawControl.setDrawingOptions({{ marker: {{ icon: radiationIcon }} }});
}}

// Оновлення типу маркера при зміні вибору у Streamlit
window.parent.document.addEventListener('streamlit:radio:changed', function(e) {{
    // Streamlit не передає дані напряму в JS при зміні, 
    // тому цей метод для демонстрації, реальне оновлення відбувається при перезавантаженні фрейму.
    // Оскільки Streamlit перезавантажує компоненти, 
    // тип маркера буде оновлено автоматично при старті.
}});

map.on(L.Draw.Event.CREATED, function(e){{
    var layer = e.layer;
    var type = e.layerType;

    if(type === "marker") {{
        // Додаємо кастомну властивість, щоб знати тип при експорті
        if(currentMarkerType === 'measurement') {{
            layer.setIcon(bluePointIcon);
            layer.options.isMeasurementPoint = true; 
        }} else {{
            layer.setIcon(radiationIcon);
            layer.options.isRadiationSign = true;
        }}
    }} else if(type === "circlemarker") {{
        // Це наше прогнозний круг
        layer.setStyle({{fillOpacity: 0, color: 'black', weight: 2}});
        layer.options.isForecastCircle = true;
    }} else {{
        // Всі інші фігури (полігони, прямокутники) - жовте заповнення
        layer.setStyle({{color:'black', fillColor:'yellow', fillOpacity:0.5, weight:2}});
    }}
    drawnItems.addLayer(layer);
}});

function addText(){{
    var text = prompt("Введіть текст:");
    if(text){{
        map.once('click', function(e){{
            var icon = L.divIcon({{
                html:'<div style="background:rgba(255,255,255,0.8); padding:2px 5px; border:1px solid black; border-radius:3px; font-weight:bold; color:black; white-space:nowrap;">'+text+'</div>',
                iconSize: null
            });
            L.marker(e.latlng,{{icon:icon}}).addTo(drawnItems);
        });
    }}
}}

function clearMap() {{
    if(confirm("Очистити всі нанесені дані?")) {{
        drawnItems.clearLayers();
    }}
}}

function downloadPNG(){{
    const area = document.getElementById("capture_area");
    setTimeout(() => {{
        html2canvas(area, {{
            useCORS: true,
            allowTaint: false,
            backgroundColor: "#0e1117",
            scale: 2
        }}).then(function(canvas){{
            var link = document.createElement("a");
            link.download = "CBRN_Report_Map_v3.18.png";
            link.href = canvas.toDataURL("image/png");
            link.click();
        }});
    }}, 150);
}}
</script>
"""
    components.html(map_html, height=800)

# -------- ПРАВА ПАНЕЛЬ --------
with col_right:
    st.markdown('<p class="module-header">МОДУЛЬ 3. РОЗРАХУНКИ</p>', unsafe_allow_html=True)
    st.link_button("3.1. Калькулятор дози при ядерному вибуху", "https://sergsh1125-dotcom.github.io/radiation-calculator/")
    st.link_button("3.2. Калькулятор дози при аварії на АЕС", "https://sergsh1125-dotcom.github.io/radiation-doza/")
    st.link_button("3.3. Розрахунок часу перебування у зоні", "https://sergsh1125-dotcom.github.io/calculator-time/")

    st.markdown('<p class="module-header">МОДУЛЬ 4. ДОВІДКА</p>', unsafe_allow_html=True)
    st.link_button("4.1. Метеообстановка", "https://www.meteo.gov.ua/")

    with st.expander("📄 4.2. Методичні матеріали"):
        st.link_button("📜 Управління РХБ захисту ДСНС", "https://dsns.gov.ua/")
        st.link_button("📚 Методичні рекомендації", "https://dsns.gov.ua/metodichni-rekomendaciyi")

st.sidebar.caption("ОФІС CBRN v3.18")
