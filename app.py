import os
import base64
import io
import random
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import gdown

# ---------------------------------------------------------
# CONFIGURACIÓN DE DRIVE PARA FOTOS Y MÚSICA
# ---------------------------------------------------------
URL_DRIVE_FOTOS = "https://drive.google.com/drive/folders/18IbNspLPRE20xGHNiA1ldh0H9zf1kD_l?usp=sharing"
URL_DRIVE_MUSICA = "PEGA_AQUI_EL_ENLACE_DE_TU_CARPETA_DE_MUSICA_EN_DRIVE"

CARPETA_FOTOS = "fotos_drive"
CARPETA_MUSICA = "musica_drive"

# 1. Configuración inicial de la página
st.set_page_config(
    page_title="GALERÍA DE RECUERDOS", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS para eliminar márgenes de Streamlit
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        div[data-testid="stHeader"] {display: none;}
        
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }
        
        iframe {
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
        }
        
        body {
            background-color: #080014 !important;
            overflow: hidden !important;
        }
    </style>
""", unsafe_allow_html=True)

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
@st.cache_resource
def descargar_fotos_de_drive():
    if not os.path.exists(CARPETA_FOTOS):
        os.makedirs(CARPETA_FOTOS)
    if len(os.listdir(CARPETA_FOTOS)) == 0:
        try:
            gdown.download_folder(URL_DRIVE_FOTOS, output=CARPETA_FOTOS, quiet=True, use_cookies=False)
        except Exception as e:
            st.error(f"Error al descargar fotos de Drive: {e}")

# --- DESCARGA DE MÚSICA DESDE DRIVE ---
@st.cache_resource
def descargar_musica_de_drive():
    if not os.path.exists(CARPETA_MUSICA):
        os.makedirs(CARPETA_MUSICA)
    if len(os.listdir(CARPETA_MUSICA)) == 0:
        try:
            gdown.download_folder(URL_DRIVE_MUSICA, output=CARPETA_MUSICA, quiet=True, use_cookies=False)
        except Exception as e:
            st.error(f"Error al descargar música de Drive: {e}")

with st.spinner("Cargando recuerdos y música... ❤️✨"):
    descargar_fotos_de_drive()
    descargar_musica_de_drive()

# Procesar Fotos
archivos_fotos = []
if os.path.exists(CARPETA_FOTOS):
    for root, _, files in os.walk(CARPETA_FOTOS):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'webp')):
                archivos_fotos.append(os.path.join(root, file))

archivos_fotos.sort()

@st.cache_data
def get_optimized_image_base64(path):
    try:
        with Image.open(path) as img:
            img = img.convert('RGB')
            img.thumbnail((400, 450))
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=80, optimize=True)
            encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')
            return f"data:image/jpeg;base64,{encoded}"
    except Exception:
        return ""

imagenes_b64 = [get_optimized_image_base64(f) for f in archivos_fotos if get_optimized_image_base64(f)]

if not imagenes_b64:
    st.warning("No se encontraron imágenes en la carpeta de Drive.")
    st.stop()

# Procesar Canción Aleatoria a Base64
archivos_musica = []
if os.path.exists(CARPETA_MUSICA):
    for root, _, files in os.walk(CARPETA_MUSICA):
        for file in files:
            if file.lower().endswith(('mp3', 'wav', 'm4a', 'ogg')):
                archivos_musica.append(os.path.join(root, file))

musica_b64 = ""
if archivos_musica:
    cancion_elegida = random.choice(archivos_musica)
    try:
        with open(cancion_elegida, "rb") as audio_file:
            encoded_audio = base64.b64encode(audio_file.read()).decode('utf-8')
            musica_b64 = f"data:audio/mp3;base64,{encoded_audio}"
    except Exception as e:
        st.error(f"Error al procesar el audio: {e}")

# --- CONSTRUCCIÓN DE LA GALERÍA ---
focos_colores = ["foco-rojo", "foco-azul", "foco-dorado", "foco-verde", "foco-morado"]
items_galeria = imagenes_b64 + imagenes_b64

html_fotos = ""
for idx, img_src in enumerate(items_galeria):
    foco_clase = focos_colores[idx % len(focos_colores)]
    frase_actual = LISTA_DE_FRASES[idx % len(LISTA_DE_FRASES)]
    
    html_fotos += f"""
    <div class="item-cuerda">
        <div class="foco {foco_clase}"></div>
        <div class="polaroid">
            <div class="pinza"></div>
            <img src="{img_src}" alt="Recuerdo" loading="lazy" />
            <p class="texto-polaroid">{frase_actual}</p>
        </div>
    </div>
    """

# --- ESTRUCTURA HTML Y CSS ---
html_completo = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600&family=Montserrat:wght@800;900&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; }}

html, body {{
    width: 100vw;
    height: 100vh;
    margin: 0;
    padding: 0;
    overflow: hidden;
    background: radial-gradient(circle at center, #1b003a 0%, #080014 100%);
    font-family: 'Montserrat', sans-serif;
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
}}

.top-controls {{
    position: fixed;
    top: 20px;
    right: 25px;
    z-index: 1000;
    display: flex;
    gap: 12px;
}}

.btn-control {{
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.25);
    color: #ffffff;
    padding: 12px 22px;
    border-radius: 30px;
    font-family: 'Montserrat', sans-serif;
    font-size: 0.85rem;
    font-weight: 800;
    cursor: pointer;
    box-shadow: 0 0 15px rgba(255, 0, 127, 0.3);
    transition: all 0.3s ease;
    outline: none;
    display: flex;
    align-items: center;
    gap: 6px;
}}

.btn-control:hover {{
    background: rgba(255, 0, 127, 0.4);
    border-color: #00ffff;
    box-shadow: 0 0 25px rgba(0, 255, 255, 0.8);
    transform: scale(1.08);
}}

.btn-control.active {{
    background: rgba(0, 255, 255, 0.25);
    border-color: #00ffff;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.8);
}}

.corazon-flotante {{
    position: fixed;
    bottom: -40px;
    user-select: none;
    pointer-events: none;
    z-index: 0;
    animation: flotarHaciaArriba linear forwards;
}}

@keyframes flotarHaciaArriba {{
    0% {{ transform: translateY(0) rotate(0deg); opacity: 1; }}
    100% {{ transform: translateY(-120vh) rotate(360deg); opacity: 0; }}
}}

.titulo-container {{
    text-align: center;
    margin-top: 25px;
    z-index: 2;
}}

.titulo-3d {{
    font-family: 'Montserrat', sans-serif;
    font-size: 4.2rem;
    font-weight: 900;
    letter-spacing: 8px;
    background: linear-gradient(120deg, #ff007f, #ffd700, #00ffff, #a855f7);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline-block;
    animation: moverColores 5s linear infinite, flotarYLatir 3.5s ease-in-out infinite;
    margin: 0;
}}

@keyframes moverColores {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

@keyframes flotarYLatir {{
    0%, 100% {{
        transform: translateY(0) scale(1);
        filter: drop-shadow(0px 0px 15px rgba(255, 0, 127, 0.8));
    }}
    50% {{
        transform: translateY(-12px) scale(1.04);
        filter: drop-shadow(0px 0px 30px rgba(0, 255, 255, 1));
    }}
}}

.galeria-caja {{
    width: 100%;
    overflow: hidden;
    position: relative;
    padding: 70px 0 60px 0;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
    z-index: 2;
}}

.cuerda {{
    position: absolute;
    top: 85px;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #8a5a36, #d2b48c, #8a5a36);
    box-shadow: 0 3px 8px rgba(0,0,0,0.6);
    z-index: 1;
}}

.riel-desplazamiento {{
    display: flex;
    width: max-content;
    animation: desplazar 150s linear infinite;
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
    margin: 0 35px;
    position: relative;
}}

.pinza {{
    position: absolute;
    top: -20px;
    left: 50%;
    transform: translateX(-50%);
    width: 15px;
    height: 32px;
    background: linear-gradient(to bottom, #d2b48c, #a87e50);
    border-radius: 3px;
    box-shadow: 0 3px 6px rgba(0,0,0,0.5);
    z-index: 10;
}}

.polaroid {{
    background: #ffffff;
    padding: 14px 14px 20px 14px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.7);
    border-radius: 6px;
    width: 250px;
    display: flex;
    flex-direction: column;
    align-items: center;
    transform-origin: top center;
    animation: balanceoFoto 3.5s ease-in-out infinite alternate;
    transition: transform 0.3s ease;
}}

.polaroid:hover {{
    transform: scale(1.05) rotate(0deg) !important;
    z-index: 20;
}}

.item-cuerda:nth-child(even) .polaroid {{ animation-delay: -1.75s; }}
.item-cuerda:nth-child(3n) .polaroid {{ animation-duration: 4.2s; animation-delay: -0.9s; }}

@keyframes balanceoFoto {{
    0% {{ transform: rotate(-5deg); }}
    100% {{ transform: rotate(5deg); }}
}}

.polaroid img {{
    width: 222px;
    height: 255px;
    object-fit: cover;
    border-radius: 3px;
    display: block;
}}

.texto-polaroid {{
    font-family: 'Caveat', cursive, sans-serif;
    font-size: 1.45rem;
    color: #1a1a1a;
    text-align: center;
    margin: 14px 0 0 0;
    line-height: 1.2;
    font-weight: 600;
}}

.foco {{
    position: absolute;
    top: -50px;
    width: 24px;
    height: 35px;
    border-radius: 50% 50% 45% 45%;
    z-index: 5;
}}

.foco-rojo {{ background: #ff4d4d; box-shadow: 0 0 18px #ff4d4d, 0 0 35px #ff4d4d; }}
.foco-azul {{ background: #4da6ff; box-shadow: 0 0 18px #4da6ff, 0 0 35px #4da6ff; }}
.foco-dorado {{ background: #ffd700; box-shadow: 0 0 18px #ffd700, 0 0 35px #ffd700; }}
.foco-verde {{ background: #4dff4d; box-shadow: 0 0 18px #4dff4d, 0 0 35px #4dff4d; }}
.foco-morado {{ background: #a855f7; box-shadow: 0 0 18px #a855f7, 0 0 35px #a855f7; }}

.frase-bottom {{
    text-align: center;
    margin-bottom: 30px;
    font-family: 'Montserrat', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff;
    text-shadow: 0 0 15px rgba(0, 255, 255, 0.9), 0 0 25px rgba(255, 0, 127, 0.7);
    z-index: 2;
}}
</style>
</head>
<body>

<audio id="musicaFondo" loop src="{musica_b64}"></audio>

<div class="top-controls">
    <button id="btnMusica" class="btn-control" onclick="toggleMusica()">
        🎵 Música: OFF
    </button>
    <button id="btnFullscreen" class="btn-control" onclick="toggleFullscreen()">
        ⛶ Pantalla Completa
    </button>
</div>

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

<script>
const audio = document.getElementById('musicaFondo');
const btnMusica = document.getElementById('btnMusica');

function toggleMusica() {{
    if (audio.paused) {{
        audio.play();
        btnMusica.innerHTML = '🎶 Música: ON';
        btnMusica.classList.add('active');
    }} else {{
        audio.pause();
        btnMusica.innerHTML = '🎵 Música: OFF';
        btnMusica.classList.remove('active');
    }}
}}

function toggleFullscreen() {{
    if (!document.fullscreenElement && !document.webkitFullscreenElement) {{
        const elem = document.documentElement;
        if (elem.requestFullscreen) {{
            elem.requestFullscreen();
        }} else if (elem.webkitRequestFullscreen) {{
            elem.webkitRequestFullscreen();
        }}
    }} else {{
        if (document.exitFullscreen) {{
            document.exitFullscreen();
        }} else if (document.webkitExitFullscreen) {{
            document.webkitExitFullscreen();
        }}
    }}
}}

function actualizarBoton() {{
    const btn = document.getElementById('btnFullscreen');
    if (document.fullscreenElement || document.webkitFullscreenElement) {{
        btn.innerHTML = '🗗 Salir';
    }} else {{
        btn.innerHTML = '⛶ Pantalla Completa';
    }}
}}

document.addEventListener('fullscreenchange', actualizarBoton);
document.addEventListener('webkitfullscreenchange', actualizarBoton);

const iconosCorazones = ['❤️', '💖', '💕', '💗', '💓', '✨', '🌹'];

function crearCorazon() {{
    const corazon = document.createElement('div');
    corazon.classList.add('corazon-flotante');
    corazon.innerHTML = iconosCorazones[Math.floor(Math.random() * iconosCorazones.length)];
    corazon.style.left = Math.random() * 100 + 'vw';
    
    const tamano = Math.random() * 22 + 16;
    corazon.style.fontSize = tamano + 'px';
    
    const duracion = Math.random() * 5 + 6;
    corazon.style.animationDuration = duracion + 's';
    corazon.style.opacity = Math.random() * 0.7 + 0.3;
    
    document.body.appendChild(corazon);
    
    setTimeout(() => {{
        corazon.remove();
    }}, duracion * 1000);
}}

setInterval(crearCorazon, 300);
</script>

</body>
</html>
"""

components.html(html_completo)
