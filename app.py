import os
import base64
import io
import streamlit as st
from PIL import Image
import gdown

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

# --- DESCARGA Y OPTIMIZACIÓN DE IMÁGENES ---
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
            st.error(f"Error al descargar de Drive: {e}")

with st.spinner("Cargando y optimizando recuerdos... ❤️✨"):
    descargar_fotos_de_drive()

archivos_fotos = []
if os.path.exists(CARPETA_FOTOS):
    for root, _, files in os.walk(CARPETA_FOTOS):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'webp')):
                archivos_fotos.append(os.path.join(root, file))

archivos_fotos.sort()

# Función optimizada: Redimensiona y comprime la foto en memoria antes de Base64
@st.cache_data
def get_optimized_image_base64(path):
    try:
        with Image.open(path) as img:
            img = img.convert('RGB')
            # Redimensiona a tamaño compacto para Polaroid (máximo 300px)
            img.thumbnail((300, 350))
            
            buffer = io.BytesIO()
            # Guarda comprimido en calidad 75%
            img.save(buffer, format="JPEG", quality=75, optimize=True)
            encoded = base64.b64encode(buffer.getvalue()).decode()
            return f"data:image/jpeg;base64,{encoded}"
    except Exception:
        return ""

# Cargar imágenes optimizadas en una lista de cadenas Base64
imagenes_b64 = [get_optimized_image_base64(f) for f in archivos_fotos if get_optimized_image_base64(f)]

if not imagenes_b64:
    st.warning("No se encontraron imágenes o aún se están procesando.")
    st.stop()

# --- CONSTRUCCIÓN DEL HTML (CORREGIDO) ---
# Se utiliza una lógica de bucle para generar una secuencia sin interrupciones
num_fotos = len(imagenes_b64)
focos_colores = ["foco-rojo", "foco-azul", "foco-dorado", "foco-verde", "foco-morado"]
html_fotos = ""

# Se generan 2 conjuntos de fotos para un bucle infinito
for idx in range(num_fotos * 2):
    img_idx = idx % num_fotos # Índice de la foto original
    # Obtiene la cadena Base64 correcta para esta foto
    img_data_uri = imagenes_b64[img_idx]
    
    foco_clase = focos_colores[idx % len(focos_colores)]
    rotacion = "-3deg" if idx % 2 == 0 else "3deg"
    frase_actual = LISTA_DE_FRASES[idx % len(LISTA_DE_FRASES)]
    
    # Aquí está la corrección: el Base64 se pone como src="data:..."
    html_fotos += f"""
    <div class="item-cuerda">
        <div class="foco {foco_clase}"></div>
        <div class="polaroid" style="transform: rotate({rotacion});">
            <div class="pinza"></div>
            <img src="{img_data_uri}" alt="Recuerdo {img_idx + 1}" loading="lazy" />
            <p class="texto-polaroid">{frase_actual}</p>
        </div>
    </div>
    """

# --- ESTILOS CSS ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600&family=Montserrat:wght@800;900&display=swap');

body {{
    background-color: #0c001f;
}}

.titulo-container {{
    text-align: center;
    margin-top: -10px;
    margin-bottom: 25px;
}}

.titulo-3d {{
    font-family: 'Montserrat', sans-serif;
    font-size: 3.5rem;
    font-weight: 900;
    letter-spacing: 5px;
    background: linear-gradient(120deg, #ff007f, #ffd700, #00ffff, #a855f7);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: moverColores 5s linear infinite;
    filter: drop-shadow(0px 0px 12px rgba(255, 0, 127, 0.8));
}}

@keyframes moverColores {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

.galeria-caja {{
    width: 100%;
    overflow: hidden;
    position: relative;
    padding: 60px 0 40px 0;
    background: radial-gradient(circle, rgba(26,0,51,0.8) 0%, rgba(12,0,31,1) 100%);
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}}

.cuerda {{
    position: absolute;
    top: 75px;
    left: 0;
    width: 100%;
    height: 4px;
    background: #a87e50;
    box-shadow: 0 2px 5px rgba(0,0,0,0.5);
    z-index: 1;
}}

.riel-desplazamiento {{
    display: flex;
    width: max-content;
    animation: desplazar 40s linear infinite;
    z-index: 2;
    position: relative;
}}

.riel-desplazamiento:hover {{
    animation-play-state: paused;
}}

@keyframes desplazar {{
    0% {{ transform: translateX(0); }}
    100% {{ transform: translateX(-50%); }}
}}

.item-cuerda {{
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0 25px;
    position: relative;
}}

.pinza {{
    position: absolute;
    top: -18px;
    left: 50%;
    transform: translateX(-50%);
    width: 12px;
    height: 28px;
    background: #d2b48c;
    border-radius: 2px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.4);
    z-index: 10;
}}

.polaroid {{
    background: #ffffff;
    padding: 10px 10px 15px 10px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.6);
    border-radius: 4px;
    width: 190px;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.polaroid img {{
    width: 170px;
    height: 200px;
    object-fit: cover;
    border-radius: 2px;
    display: block;
}}

.texto-polaroid {{
    font-family: 'Caveat', cursive, sans-serif;
    font-size: 1.2rem;
    color: #222222;
    text-align: center;
    margin: 10px 0 0 0;
    line-height: 1.2;
    font-weight: 600;
}}

.foco {{
    position: absolute;
    top: -45px;
    width: 22px;
    height: 32px;
    border-radius: 50% 50% 45% 45%;
    z-index: 5;
}}

.foco-rojo {{ background: #ff4d4d; box-shadow: 0 0 15px #ff4d4d, 0 0 30px #ff4d4d; }}
.foco-azul {{ background: #4da6ff; box-shadow: 0 0 15px #4da6ff, 0 0 30px #4da6ff; }}
.foco-dorado {{ background: #ffd700; box-shadow: 0 0 15px #ffd700, 0 0 30px #ffd700; }}
.foco-verde {{ background: #4dff4d; box-shadow: 0 0 15px #4dff4d, 0 0 30px #4dff4d; }}
.foco-morado {{ background: #a855f7; box-shadow: 0 0 15px #a855f7, 0 0 30px #a855f7; }}

.frase-bottom {{
    text-align: center;
    margin-top: 35px;
    font-family: 'Montserrat', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: #ffffff;
    text-shadow: 0 0 12px rgba(0, 255, 255, 0.8), 0 0 20px rgba(255, 0, 127, 0.6);
}}
</style>

<div class="titulo-container">
    <h1 class="titulo-3d">RECUERDOS</h1>
</div>

<div class="galeria-caja">
    <div class="cuerda"></div>
    <div class="riel-desplazamiento">
        {html_fotos}
    </div>
</div>

<div class="frase-bottom">
    Nuestra historia en imágenes 💖✨🌙
</div>
""", unsafe_allow_html=True)
