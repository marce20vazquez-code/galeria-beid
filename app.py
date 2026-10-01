import os
import streamlit as st
from PIL import Image

# Configuración de la interfaz
st.set_page_config(page_title="BEID", layout="centered")
st.title("📸 BEID")

# --- ANIMACIÓN CSS (Corazones flotantes y estilo de foto) ---
st.markdown("""
    <style>
    /* Efecto de la foto (aparece y hace zoom suave) */
    div[data-testid="stImage"] img {
        animation: zoomFade 2s ease-in-out forwards;
        border-radius: 15px;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.4);
        max-height: 75vh;
        object-fit: contain;
    }
    @keyframes zoomFade {
        0% { opacity: 0.2; transform: scale(0.95); }
        20% { opacity: 1; }
        100% { opacity: 1; transform: scale(1.05); }
    }

    /* Fondo con corazones flotantes constantes */
    .heart-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: hidden;
        z-index: 99999;
    }

    .heart {
        position: absolute;
        bottom: -20px;
        color: #ff3366;
        font-size: 24px;
        animation: floatUp 4s linear infinite;
        opacity: 0.8;
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

# --- CREAR CARPETA SI NO EXISTE ---
CARPETA_FOTOS = "BEID"
if not os.path.exists(CARPETA_FOTOS):
    os.makedirs(CARPETA_FOTOS)

# --- GALERÍA PÚBLICA ---
st.subheader("🖼️ Galería BEID")

# Filtrar solo archivos de imagen (excluyendo el .gitkeep)
archivos = [f for f in os.listdir(CARPETA_FOTOS) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))]

if archivos:
    archivos.sort()
    
    # Menú desplegable para elegir qué foto ver tranquilamente
    foto_seleccionada = st.selectbox("Selecciona una foto:", archivos, index=0)

    # Mostrar la foto seleccionada completa y sin recortes
    ruta_img = os.path.join(CARPETA_FOTOS, foto_seleccionada)
    img = Image.open(ruta_img)
    st.image(img, use_container_width=True)
else:
    st.info("Sube tus fotos a la carpeta BEID en GitHub para verlas aquí.")
