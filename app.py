import streamlit as st
import streamlit.components.v1 as components

# --- 1. НАЛАШТУВАННЯ СТОРІНКИ ---
st.set_page_config(
    page_title="ОФІС CBRN",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. СТИЛІЗАЦІЯ (МАКСИМАЛЬНЕ РОЗШИРЕННЯ ТА КОРЕКЦІЯ ШРИФТІВ) ---
st.markdown("""
    <style>
    /* ПРИБИРАЄМО ПУСТІ ПОЛЯ ПО КРАЯХ (2 СМ) */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0e1117; color: #e0e0e0;}
    
    /* ГОЛОВНА НАЗВА (23px) */
    .main-title {
        color: #ffcc00 !important; 
        text-align: center !important; 
        font-size: 23px !important; 
        font-weight: bold !important; 
        margin-top: -30px !important; 
        margin-bottom: 10px !important;
        text-transform: uppercase !important;
    }
    
    /* НАЗВИ МОДУЛІВ (14px) */
    .module-header {
        color: #ffcc00 !important; 
        border-bottom: 1px solid #ffcc00 !important; 
        margin-top: 10px !important; 
        margin-bottom: 8px !important; 
        font-weight: bold !important; 
        font-size: 14px !important; 
        text-transform: uppercase !important;
    }

    /* КНОПКИ ПІДМОДУЛІВ (12px + розширення) */
    div.stButton > button, a.stLinkButton {
        background-color: #1b1e23 !important; 
        color: #ffffff !important;
        border: 1px solid #3d444d !important; 
        border-radius: 4px !important;
        padding: 8px 12px !important; 
        width: 100% !important; 
        text-align: left !important; 
        font-size: 12px !important; /* Розмір за запитом */
        font-weight: 500 !important;
        margin-bottom: 5px !important;
        display: block !important;
    }
    
    div.stButton > button:hover, a.stLinkButton:hover {
        border-color: #ffcc00 !important; 
        color: #ffcc00 !important;
    }

    /* Стиль для фрейму карти */
    iframe {
        border: 1px solid #3d444d !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. ЗАГОЛОВОК ---
st.markdown('<p class="main-title">ПЛАТФОРМА ПІДТРИМКИ РХБ ЗАХИСТУ</p>', unsafe_allow_html=True)

# --- 4. РОБОЧИЙ ПРОСТІР ---
# Збільшуємо частку бокових колонок, щоб кнопки були ширшими (1.2 замість 0.7)
col_left, col_center, col_right = st.columns([1.2, 4.6, 1.2])

with col_left:
    st.markdown('<p class="module-header">МОДУЛЬ 1. РХБ ОБСТАНОВКА</p>', unsafe_allow_html=True)
    st.link_button("1.1. Карта моніторингу (SaveEcoBot)", "https://www.saveecobot.com/radiation-maps")
    st.link_button("1.2. Карта прогнозу хім. обстановки", "http://forecast.inf.ua/")
    st.link_button("1.3. Карта фактичної рад. обстановки", "https://sergsh1125-dotcom-radiation-situation-app-vlg9fu.streamlit.app/")
    st.link_button("1.4. Карта фактичної хім. обстановки", "https://sergsh1125-dotcom-chemical-map-app-rhopcd.streamlit.app/")
    
    st.markdown('<p class="module-header">МОДУЛЬ 2. БАЗИ ДАНИХ</p>', unsafe_allow_html=True)
    st.link_button("2.1. Аварійні картки НХР", "https://sergsh1125-dotcom.github.io/emergency-cards/")
    st.link_button("2.2. Токсодози бойових ОР", "https://sergsh1125-dotcom.github.io/toxicdoze/")

with col_center:
    # ПРАВИЛЬНА КАРТА GOOGLE (Локалізація UA)
    # Використовуємо надійне посилання для вбудовування
    google_maps_url = "https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d2000000!2d31.16558!3d48.379433!5m2!1suk!2sua"
    components.iframe(google_maps_url, height=750)

with col_right:
    st.markdown('<p class="module-header">МОДУЛЬ 3. РОЗРАХУНКИ</p>', unsafe_allow_html=True)
    st.link_button("3.1. Калькулятор дози опромінення - при ядерному вибуху", "https://sergsh1125-dotcom.github.io/radiation-calculator/")
    st.link_button("3.2. Калькулятор часу перебування", "https://sergsh1125-dotcom.github.io/calculator-time/")
    
    st.markdown('<p class="module-header">МОДУЛЬ 4. ДОВІДКОВА ІНФОРМАЦІЯ</p>', unsafe_allow_html=True)
    st.link_button("4.1. Метеообстановка", "https://www.meteo.gov.ua/")
    
    with st.expander("📄 4.2. СОП ТА НПА"):
        st.link_button("📜 Сайт ДСНС України", "https://dsns.gov.ua/")
        st.link_button("⚖️ Сайт Верховної Ради України", "https://zakon.rada.gov.ua/")

# Сайдбар (технічний мінімум)
st.sidebar.caption("ОФІС CBRN v3.1")
