import os
from PIL import Image
import streamlit as st

# ---------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="GALERÍA DE RECUERDOS",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Estilos personalizados para un fondo elegante y romántico
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        div[data-testid="stHeader"] {display: none;}
        
        .stApp {
            background: radial-gradient(circle at center, #1b003a 0%, #080014 100%);
            color: white;
        }
        
        .titulo-principal {
            text-align: center;
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(120deg, #ff007f, #ffd700, #00ffff, #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 30px;
            letter-spacing: 4px;
        }
        
        .polaroid-card {
            background: white;
            padding: 15px 15px 25px 15px;
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.6);
            margin-bottom: 25px;
            text-align: center;
            transform: rotate(-1deg);
            transition: transform 0.3s ease;
        }
        
        .polaroid-card:hover {
            transform: scale(1.03) rotate(0deg);
        }
        
        .polaroid-text {
            font-family: 'Courier New', Courier, monospace;
            font-size: 1.2rem;
            color: #222;
            margin-top: 15px;
            font-weight: bold;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# --- FRASES ROMÁNTICAS ---
LISTA_DE_FRASES = [
    "Tú y yo, mi momento preferido del día. 💖✨",
    "Contigo cada instante se vuelve inolvidable. 🌙✨",
    "Mi lugar favorito en el mundo siempre es a tu lado. 🌹",
    "Cada foto guarda una sonrisa que me sacaste. 📸❤",
    "El mejor capítulo de mi vida lo escribo contigo. 📖💖",
    "Gracias por iluminar mis días con tu existencia. ✨💫",
    "Un recuerdo más de todos los que nos faltan por vivir. 🥰",
    "Amor del bueno, del que hace bien al alma. 💘",
]

CARPETA_FOTOS = "fotos"
CARPETA_MUSICA = "musica"

if not os.path.exists(CARPETA_FOTOS):
  os.makedirs(CARPETA_FOTOS)
if not os.path.exists(CARPETA_MUSICA):
  os.makedirs(CARPETA_MUSICA)

# --- TÍTULO ---
st.markdown('<h1 class="titulo-principal">✨ RECUERDOS ✨</h1>', unsafe_allow_html=True)

# --- CARGAR FOTOS DE LA CARPETA ---
archivos_fotos = []
try:
  for file in os.listdir(CARPETA_FOTOS):
    if file.lower().endswith(("png", "jpg", "jpeg", "webp")):
      archivos_fotos.append(os.path.join(CARPETA_FOTOS, file))
except Exception:
  pass

archivos_fotos.sort()

# --- REPRODUCTOR DE MÚSICA AUTOMÁTICO ---
archivos_musica = []
try:
  for file in os.listdir(CARPETA_MUSICA):
    if file.lower().endswith(("mp3", "wav", "m4a", "ogg")):
      archivos_musica.append(os.path.join(CARPETA_MUSICA, file))
except Exception:
  pass

if archivos_musica:
  st.audio(archivos_musica[0], format="audio/mp3", autoplay=True, loop=True)

# --- MOSTRAR GALERÍA EN CUADRÍCULA LIMPIA ---
if archivos_fotos:
  # Creamos columnas para organizar las fotos de forma atractiva (3 por fila)
  columnas = st.columns(3)

  for idx, ruta_foto in enumerate(archivos_fotos):
    columna_actual = columnas[idx % 3]
    frase = LISTA_DE_FRASES[idx % len(LISTA_DE_FRASES)]

    with columna_actual:
      try:
        imagen = Image.open(ruta_foto)
        st.markdown('<div class="polaroid-card">', unsafe_allow_html=True)
        st.image(imagen, use_column_width=True)
        st.markdown(
            f'<p class="polaroid-text">{frase}</p>', unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
      except Exception:
        pass
else:
  st.info(
      "Sube tus imágenes a la carpeta 'fotos' para comenzar a ver tu galería."
  )
