import os
import streamlit as st
from PIL import Image
import gdown

# Configuración de la interfaz
st.set_page_config(page_title="BEID", layout="centered")
st.title("📸 BEID")

# --- ANIMACIÓN CSS (Corazones flotantes) ---
st.markdown("""
    <style>
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

# Usamos st.cache_resource para descargar solo una vez cuando se abre la app
@st.cache_resource
def descargar_fotos_de_drive():
    if not os.path.exists(CARPETA_FOTOS):
        os.makedirs(CARPETA_FOTOS)
    
    # Si la carpeta local está vacía, iniciamos la descarga
    if len(os.listdir(CARPETA_FOTOS)) == 0:
        try:
            gdown.download_folder(URL_DRIVE, output=CARPETA_FOTOS, quiet=False, use_cookies=False)
        except Exception as e:
            st.error(f"Ocurrió un error al conectar con Drive: {e}")

# Mensaje de carga mientras se bajan las imágenes pesadas
with st.spinner("Descargando fotos desde Google Drive... (esto puede tardar un poco la primera vez) ❤️"):
    descargar_fotos_de_drive()

# --- MOSTRAR GALERÍA ---
if os.path.exists(CARPETA_FOTOS):
    archivos_completos = []
    
    # Buscar imágenes en todas las subcarpetas que Drive haya creado
    for root, dirs, files in os.walk(CARPETA_FOTOS):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'webp')):
                archivos_completos.append(os.path.join(root, file))
    
    if archivos_completos:
        # Ordenamos y separamos solo los nombres para que el menú se vea limpio
        nombres_archivos = [os.path.basename(ruta) for ruta in archivos_completos]
        nombres_archivos.sort()
        
        foto_seleccionada_nombre = st.selectbox("Selecciona una foto:", nombres_archivos, index=0)
        
        # Encontramos la ruta real de la foto que el usuario eligió en el menú
        ruta_img = next(ruta for ruta in archivos_completos if os.path.basename(ruta) == foto_seleccionada_nombre)
        
        img = Image.open(ruta_img)
        st.image(img, use_container_width=True)
    else:
        st.warning("No se encontraron fotos. Asegúrate de haber subido imágenes a tu carpeta de Drive.")
