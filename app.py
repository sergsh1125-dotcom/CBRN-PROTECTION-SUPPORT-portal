import streamlit as st
import streamlit.components.v1 as components

# --- 1. НАЛАШТУВАННЯ СТОРІНКИ ТА ІКОНКИ ---
# Замініть YOUR_REPO на вашу назву репозиторію
ICON_URL = "https://raw.githubusercontent.com/sergsh1125-dotcom/YOUR_REPO/main/icon.png"

st.set_page_config(
    page_title="ДСНС - ОФІС CBRN",
    page_icon=ICON_URL,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ПЕРЕВІРКА ПАРОЛЯ (ЗБЕРЕЖЕННЯ СЕСІЇ) ---
def check_password():
    """Повертає True, якщо пароль вірний. Стан зберігається в сесії."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    # Екран входу
    st.markdown("""
        <style>
        .login-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-top: 10%;
            padding: 40px;
            background-color: #1b1e23;
            border: 2px solid #ffcc00;
            border-radius: 15px;
            width: 350px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.image(ICON_URL, width=100)
        st.markdown('<h2 style="color:#ffcc00; text-align:center;">CBRN OFFICE</h2>', unsafe_allow_html=True)
        password = st.text_input("Введіть код доступу:", type="password")
        if st.button("УВІЙТИ"):
            if password == "1125":  # ВАШ ПАРОЛЬ
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Доступ обмежено")
        st.markdown('</div>', unsafe_allow_html=True)
    return False

if not check_password():
    st.stop()

# --- 3. СТИЛІЗАЦІЯ ІНТЕРФЕЙСУ (ПІСЛЯ ВХОДУ) ---
st.markdown(f"""
    <head>
        <link rel="apple-touch-icon" href="{ICON_URL}">
        <link rel="icon" href="{ICON_URL}" type="image/png">
        <meta name="apple-mobile-web-app-capable" content="yes">
    </head>
    <style>
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stApp {{background-color: #0e1117; color: #e0e0e0;}}
    
    .main-title {{color: #ffcc00; text-align: center; font-size: 26px; font-weight: bold; margin-bottom: 0px;}}
    .sub-title {{color: #ffcc00; text-align: center; font-size: 20px; margin-bottom: 20px; font-weight: 400;}}
    
    .module-header {{
        color: #ffcc00; 
        border-bottom: 1px solid #3d444d; 
        margin-top: 15px; 
        margin-bottom: 10px; 
        font-weight: bold; 
        font-size: 14px; 
        text-transform: uppercase;
    }}

    div.stButton > button, a.stLinkButton {{
        background-color: #1b1e23 !important; 
        color: #e0e0e0 !important;
        border: 1px solid #3d444d !important; 
        border-radius: 4px !important;
        padding: 8px !important;
        width: 100% !important; 
        text-align: left !important;
        font-size: 13px !important;
        margin-bottom: 5px !important;
    }}
    
    div.stButton > button:hover, a.stLinkButton:hover {{
        border-color: #ffcc00 !important; 
        color: #ffcc00 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. ШАПКА ПОРТАЛУ ---
st.markdown('<p class="main-title">ПЛАТФОРМА ПІДТРИМКИ РХБ ЗАХИСТУ</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">ДСНС - ОФІС CBRN</p>', unsafe_allow_html=True)

# --- 5. ОСНОВНИЙ РОБОЧИЙ ПРОСТІР ---
col_left, col_center, col_right = st.columns([1.2, 3, 1.2])

# ЛІВА КОЛОНКА
with col_left:
    st.markdown('<p style="color:#ffcc00; font-weight:bold; font-size:16px;">📱 ПАНЕЛЬ УПРАВЛІННЯ</p>', unsafe_allow_html=True)
    
    st.markdown('<p class="module-header">МОДУЛЬ 1. РХБ ОБСТАНОВКА</p>', unsafe_allow_html=True)
    st.link_button("1.1. Карта рад. моніторингу", "https://sergsh1125-dotcom-radiation-situation-app-vlg9fu.streamlit.app/")
    st.link_button("1.2. Карта прогнозу хім. обстановки", "http://forecast.inf.ua/")
    st.link_button("1.3. Карта факт. рад. обстановки", "https://sergsh1125-dotcom-radiation-situation-app-vlg9fu.streamlit.app/")
    st.link_button("1.4. Карта факт. хім. обстановки", "https://sergsh1125-dotcom-chemical-map-app-rhopcd.streamlit.app/")
    
    st.markdown('<p class="module-header">МОДУЛЬ 2. БАЗИ ДАНИХ</p>', unsafe_allow_html=True)
    st.link_button("2.1. Аварійні картки НХР", "https://sergsh1125-dotcom.github.io/emergency-cards/")
    st.link_button("2.2. Токсодози бойових ОР", "https://sergsh1125-dotcom.github.io/toxicdoze/")

# ЦЕНТРАЛЬНА КОЛОНКА (КАРТА)
with col_center:
    # Google Maps з параметром для стабільної роботи
    components.iframe("https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d2600000!2d31.1!3d48.5!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1suk!2sua!4v1700000000000", height=600)

# ПРАВА КОЛОНКА
with col_right:
    st.markdown('<p class="module-header">МОДУЛЬ 3. РОЗРАХУНКИ</p>', unsafe_allow_html=True)
    st.link_button("3.1. Доза опромінення", "https://sergsh1125-dotcom.github.io/radiation-calculator/")
    st.link_button("3.2. Час перебування", "https://sergsh1125-dotcom.github.io/calculator-time/")
    
    st.markdown('<p class="module-header">МОДУЛЬ 4. ДОВІДКА</p>', unsafe_allow_html=True)
    st.link_button("4.1. Метеообстановка", "https://www.meteo.gov.ua/")
    
    # Випадаючий список для СОП та НПА
    with st.expander("📄 4.2. СОП та НПА"):
        st.link_button("📜 СОП №1 (Сайт ДСНС)", "https://dsns.gov.ua/")
        st.link_button("⚖️ Нормативна база", "https://zakon.rada.gov.ua/")

# Кнопка виходу в сайдбарі
if st.sidebar.button("Завершити сесію"):
    st.session_state["password_correct"] = False
    st.rerun()
