import streamlit as st
import pandas as pd
import os

# 1. Налаштування сторінки
st.set_page_config(
    page_title="ДСНС | РХБ захист",
    page_icon="☢️",
    layout="wide"
)

# 2. Мета-дані для іконки ярлика та стилізація
# ЗАМІНІТЬ 'YOUR_REPO' на назву вашого репозиторію
icon_url = "https://raw.githubusercontent.com/sergsh1125-dotcom/YOUR_REPO/main/icon.png"

st.markdown(f"""
    <head>
        <link rel="apple-touch-icon" href="{icon_url}">
        <link rel="icon" href="{icon_url}" type="image/png">
        <meta name="apple-mobile-web-app-capable" content="yes">
    </head>
    <style>
    /* Темна тема з золотими акцентами */
    .stApp {{
        background-color: #0e1117;
        color: #e0e0e0;
    }}
    
    /* Заголовки */
    h1, h2, h3 {{
        color: #ffcc00 !important;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }}

    /* Картки модулів */
    .module-card {{
        background-color: #1b1e23;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #3d444d;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }}

    /* Кнопки в стилі ДСНС (Золото на темному) */
    div.stButton > button, a.stLinkButton {{
        background-color: #ffcc00 !important;
        color: #000000 !important;
        border-radius: 8px !important;
        padding: 14px !important;
        width: 100% !important;
        font-weight: bold !important;
        text-transform: uppercase;
        border: none !important;
        transition: 0.3s;
    }}
    
    div.stButton > button:hover, a.stLinkButton:hover {{
        background-color: #e6b800 !important;
        transform: scale(1.02);
    }}

    /* Стиль табів */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: #1b1e23;
        border-radius: 10px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        color: #ffffff;
    }}
    
    .stTabs [aria-selected="true"] {{
        color: #ffcc00 !important;
        border-bottom-color: #ffcc00 !important;
    }}

    /* Таблиці */
    [data-testid="stDataFrame"] {{
        background-color: #1b1e23;
        border-radius: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ВЕРХНЯ ПАНЕЛЬ ---
col_logo, col_title = st.columns([1, 4])
with col_logo:
    # Якщо іконка вже завантажена на GitHub, вона з'явиться тут
    st.image(icon_url, width=100)
with col_title:
    st.title("ПЛАТФОРМА ПІДТРИМКИ РХБ ЗАХИСТУ")
    st.write("🚒 **ДСНС УКРАЇНИ** | Оперативне управління")

st.divider()

# --- МОДУЛЬ 1: ОБСТАНОВКА ---
st.markdown('<div class="module-card">', unsafe_allow_html=True)
st.subheader("🌐 1. МОНІТОРІНГ ОБСТАНОВКИ")
c1, c2 = st.columns(2)
with c1:
    st.link_button("📊 1.1. Радіаційний моніторинг", "https://sergsh1125-dotcom-radiation-situation-app-vlg9fu.streamlit.app/")
    st.link_button("☢️ 1.3. Фактична рад. обстановка", "https://sergsh1125-dotcom-radiation-situation-app-vlg9fu.streamlit.app/")
with c2:
    st.link_button("🚀 1.2. Прогноз хім. обстановки", "http://forecast.inf.ua/")
    st.link_button("☣️ 1.4. Фактична хім. обстановка", "https://sergsh1125-dotcom-chemical-map-app-rhopcd.streamlit.app/")
st.markdown('</div>', unsafe_allow_html=True)

# --- МОДУЛЬ 2 & 3: БД ТА КАЛЬКУЛЯТОРИ ---
col_db, col_calc = st.columns(2)

with col_db:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.subheader("🧪 2. БАЗА ДАНИХ НХР")
    st.link_button("📋 2.1. Аварійні картки", "https://sergsh1125-dotcom.github.io/emergency-cards/")
    st.link_button("⚠️ 2.2. Рівні впливу БОР", "#")
    st.markdown('</div>', unsafe_allow_html=True)

with col_calc:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.subheader("🧮 3. КАЛЬКУЛЯТОРИ")
    st.link_button("⚛️ 3.1. Доза опромінення", "https://sergsh1125-dotcom.github.io/radiation-calculator/")
    st.link_button("🕒 3.2. Час перебування", "https://sergsh1125-dotcom.github.io/calculator-time/")
    st.link_button("⚗️ 3.3. Токсичні дози", "https://sergsh1125-dotcom.github.io/toxicdoze/")
    st.markdown('</div>', unsafe_allow_html=True)

# --- МОДУЛЬ 4: ДОВІДКА ---
st.markdown('<div class="module-card">', unsafe_allow_html=True)
st.subheader("📚 4. ДОВІДКОВА ІНФОРМАЦІЯ")
t1, t2, t3 = st.tabs(["☁️ МЕТЕО", "📄 ІНСТРУКЦІЇ", "🧴 СПЕЦОБРОБКА"])

with t1:
    st.link_button("🌍 Гідрометцентр України", "https://www.meteo.gov.ua/")

with t2:
    st.write("Документація та технічні описи приладів.")
    st.button("📥 Завантажити архів інструкцій")

with t3:
    st.write("📋 Таблиця розчинів (дані з GitHub)")
    # Посилання на ваш CSV файл
    csv_url = "https://raw.githubusercontent.com/sergsh1125-dotcom/YOUR_REPO/main/solutions.csv"
    try:
        df = pd.read_csv(csv_url)
        st.dataframe(df, use_container_width=True, hide_index=True)
    except:
        st.info("Очікується завантаження solutions.csv...")
st.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("🆔 **Підрозділ:** РХБ захисту")
st.sidebar.markdown("🛰️ **Статус:** Онлайн")
