import streamlit as st
import streamlit.components.v1 as components

# --- 1. НАЛАШТУВАННЯ СТОРІНКИ ---
st.set_page_config(
    page_title="ДСНС - ОФІС CBRN",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ОЧИЩЕНИЙ ЕКРАН ВХОДУ ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True

    # Стиль екрану входу без зайвих віконець
    st.markdown("""
        <style>
        .login-box {
            display: flex; flex-direction: column; align-items: center;
            justify-content: center; margin-top: 15%; padding: 50px;
            background-color: #1b1e23; border: 3px solid #ffcc00;
            border-radius: 20px; width: 400px; margin-left: auto; margin-right: auto;
        }
        .stTextInput > div > div > input {
            text-align: center; background-color: #0e1117 !important; color: white !important;
            border: 1px solid #ffcc00 !important; font-size: 20px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<h1 style="color:#ffcc00; text-align:center; font-size: 40px; margin-bottom: 10px;">CBRN OFFICE</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color:#e0e0e0; text-align:center; margin-bottom: 30px;">СИСТЕМА ПІДТРИМКИ ПРИЙНЯТТЯ РІШЕНЬ</p>', unsafe_allow_html=True)
        
        # Використовуємо label_visibility="collapsed" щоб прибрати назву над полем вводу
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

# --- 3. СТИЛІЗАЦІЯ ПОРТАЛУ ---
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0e1117; color: #e0e0e0;}
    
    .main-title {
        color: #ffcc00; text-align: center; 
        font-size: 72px; font-weight: 900; 
        margin-top: -50px; text-transform: uppercase; line-height: 1.1;
    }
    .sub-title {
        color: #ffcc00; text-align: center; 
        font-size: 36px; margin-bottom: 30px;
    }
    
    .module-header {
        color: #ffcc00 !important; border-bottom: 2px solid #ffcc00; 
        margin-top: 25px; margin-bottom: 15px; 
        font-weight: bold; font-size: 22px; text-transform: uppercase;
    }

    div.stButton > button, a.stLinkButton {
        background-color: #1b1e23 !important; color: #ffffff !important;
        border: 1px solid #3d444d !important; border-radius: 4px !important;
        padding: 12px !important; width: 100% !important; 
        text-align: left !important; font-size: 16px !important; margin-bottom: 8px !important;
    }
    
    div.stButton > button:hover, a.stLinkButton:hover {
        border-color: #ffcc00 !important; color: #ffcc00 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. КОНТЕНТ ---
st.markdown('<p class="main-title">ПЛАТФОРМА ПІДТРИМКИ РХБ ЗАХИСТУ</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">ДСНС - ОФІС CBRN</p>', unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1, 4.5, 1])

with col_left:
    st.markdown('<p style="color:#ffcc00; font-weight:bold; font-size:20px; text-decoration: underline;">📱 ПАНЕЛЬ УПРАВЛІННЯ</p>', unsafe_allow_html=True)
    st.markdown('<p class="module-header">МОДУЛЬ 1. РХБ ОБСТАНОВКА</p>', unsafe_allow_html=True)
    st.link_button("1.1. Карта рад. моніторингу", "https://sergsh1125-dotcom-radiation-situation-app-vlg9fu.streamlit.app/")
    st.link_button("1.2. Карта прогнозу хім. обстановки", "http://forecast.inf.ua/")
    st.link_button("1.3. Карта факт. рад. обстановки", "https://sergsh1125-dotcom-radiation-situation-app-vlg9fu.streamlit.app/")
    st.link_button("1.4. Карта факт. хім. обстановки", "https://sergsh1125-dotcom-chemical-map-app-rhopcd.streamlit.app/")
    
    st.markdown('<p class="module-header">МОДУЛЬ 2. БАЗИ ДАНИХ</p>', unsafe_allow_html=True)
    st.link_button("2.1. Аварійні картки НХР", "https://sergsh1125-dotcom.github.io/emergency-cards/")
    st.link_button("2.2. Токсодози бойових ОР", "https://sergsh1125-dotcom.github.io/toxicdoze/")

with col_center:
    # Широка карта України українською
    components.iframe("https://www.openstreetmap.org/export/embed.html?bbox=22.0,44.0,40.2,52.5&layer=mapnik", height=750)

with col_right:
    st.markdown('<p class="module-header">МОДУЛЬ 3. РОЗРАХУНКИ</p>', unsafe_allow_html=True)
    st.link_button("3.1. Доза опромінення", "https://sergsh1125-dotcom.github.io/radiation-calculator/")
    st.link_button("3.2. Час перебування", "https://sergsh1125-dotcom.github.io/calculator-time/")
    
    st.markdown('<p class="module-header">МОДУЛЬ 4. ДОВІДКОВА ІНФОРМАЦІЯ</p>', unsafe_allow_html=True)
    st.link_button("4.1. Метеообстановка", "https://www.meteo.gov.ua/")
    
    with st.expander("📄 4.2. СОП ТА НПА"):
        st.link_button("📜 Сайт ДСНС", "https://dsns.gov.ua/")
        st.link_button("⚖️ Сайт Верховної Ради України", "https://zakon.rada.gov.ua/")

if st.sidebar.button("ВИХІД"):
    st.session_state["password_correct"] = False
    st.rerun()
