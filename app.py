import streamlit as st
import streamlit.components.v1 as components

# --- 1. НАЛАШТУВАННЯ СТОРІНКИ ---
st.set_page_config(
    page_title="ОФІС CBRN",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. СТИЛІЗАЦІЯ (ОПТИМІЗАЦІЯ ПІД НОУТБУК) ---
st.markdown("""
    <style>
    /* Приховуємо службові елементи */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0e1117; color: #e0e0e0;}
    
    /* ГОЛОВНА НАЗВА (23px) */
    .main-title {
        color: #ffcc00 !important; 
        text-align: center !important; 
        font-size: 23px !important; 
        font-weight: bold !important; 
        margin-top: -75px !important; /* Піднімаємо вгору */
        margin-bottom: 15px !important;
        text-transform: uppercase !important;
    }
    
    /* НАЗВИ МОДУЛІВ (14px) */
    .module-header {
        color: #ffcc00 !important; 
        border-bottom: 1px solid #ffcc00 !important; 
        margin-top: 12px !important; 
        margin-bottom: 8px !important; 
        font-weight: bold !important; 
        font-size: 14px !important; 
        text-transform: uppercase !important;
    }

    /* КНОПКИ (13px) */
    div.stButton > button, a.stLinkButton {
        background-color: #1b1e23 !important; 
        color: #ffffff !important;
        border: 1px solid #3d444d !important; 
        border-radius: 4px !important;
        padding: 5px 10px !important; 
        width: 100% !important; 
        text-align: left !important; 
        font-size: 13px !important;
        margin-bottom: 4px !important;
        transition: 0.2s;
    }
    
    div.stButton > button:hover, a.stLinkButton:hover {
        border-color: #ffcc00 !important; 
        color: #ffcc00 !important;
        background-color: #262a33 !important;
    }

    /* Прибираємо відступи у колонок */
    [data-testid="column"] {
        padding: 0px 5px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. ЗАГОЛОВОК ---
st.markdown('<p class="main-title">ПЛАТФОРМА ПІДТРИМКИ РХБ ЗАХИСТУ</p>', unsafe_allow_html=True)

# --- 4. РОБОЧИЙ ПРОСТІР (Широка карта 5.5) ---
col_left, col_center, col_right = st.columns([0.7, 5.5, 0.7])

with col_left:
    st.markdown('<p class="module-header">МОДУЛЬ 1. РХБ ОБСТАНОВКА</p>', unsafe_allow_html=True)
    st.link_button("1.1. Карта моніторингу", "https://www.saveecobot.com/radiation-maps")
    st.link_button("1.2. Карта прогнозу", "http://forecast.inf.ua/")
    st.link_button("1.3. Карта факт. рад.", "https://sergsh1125-dotcom-radiation-situation-app-vlg9fu.streamlit.app/")
    st.link_button("1.4. Карта факт. хім.", "https://sergsh1125-dotcom-chemical-map-app-rhopcd.streamlit.app/")
    
    st.markdown('<p class="module-header">МОДУЛЬ 2. БАЗИ ДАНИХ</p>', unsafe_allow_html=True)
    st.link_button("2.1. Аварійні картки НХР", "https://sergsh1125-dotcom.github.io/emergency-cards/")
    st.link_button("2.2. Токсодози ОР", "https://sergsh1125-dotcom.github.io/toxicdoze/")

with col_center:
    # Оперативна карта (максимально розширена)
    components.iframe("http://googleusercontent.com/maps.google.com/5", height=780)

with col_right:
    st.markdown('<p class="module-header">МОДУЛЬ 3. РОЗРАХУНКИ</p>', unsafe_allow_html=True)
    st.link_button("3.1. Калькулятор дози опромінення - при ядерному вибуху", "https://sergsh1125-dotcom.github.io/radiation-calculator/")
    st.link_button("3.2. Час перебування", "https://sergsh1125-dotcom.github.io/calculator-time/")
    
    st.markdown('<p class="module-header">МОДУЛЬ 4. ДОВІДКА</p>', unsafe_allow_html=True)
    st.link_button("4.1. Метеообстановка", "https://www.meteo.gov.ua/")
    
    with st.expander("📄 4.2. СОП ТА НПА"):
        st.link_button("📜 Сайт ДСНС", "https://dsns.gov.ua/")
        st.link_button("⚖️ Сайт ВРУ", "https://zakon.rada.gov.ua/")

# Порожній сайдбар (щоб не заважав)
st.sidebar.markdown("---")
st.sidebar.caption("ОФІС CBRN v3.0")
