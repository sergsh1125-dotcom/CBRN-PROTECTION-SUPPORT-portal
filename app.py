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
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">Платформа підтримки заходів реагування на ХБРЯ інциденти</p>', unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1.3, 4.4, 1.3])

# -------- ЛІВА ПАНЕЛЬ --------
with col_left:
    st.markdown('<p class="module-header">МОДУЛЬ 1. РХБ ОБСТАНОВКА</p>', unsafe_allow_html=True)
    st.link_button("1.1. Карта радіаційного моніторингу (SaveEcoBot)", "https://www.saveecobot.com/radiation-maps")
    st.link_button("1.2. Карта радіаційного моніторингу Укргідромету", "https://www.meteo.gov.ua/#RADIO")
    st.link_button("1.3. Карта радіаційного моніторингу країн ЄС", "https://remap.jrc.ec.europa.eu/Advanced.aspx")
    st.link_button("1.4. Карта прогнозу хімічної обстановки", "http://forecast.inf.ua/")
    st.link_button("1.5. Карта фактичної РХБ обстановки", "https://map-obstanovka-vuvukyx4vwu9jrhuv68vcg.streamlit.app/")
    st.info("💡 Координати на карті фактичної РХБ обстановки завантажуються кліком мишки.")

    st.markdown('<p class="module-header">МОДУЛЬ 2. БАЗИ ДАНИХ</p>', unsafe_allow_html=True)
    st.link_button("2.1. Аварійні картки НХР", "https://sergsh1125-dotcom.github.io/emergency-cards/")
    st.link_button("2.2. Токсодози бойових ОР", "https://sergsh1125-dotcom.github.io/toxicdoze/")

# -------- ЦЕНТР (КАРТА) --------
with col_center:
    with open("modules/map_engine_v2.html", "r", encoding="utf-8") as f:
        map_html = f.read()

    components.html(map_html, height=750)
# -------- ПРАВА ПАНЕЛЬ --------
with col_right:
    with st.expander("🌤️ МОНІТОРИНГ ВІТРУ", expanded=False):
        windy_html = """
        <iframe width="100%" height="300" src="https://embed.windy.com/embed2.html?lat=49.0&lon=31.0&zoom=5&level=surface&overlay=wind&product=ecmwf&metricWind=m%2Fs&metricTemp=%C2%B0C" frameborder="0"></iframe>
        """
        components.html(windy_html, height=310)

    st.markdown('<p class="module-header">МОДУЛЬ 3. РОЗРАХУНКИ</p>', unsafe_allow_html=True)
    st.link_button("3.1. Калькулятор дози (Ядерний вибух)", "https://sergsh1125-dotcom.github.io/radiation-calculator/")
    st.link_button("3.2. Калькулятор дози (Аварія на АЕС)", "https://sergsh1125-dotcom.github.io/radiation-doza/")
    st.link_button("3.3. Розрахунок часу перебування", "https://sergsh1125-dotcom.github.io/calculator-time/")

    st.markdown('<p class="module-header">МОДУЛЬ 4. ДОВІДКА</p>', unsafe_allow_html=True)
    st.link_button("4.1. Укргідрометеоцентр", "https://www.meteo.gov.ua/")
    st.link_button("4.2. Нормативно-правова база РХЗ", "https://dsns.gov.ua/zakonodavstvo/perelik-normativno-pravovix-dokumentiv-shho-reglamentuyut-diyalnist-pidrozdiliv-dsns-ukrayini/upravlinnia-organizaciyi-radiaciinogo-ximicnogo-ta-biologicnogo-zaxistu")
    st.link_button("4.3. СОП 1.1/РХБЗ: Демеркуризація\nСОП 1.2: Дії підрозділів при НС з НХР", "https://kyiv.dsns.gov.ua/navchalniy-centr-gu/sluzhbova-pidgotovka/normativno-pravovi-akti")
    # ===============================
    # 4.4. ФОРМАЛІЗОВАНІ ДОКУМЕНТИ
    # ===============================

    DOCS_FOLDER = "docs"

    # ----- Стиль кнопок документів -----
    st.markdown("""
    <style>
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

    # ----- Розділ модуля -----
    with st.expander("4.4. ФОРМАЛІЗОВАНІ ДОКУМЕНТИ", expanded=False):

        if os.path.isdir(DOCS_FOLDER):

            allowed_extensions = (
                ".docx",
                ".pdf",
                ".xlsx",
                ".csv",
                ".txt",
                ".pptx"
            )

            doc_files = sorted([
                f for f in os.listdir(DOCS_FOLDER)
                if f.lower().endswith(allowed_extensions)
            ])

            if doc_files:

                for file_name in doc_files:

                    file_path = os.path.join(DOCS_FOLDER, file_name)

                    with open(file_path, "rb") as file:

                        st.download_button(
                            label=f"📄 {file_name}",
                            data=file,
                            file_name=file_name,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True,
                            key=f"doc_{file_name}"
                        )

            else:
                st.warning("У папці docs немає файлів.")

        else:
            st.error("Папка docs не знайдена.")
   
