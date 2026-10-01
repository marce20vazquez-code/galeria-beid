import os
import time
import streamlit as st
from PIL import Image
import gdown

# Configuración de la página
st.set_page_config(page_title="BEID", layout="centered")
st.title("📸 BEID")

# --- ANIMACIONES CSS (Movimiento Ken Burns a la foto + Corazones) ---
st.markdown("""
    <style>
    /* Efecto Ken Burns: Zoom suave y ligero desplazamiento en las fotos */
    div[data-testid="stImage"] img {
        border-radius: 20px;
        box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.4);
        max-height: 75vh;
        object-fit: contain;
        animation: kenBurns 6s ease-in-out infinite alternate;
    }

    @keyframes kenBurns {
        0% {
            transform: scale(1) translateY(0px);
            opacity: 0.85;
        }
        50% {
            transform: scale(1.05) translateY(-6px);
            opacity: 1;
        }
        100% {
            transform: scale(1.08) translateY(6px);
            opacity: 0.95;
        }
    }

    /* Fondo con lluvia continua de corazones */
    .heart-container {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none; overflow: hidden; z-index: 99999;
    }

    .heart {
        position: absolute; bottom: -20px; color: #ff3366; font-size: 24px;
        animation: floatUp 4s linear infinite; opacity: 0.8;
    }

    @keyframes floatUp {
        0% { transform: translateY(0) rotate(0deg); opacity: 1; }
        100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
    }
    </style>

    <div class="heart-container">
        <div class="heart" style="left: 10%; animation-delay: 0s; animation-duration: 3.5s;">❤️</div>
        <div class="heart" style="left: 25%; animation-delay: 1.2s; animation-duration: 4s;">💖</div>
        <div class="heart" style="left: 40%; animation-delay: 0.5s; animation-duration: 3s;">💗</div>
        <div class="heart" style="left: 60%; animation-delay: 2s; animation-duration: 4.5s;">❤️</div>
        <div class="heart" style="left: 75%; animation-delay: 0.8s; animation-duration: 3.8s;">💘</div>
        <div class="heart" style="left: 90%; animation-delay: 1.5s; animation-duration: 4.2s;">💖</div>
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

# --- REPRODUCCIÓN AUTOMÁTICA CON MOVIMIENTO ---
if os.path.exists(CARPETA_FOTOS):
    archivos_completos = []
    
    for root, dirs, files in os.walk(CARPETA_FOTOS):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'webp')):
                archivos_completos.append(os.path.join(root, file))
    
    if archivos_completos:
        archivos_completos.sort()
        
        contenedor_foto = st.empty()
        
        # Bucle continuo de la galería
        while True:
            for ruta in archivos_completos:
                img = Image.open(ruta)
                contenedor_foto.image(img, use_container_width=True)
                # Duración de 6 segundos por foto para permitir apreciar el movimiento
                time.sleep(6)
    else:
        st.warning("No se encontraron fotos. Asegúrate de haber subido imágenes a tu carpeta de Drive.")
