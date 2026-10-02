import os
import base64
import io
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
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
    st.warning("No se encontraron imágenes en la carpeta de Drive o aún se están procesando.")
    st.stop()

# --- CONSTRUCCIÓN DE LA GALERÍA CON CUERDA Y FOCOS ---
focos_colores = ["foco-rojo", "foco-azul", "foco-dorado", "foco-verde", "foco-morado"]
items_galeria = imagenes_b64 + imagenes_b64  # Duplicar para el efecto de bucle infinito

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

# --- ESTRUCTURA COMPLETA HTML, CSS Y ANIMACIONES ---
html_completo = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600&family=Montserrat:wght@800;900&display=swap" rel="stylesheet">
<style>
body {{
    background-color: #0c001f;
    margin: 0;
    padding: 10px;
    font-family: 'Montserrat', sans-serif;
    color: white;
    overflow-x: hidden;
    position: relative;
}}

/* BOTÓN DE PANTALLA COMPLETA */
.btn-fullscreen {{
    position: fixed;
    top: 15px;
    right: 15px;
    z-index: 1000;
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 0, 127, 0.5);
    color: #ffffff;
    padding: 10px 18px;
    border-radius: 25px;
    font-family: 'Montserrat', sans-serif;
    font-size: 0.85rem;
    font-weight: 800;
    cursor: pointer;
    box-shadow: 0 0 12px rgba(255, 0, 127, 0.4);
    transition: all 0.3s ease;
    outline: none;
    display: flex;
    align-items: center;
    gap: 8px;
}}

.btn-fullscreen:hover {{
    background: rgba(255, 0, 127, 0.3);
    border-color: #00ffff;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.8);
    transform: scale(1.05);
}}

/* Corazones flotantes del fondo */
.corazon-flotante {{
    position: fixed;
    bottom: -30px;
    user-select: none;
    pointer-events: none;
    z-index: 0;
    animation: flotarHaciaArriba linear forwards;
}}

@keyframes flotarHaciaArriba {{
    0% {{
        transform: translateY(0) rotate(0deg);
        opacity: 1;
    }}
    100% {{
        transform: translateY(-115vh) rotate(360deg);
        opacity: 0;
    }}
}}

.titulo-container {{
    text-align: center;
    margin-top: 15px;
    margin-bottom: 25px;
    position: relative;
    z-index: 2;
}}

/* Título con movimiento y resplandor neón */
.titulo-3d {{
    font-family: 'Montserrat', sans-serif;
    font-size: 3.8rem;
    font-weight: 900;
    letter-spacing: 6px;
    background: linear-gradient(120deg, #ff007f, #ffd700, #00ffff, #a855f7);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline-block;
    animation: moverColores 5s linear infinite, flotarYLatir 3s ease-in-out infinite;
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
        filter: drop-shadow(0px 0px 12px rgba(255, 0, 127, 0.8));
    }}
    50% {{
        transform: translateY(-10px) scale(1.05);
        filter: drop-shadow(0px 0px 25px rgba(0, 255, 255, 1));
    }}
}}

.galeria-caja {{
    width: 100%;
    overflow: hidden;
    position: relative;
    padding: 60px 0 50px 0;
    background: radial-gradient(circle, rgba(26,0,51,0.85) 0%, rgba(12,0,31,0.95) 100%);
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    z-index: 2;
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
    margin: 0 30px;
    position: relative;
}}

.pinza {{
    position: absolute;
    top: -18px;
    left: 50%;
    transform: translateX(-50%);
    width: 14px;
    height: 30px;
    background: #d2b48c;
    border-radius: 2px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.4);
    z-index: 10;
}}

/* POLAROID CON EFECTO DE BALANCEO EN LA CUERDA */
.polaroid {{
    background: #ffffff;
    padding: 12px 12px 18px 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.6);
    border-radius: 4px;
    width: 230px;
    display: flex;
    flex-direction: column;
    align-items: center;
    transform-origin: top center;
    animation: balanceoFoto 3.2s ease-in-out infinite alternate;
}}

.item-cuerda:nth-child(even) .polaroid {{
    animation-delay: -1.6s;
}}

.item-cuerda:nth-child(3n) .polaroid {{
    animation-duration: 4s;
    animation-delay: -0.8s;
}}

@keyframes balanceoFoto {{
    0% {{
        transform: rotate(-6deg);
    }}
    100% {{
        transform: rotate(6deg);
    }}
}}

.polaroid img {{
    width: 206px;
    height: 240px;
    object-fit: cover;
    border-radius: 2px;
    display: block;
}}

.texto-polaroid {{
    font-family: 'Caveat', cursive, sans-serif;
    font-size: 1.35rem;
    color: #222222;
    text-align: center;
    margin: 12px 0 0 0;
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
    position: relative;
    z-index: 2;
}}
</style>
</head>
<body>

<!-- BOTÓN PARA ACTIVAR PANTALLA COMPLETA -->
<button id="btnFullscreen" class="btn-fullscreen" onclick="toggleFullscreen()">
    ⛶ Pantalla Completa
</button>

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
// Función para alternar Pantalla Completa
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

// Cambiar el texto del botón al entrar o salir
function actualizarBoton() {{
    const btn = document.getElementById('btnFullscreen');
    if (document.fullscreenElement || document.webkitFullscreenElement) {{
        btn.innerHTML = '🗗 Salir de Pantalla Completa';
    }} else {{
        btn.innerHTML = '⛶ Pantalla Completa';
    }}
}}

document.addEventListener('fullscreenchange', actualizarBoton);
document.addEventListener('webkitfullscreenchange', actualizarBoton);

// Corazones flotantes en el fondo
const iconosCorazones = ['❤️', '💖', '💕', '💗', '💓', '✨'];

function crearCorazon() {{
    const corazon = document.createElement('div');
    corazon.classList.add('corazon-flotante');
    corazon.innerHTML = iconosCorazones[Math.floor(Math.random() * iconosCorazones.length)];
    corazon.style.left = Math.random() * 100 + 'vw';
    
    const tamano = Math.random() * 20 + 15;
    corazon.style.fontSize = tamano + 'px';
    
    const duracion = Math.random() * 5 + 6;
    corazon.style.animationDuration = duracion + 's';
    corazon.style.opacity = Math.random() * 0.7 + 0.3;
    
    document.body.appendChild(corazon);
    
    setTimeout(() => {{
        corazon.remove();
    }}, duracion * 1000);
}}

setInterval(crearCorazon, 350);
</script>

</body>
</html>
"""

components.html(html_completo, height=620, scrolling=False)
