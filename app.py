import os
import time
import streamlit as st
from PIL import Image, ImageOps
import gdown

# Configuración de la página
st.set_page_config(page_title="BEID", layout="centered")
st.title("📸 BEID")

# --- LISTA AMPLIADA DE FRASES DE AMOR ---
FRASES_DE_AMOR = [
    "Eres mi lugar favorito en el mundo. ❤️",
    "Cada día a tu lado es un regalo hermoso. 💖",
    "Gracias por hacer mi vida más bonita. 💕",
    "Tú y yo, mi momento preferido del día. 💗",
    "Contigo todo es infinitamente mejor. 💘",
    "Mi sonrisa favorita es la que tú me sacas. ✨",
    "El mejor recuerdo siempre es el que construyo a tu lado. 🥰",
    "Simplemente gracias por existir y estar en mi vida. 🌹",
    "Juntos es mi lugar favorito. ❤️",
    "Si pudiera elegir un momento, elegiría cualquier instante contigo. 💫",
    "Eres la historia más bonita que el destino escribió en mi vida. 📖✨",
    "Mi felicidad tiene tu nombre y tu sonrisa. 🥰",
    "Amarte es la decisión más fácil y hermosa que he tomado. 💖",
    "En tus ojos encontré mi hogar y en tu abrazo mi paz. 💓",
    "Cada segundo a tu lado vale por mil recuerdos. ⏳❤️",
    "No necesito el mundo entero, solo tu mano en la mía. 🤝💕",
    "Le das color, luz y sentido a todos mis días. ☀️💗",
    "Coincidir contigo es lo mejor que me ha pasado. 🌸✨",
    "Eres mi presente, mi futuro y mi pensamiento favorito de cada día. 💖",
    "Haces que lo ordinario se vuelva extraordinario. 💘"
]

# --- ANIMACIONES Y ESTILOS CSS ---
st.markdown("""
    <style>
    /* Centrado de la imagen */
    div[data-testid="stImage"] {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    /* Movimiento suave estilo Ken Burns a la foto */
    div[data-testid="stImage"] img {
        border-radius: 20px;
        box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.4);
        max-height: 70vh;
        object-fit: contain;
        animation: kenBurns 6s ease-in-out infinite alternate;
    }

    @keyframes kenBurns {
        0% { transform: scale(1) translateY(0px); opacity: 0.85; }
        50% { transform: scale(1.05) translateY(-6px); opacity: 1; }
        100% { transform: scale(1.08) translateY(6px); opacity: 0.95; }
    }

    /* Estilo para el texto de las frases de amor */
    .frase-amor {
        text-align: center;
        font-size: 26px;
        font-weight: 600;
        color: #ff3366;
        font-family: 'Georgia', serif;
        margin-top: 18px;
        margin-bottom: 20px;
        padding: 12px 18px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        text-shadow: 0px 2px 8px rgba(255, 51, 102, 0.3);
        animation: fadeIn 1.5s ease-in-out;
    }

    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* Fondo con lluvia intensa de corazones grandes */
    .heart-container {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none; overflow: hidden; z-index: 99999;
    }

    .heart {
        position: absolute; 
        bottom: -50px; 
        color: #ff3366;
        animation: floatUp 3.2s linear infinite; 
        opacity: 0.85;
    }

    @keyframes floatUp {
        0% { transform: translateY(0) rotate(0deg); opacity: 1; }
        100% { transform: translateY(-105vh) rotate(360deg); opacity: 0; }
    }
    </style>

    <div class="heart-container">
        <div class="heart" style="left: 5%; font-size: 42px; animation-delay: 0s; animation-duration: 3s;">❤️</div>
        <div class="heart" style="left: 15%; font-size: 58px; animation-delay: 1s; animation-duration: 3.8s;">💖</div>
        <div class="heart" style="left: 25%; font-size: 38px; animation-delay: 0.4s; animation-duration: 3.1s;">💗</div>
        <div class="heart" style="left: 35%; font-size: 62px; animation-delay: 1.8s; animation-duration: 4.2s;">❤️</div>
        <div class="heart" style="left: 45%; font-size: 48px; animation-delay: 0.2s; animation-duration: 3.4s;">💕</div>
        <div class="heart" style="left: 55%; font-size: 54px; animation-delay: 2.1s; animation-duration: 3.9s;">💖</div>
        <div class="heart" style="left: 65%; font-size: 40px; animation-delay: 0.7s; animation-duration: 3.2s;">💗</div>
        <div class="heart" style="left: 75%; font-size: 60px; animation-delay: 1.4s; animation-duration: 4.1s;">❤️</div>
        <div class="heart" style="left: 85%; font-size: 45px; animation-delay: 0.5s; animation-duration: 3.3s;">💘</div>
        <div class="heart" style="left: 95%; font-size: 52px; animation-delay: 1.9s; animation-duration: 3.6s;">💖</div>
    </div>
""", unsafe_allow_html=True)

# --- CONEXIÓN A GOOGLE DRIVE ---
URL_DRIVE = "https://drive.google.com/drive/folders/18IbNspLPRE20xGHNiA1ldh0H9zf1kD_l?usp=sharing"
CARPETA_FOTOS = "fotos_drive"

@st.cache_resource
def descargar_fotos_de_drive():
    if not os.path.exists(CARPETA_FOTOS):
        os.makedirs(CARPETA_FOTOS)
    if len(os.listdir(CARPETA_FOTOS)) == 0:
        try:
            gdown.download_folder(URL_DRIVE, output=CARPETA_FOTOS, quiet=False, use_cookies=False)
        except Exception as e:
            st.error(f"Ocurrió un error al conectar con Drive: {e}")

with st.spinner("Descargando fotos desde Google Drive... ❤️"):
    descargar_fotos_de_drive()

# --- REPRODUCCIÓN AUTOMÁTICA CON FOTOS Y FRASES ---
if os.path.exists(CARPETA_FOTOS):
    archivos_completos = []
    
    for root, dirs, files in os.walk(CARPETA_FOTOS):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'webp')):
                archivos_completos.append(os.path.join(root, file))
    
    if archivos_completos:
        archivos_completos.sort()
        
        contenedor_foto = st.empty()
        contenedor_frase = st.empty()
        
        while True:
            for idx, ruta in enumerate(archivos_completos):
                frase_actual = FRASES_DE_AMOR[idx % len(FRASES_DE_AMOR)]
                
                img = Image.open(ruta)
                img = ImageOps.exif_transpose(img)
                
                contenedor_foto.image(img, use_container_width=True)
                contenedor_frase.markdown(f'<div class="frase-amor">{frase_actual}</div>', unsafe_allow_html=True)
                
                time.sleep(6)
    else:
        st.warning("No se encontraron fotos. Asegúrate de haber subido imágenes a tu carpeta de Drive.")
