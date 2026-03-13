import streamlit as st
import streamlit.components.v1 as components

# --- 1. НАЛАШТУВАННЯ СТОРІНКИ ---
st.set_page_config(
    page_title="ДСНС - ОФІС CBRN",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ЕКРАН ВХОДУ ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True

    st.markdown("""
        <style>
        .login-box {
            display: flex; flex-direction: column; align-items: center;
            justify-content: center; margin-top: 10%; padding: 50px;
            background-color: #1b1e23; border: 4px solid #ffcc00;
            border-radius: 20px; width: 450px; margin-left: auto; margin-right: auto;
        }
        .stTextInput > div > div > input {
            text-align: center; background-color: #0e1117 !important; color: white !important;
            border: 1px solid #ffcc00 !important; font-size: 24px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<h1 style="color:#ffcc00; text-align:center; font-size: 50px; margin-bottom: 0px;">CBRN OFFICE</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color:#e0e0e0; text-align:center; margin-bottom: 30px; font-size: 18px;">СИСТЕМА ПІДТРИМКИ ПРИЙНЯТТЯ РІШЕНЬ</p>', unsafe_allow_html=True)
        password = st.text_input("Пароль", type="password", label_visibility="collapsed", placeholder="ВВЕДІТЬ ПАРОЛЬ")
        if st.button("УВІЙТИ В СИСТЕМУ"):
            if password == "1125": 
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("ДОСТУП ЗАБОРОНЕНО")
        st.markdown('</div>', unsafe_allow_html=True)
    return False

if not check_password():
    st.stop()

# --- 3. СТИЛІЗАЦІЯ ІНТЕРФЕЙСУ (ЗБІЛЬШЕНО) ---
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0e1117; color: #e0e0e0;}
    
    /* Назва порталу - ЗБІЛЬШЕНО У 3 РАЗИ */
    .main-title {
        color: #ffcc00; text-align: center; 
        font-size: 120px; /* Гігантський шрифт */
        font-weight: 900; 
        margin-top: -60px; margin-bottom: 0px;
        text-transform: uppercase; line-height: 1;
        letter-spacing: -2px;
    }
    .sub-title {
        color: #ffcc00; text-align: center; 
        font-size: 48px; font-weight: 500;
        margin-bottom: 40px;
    }
    
    /* Модулі - Більші та Жовті */
    .module-header {
        color: #ffcc00 !important; border-bottom: 3px solid #ffcc00; 
        margin-top: 30px; margin-bottom: 20px; 
        font-weight: bold; font-size: 28px; /* Збільшено */
        text-transform: uppercase;
    }

    /* Кнопки - Більші */
    div.stButton > button, a.stLinkButton {
        background-color: #1b1e23 !important; color: #ffffff !important;
        border: 1px solid #3d444d !important; border-radius: 6px !important;
        padding: 15px !important; width: 100% !important; 
        text-align: left !important; font-size: 18px !important; 
        font-weight: 500 !important; margin-bottom: 10px !important;
    }
    
    div.stButton > button:hover, a.stLinkButton:hover {
        border-color: #ffcc00 !important; color: #ffcc00 !important;
        background-color: #262a33 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. ШАПКА ---
st.markdown('<p class="main-title">ПЛАТФОРМА ПІДТРИМКИ РХБ ЗАХИСТУ</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">ДСНС - ОФІС CBRN</p>', unsafe_allow_html=True)

# --- 5. ОСНОВНА ПАНЕЛЬ ---
col_left, col_center, col_right = st.columns([1.2, 4, 1.2])

with col_left:
    st.markdown('<p style="color:#ffcc00; font-weight:bold; font-size:24px; text-decoration: underline;">📱 ПАНЕЛЬ УПРАВЛІННЯ</p>', unsafe_allow_html=True)
    
    st.markdown('<p class="module-header">МОДУЛЬ 1. РХБ ОБСТАНОВКА</p>', unsafe_allow_html=True)
    st.link_button("1.1. Карта радіаційного моніторингу (SaveEcoBot)", "https://www.saveecobot.com/radiation-maps")
    st.link_button("1.2. Карта прогнозу хім. обстановки", "http://forecast.inf.ua/")
    st.link_button("1.3. Карта фактичної рад. обстановки", "https://sergsh1125-dotcom-radiation-situation-app-vlg9fu.streamlit.app/")
    st.link_button("1.4. Карта фактичної хім. обстановки", "https://sergsh1125-dotcom-chemical-map-app-rhopcd.streamlit.app/")
    
    st.markdown('<p class="module-header">МОДУЛЬ 2. БАЗИ ДАНИХ</p>', unsafe_allow_html=True)
    st.link_button("2.1. Аварійні картки НХР", "https://sergsh1125-dotcom.github.io/emergency-cards/")
    st.link_button("2.2. Токсодози бойових ОР", "https://sergsh1125-dotcom.github.io/toxicdoze/")

with col_center:
    # Google Maps українською мовою
    # Параметр hl=uk забезпечує український інтерфейс
    components.iframe("https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d5124000.0!2d31.16558!3d48.379433!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1suk!2sua!4v1700000000000!5m2!1suk!2sua", height=800)
    st.caption("Оперативна карта України (UA)")

with col_right:
    st.markdown('<p class="module-header">МОДУЛЬ 3. РОЗРАХУНКИ</p>', unsafe_allow_html=True)
    st.link_button("3.1. Калькулятор дози опромінення", "https://sergsh1125-dotcom.github.io/radiation-calculator/")
    st.link_button("3.2. Калькулятор часу перебування", "https://sergsh1125-dotcom.github.io/calculator-time/")
    
    st.markdown('<p class="module-header">МОДУЛЬ 4. ДОВІДКОВА ІНФОРМАЦІЯ</p>', unsafe_allow_html=True)
    st.link_button("4.1. Метеообстановка", "https://www.meteo.gov.ua/")
    
    with st.expander("📄 4.2. СОП ТА НПА"):
        st.link_button("📜 Сайт ДСНС України", "https://dsns.gov.ua/")
        st.link_button("⚖️ Сайт Верховної Ради України", "https://zakon.rada.gov.ua/")

if st.sidebar.button("ВИЙТИ З СИСТЕМИ"):
    st.session_state["password_correct"] = False
    st.rerun()
