import os
import streamlit as st
import gdown
from PIL import Image

# Configuración inicial de Streamlit
st.set_page_config(page_title="GALERÍA DE RECUERDOS", layout="wide")

# --- LISTA DE FRASES (Se usarán como subtítulos de las fotos) ---
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
    # Crea la carpeta local si no existe
    if not os.path.exists(CARPETA_FOTOS):
        os.makedirs(CARPETA_FOTOS)
    # Descarga solo si la carpeta está vacía
    if len(os.listdir(CARPETA_FOTOS)) == 0:
        try:
            # Descarga de Google Drive usando gdown
            gdown.download_folder(URL_DRIVE, output=CARPETA_FOTOS, quiet=True, use_cookies=False)
        except Exception as e:
            st.error(f"Error al descargar imágenes de Drive: {e}")

# Muestra un spinner mientras se descargan las fotos
with st.spinner("Cargando recuerdos... ❤️✨"):
    descargar_fotos_de_drive()

# Obtener rutas completas de las fotos locales y ordenarlas
archivos_fotos = []
if os.path.exists(CARPETA_FOTOS):
    for root, _, files in os.walk(CARPETA_FOTOS):
        for file in files:
            # Filtra solo archivos de imagen compatibles
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'webp')):
                archivos_fotos.append(os.path.join(root, file))

# Ordena las fotos por nombre de archivo
archivos_fotos.sort()

# Título de la galería (fijo, sin animaciones complejas)
st.header("Nuestra historia en imágenes 💖✨🌙")

# --- DISEÑO DE LA GALERÍA (Robustez con st.image) ---
# Se utiliza un diseño de cuadrícula (grid) con columnas para una vista estática y ordenada
col1, col2, col3 = st.columns(3)
placeholders = [col1, col2, col3]

# Itera sobre los archivos de fotos y los muestra en las columnas con sus frases
if archivos_fotos:
    num_frases = len(LISTA_DE_FRASES)
    for i, path in enumerate(archivos_fotos):
        # Asigna secuencialmente una frase a cada foto, ciclando si hay más fotos que frases
        frase_actual = LISTA_DE_FRASES[i % num_frases]
        
        # Muestra la imagen usando el método oficial st.image con su frase como subtítulo
        # 'use_column_width=True' ajusta la imagen al ancho de la columna
        placeholders[i % 3].image(path, caption=frase_actual, use_column_width=True)
else:
    # Muestra una advertencia si no se encontraron imágenes
    st.warning("No se encontraron imágenes en la carpeta de Drive.")
