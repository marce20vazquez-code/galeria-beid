import os
import streamlit as st
import gdown

# Configuración inicial de Streamlit
st.set_page_config(page_title="GALERÍA DE RECUERDOS", layout="wide")

# --- LISTA DE FRASES ---
LISTA_DE_FRASES = [
    "Tú y yo, mi momento preferido del día. 💖✨",
    "Contigo cada instante se vuelve inolvidable. 🌙✨",
    "Mi lugar favorito en el mundo siempre es a tu lado. 🌹",
    "Cada foto guarda una sonrisa que me sacaste. 📸❤️",
    "El mejor capítulo de mi vida lo escribo contigo. 📖💖",
    "Gracias por iluminar mis días con tu existencia. ✨💫",
    "Un recuerdo más de todos los que nos faltan por vivir. 🥰",
    "Amor del bueno, del que hace bien al alma. 💘"
]

# --- DESCARGA DE FOTOS DESDE GOOGLE DRIVE ---
URL_DRIVE = "https://drive.google.com/drive/folders/18IbNspLPRE20xGHNiA1ldh0H9zf1kD_l?usp=sharing"
CARPETA_FOTOS = "fotos_drive"

@st.cache_resource
def descargar_fotos_de_drive():
    if not os.path.exists(CARPETA_FOTOS):
        os.makedirs(CARPETA_FOTOS)
    if len(os.listdir(CARPETA_FOTOS)) == 0:
        try:
            gdown.download_folder(URL_DRIVE, output=CARPETA_FOTOS, quiet=True, use_cookies=False)
        except Exception as e:
            st.error(f"Error al descargar imágenes de Drive: {e}")

with st.spinner("Cargando recuerdos... ❤️✨"):
    descargar_fotos_de_drive()

# Obtener rutas de las imágenes
archivos_fotos = []
if os.path.exists(CARPETA_FOTOS):
    for root, _, files in os.walk(CARPETA_FOTOS):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'webp')):
                archivos_fotos.append(os.path.join(root, file))

archivos_fotos.sort()

# Título
st.header("Nuestra historia en imágenes 💖✨🌙")

# --- MOSTRAR GALERÍA EN COLUMNAS ---
if archivos_fotos:
    num_frases = len(LISTA_DE_FRASES)
    cols = st.columns(3)
    
    for i, path in enumerate(archivos_fotos):
        frase_actual = LISTA_DE_FRASES[i % num_frases]
        # Se utiliza use_container_width=True en lugar de use_column_width
        cols[i % 3].image(path, caption=frase_actual, use_container_width=True)
else:
    st.warning("No se encontraron imágenes en la carpeta de Drive.")
