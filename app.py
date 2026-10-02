import os
import base64
import io
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import gdown

# 1. Configuración de página
st.set_page_config(
    page_title="GALERÍA DE RECUERDOS", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Ocultar interfaz por defecto de Streamlit
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

# --- CONFIGURACIÓN PERSONALIZABLE ---
# 📅 Cambia esto por la fecha en que iniciaron su relación (Año, Mes, Día)
FECHA_INICIO = "2023-01-01T00:00:00" 

# 🎵 Enlace directo a audio MP3 (puedes usar un enlace público de Dropbox, GitHub, o Drive directo)
URL_MUSICA = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

# 💬 Frases para las fotos
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

# --- DESCARGA DE FOTOS DE DRIVE ---
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

with st.spinner("Cargando magia... ❤️✨"):
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
            img.thumbnail((450, 500))
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=82, optimize=True)
            encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')
            return f"data:image/jpeg;base64,{encoded}"
    except Exception:
        return ""

imagenes_b64 = [get_optimized_image_base64(f) for f in archivos_fotos if get_optimized_image_base64(f)]

if not imagenes_b64:
    st.warning("No se encontraron imágenes en la carpeta.")
    st.stop()

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
        <div class="polaroid" onclick="abrirModal('{img_src}', '{frase_actual}')">
            <div class="pinza"></div>
            <img src="{img_src}" alt="Recuerdo" loading="lazy" />
            <p class="texto-polaroid">{frase_actual}</p>
        </div>
    </div>
    """

# --- ESTRUCTURA HTML & CSS ULTRA PREMIUM ---
html_completo = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600&family=Montserrat:wght@700;800;900&display=swap" rel="stylesheet">
<style>
* {{
    box-sizing: border-box;
}}

html, body {{
    width: 100vw;
    height: 100vh;
    margin: 0;
    padding: 0;
    overflow: hidden;
    background: radial-gradient(circle at center, #1c0038 0%, #070010 100%);
    font-family: 'Montserrat', sans-serif;
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    user-select: none;
}}

/* BOTONES SUPERIORES FLOTANTES */
.top-controls {{
    position: fixed;
    top: 18px;
    right: 20px;
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
    padding: 10px 18px;
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

/* CONTADOR DE TIEMPO JUNTOS */
.contador-box {{
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 0, 127, 0.3);
    border-radius: 20px;
    padding: 6px 20px;
    margin-top: 12px;
    box-shadow: 0 0 20px rgba(255, 0, 127, 0.2);
    display: inline-block;
}}

.contador-texto {{
    font-size: 0.95rem;
    font-weight: 800;
    letter-spacing: 1px;
    color: #ffb3da;
    text-shadow: 0 0 8px rgba(255, 0, 127, 0.8);
}}

/* ENCABEZADO */
.titulo-container {{
    text-align: center;
    margin-top: 15px;
    z-index: 2;
}}

.titulo-3d {{
    font-size: 3.8rem;
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
        transform: translateY(-8px) scale(1.03);
        filter: drop-shadow(0px 0px 30px rgba(0, 255, 255, 1));
    }}
}}

/* GALERÍA DE FOTOS */
.galeria-caja {{
    width: 100%;
    overflow: hidden;
    position: relative;
    padding: 65px 0 55px 0;
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(8px);
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
    z-index: 2;
}}

.cuerda {{
    position: absolute;
    top: 80px;
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
    animation: desplazar 140s linear infinite;
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
    width: 245px;
    display: flex;
    flex-direction: column;
    align-items: center;
    transform-origin: top center;
    animation: balanceoFoto 3.5s ease-in-out infinite alternate;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    cursor: pointer;
}}

.polaroid:hover {{
    transform: scale(1.1) rotate(0deg) !important;
    box-shadow: 0 0 30px rgba(0, 255, 255, 0.8), 0 15px 35px rgba(0, 0, 0, 0.8);
    z-index: 20;
}}

.item-cuerda:nth-child(even) .polaroid {{ animation-delay: -1.75s; }}
.item-cuerda:nth-child(3n) .polaroid {{ animation-duration: 4.2s; animation-delay: -0.9s; }}

@keyframes balanceoFoto {{
    0% {{ transform: rotate(-5deg); }}
    100% {{ transform: rotate(5deg); }}
}}

.polaroid img {{
    width: 217px;
    height: 250px;
    object-fit: cover;
    border-radius: 3px;
    display: block;
}}

.texto-polaroid {{
    font-family: 'Caveat', cursive;
    font-size: 1.45rem;
    color: #111111;
    text-align: center;
    margin: 12px 0 0 0;
    line-height: 1.2;
    font-weight: 600;
}}

/* FOCOS */
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

/* MODAL DE FOTO GRANDE (LIGHTBOX) */
.modal-overlay {{
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background: rgba(0, 0, 0, 0.85);
    backdrop-filter: blur(15px);
    z-index: 2000;
    display: none;
    justify-content: center;
    align-items: center;
    opacity: 0;
    transition: opacity 0.4s ease;
}}

.modal-content {{
    background: #ffffff;
    padding: 20px 20px 25px 20px;
    border-radius: 12px;
    max-width: 90vw;
    max-height: 85vh;
    box-shadow: 0 0 50px rgba(0, 255, 255, 0.6), 0 0 100px rgba(255, 0, 127, 0.4);
    display: flex;
    flex-direction: column;
    align-items: center;
    transform: scale(0.7);
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
}}

.modal-overlay.active {{
    display: flex;
    opacity: 1;
}}

.modal-overlay.active .modal-content {{
    transform: scale(1);
}}

.modal-content img {{
    max-width: 70vw;
    max-height: 60vh;
    object-fit: contain;
    border-radius: 6px;
}}

.modal-texto {{
    font-family: 'Caveat', cursive;
    font-size: 2.2rem;
    color: #111111;
    margin-top: 15px;
    text-align: center;
}}

.btn-cerrar {{
    position: absolute;
    top: -15px;
    right: -15px;
    background: #ff007f;
    color: white;
    border: none;
    border-radius: 50%;
    width: 38px;
    height: 38px;
    font-size: 1.2rem;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 0 15px rgba(255, 0, 127, 0.8);
}}

/* CORAZONES FLOTANTES */
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

.frase-bottom {{
    text-align: center;
    margin-bottom: 25px;
    font-size: 1.8rem;
    font-weight: 800;
    color: #ffffff;
    text-shadow: 0 0 15px rgba(0, 255, 255, 0.9), 0 0 25px rgba(255, 0, 127, 0.7);
    z-index: 2;
}}
</style>
</head>
<body>

<!-- REPRODUCTOR DE AUDIO OCULTO -->
<audio id="musicaFondo" loop src="{URL_MUSICA}"></audio>

<!-- CONTROLES SUPERIORES -->
<div class="top-controls">
    <button id="btnMusica" class="btn-control" onclick="toggleMusica()">
        🎵 Música: OFF
    </button>
    <button id="btnFullscreen" class="btn-control" onclick="toggleFullscreen()">
        ⛶ Pantalla Completa
    </button>
</div>

<!-- ENCABEZADO Y CONTADOR -->
<div class="titulo-container">
    <h1 class="titulo-3d">RECUERDOS</h1>
    <br>
    <div class="contador-box">
        <span class="contador-texto" id="contadorTiempo">Cargando nuestro tiempo... ⏳</span>
    </div>
</div>

<!-- GALERÍA -->
<div class="galeria-caja">
    <div class="cuerda"></div>
    <div class="riel-desplazamiento">
        {html_fotos}
    </div>
</div>

<div class="frase-bottom">
    Nuestra historia en imágenes 💖✨🌙
</div>

<!-- MODAL PARA VER FOTO EN GRANDE -->
<div id="modalFoto" class="modal-overlay" onclick="cerrarModal()">
    <div class="modal-content" onclick="event.stopPropagation()">
        <button class="btn-cerrar" onclick="cerrarModal()">✕</button>
        <img id="imgModal" src="" alt="Recuerdo Grande">
        <div id="textoModal" class="modal-texto"></div>
    </div>
</div>

<script>
// --- LÓGICA DE CONTADOR DE TIEMPO ---
const fechaInicio = new Date("{FECHA_INICIO}");

function actualizarContador() {{
    const ahora = new Date();
    const diferencia = ahora - fechaInicio;

    const dias = Math.floor(diferencia / (1000 * 60 * 60 * 24));
    const horas = Math.floor((diferencia / (1000 * 60 * 60)) % 24);
    const minutos = Math.floor((diferencia / (1000 * 60)) % 60);
    const segundos = Math.floor((diferencia / 1000) % 60);

    document.getElementById('contadorTiempo').innerHTML = 
        `✨ Llevamos ${{dias}} días, ${{horas}}h ${{minutos}}m ${{segundos}}s juntos ✨`;
}}
setInterval(actualizarContador, 1000);
actualizarContador();

// --- LÓGICA DE MÚSICA DE FONDO ---
const audio = document.getElementById('musicaFondo');
const btnMusica = document.getElementById('btnMusica');

function toggleMusica() {{
    if (audio.paused) {{
        audio.play();
        btnMusica.innerHTML = '🎶 Música: ON';
        btnMusica.style.borderColor = '#00ffff';
        btnMusica.style.boxShadow = '0 0 20px rgba(0, 255, 255, 0.8)';
    }} else {{
        audio.pause();
        btnMusica.innerHTML = '🎵 Música: OFF';
        btnMusica.style.borderColor = 'rgba(255, 255, 255, 0.25)';
        btnMusica.style.boxShadow = '0 0 15px rgba(255, 0, 127, 0.3)';
    }}
}}

// --- LÓGICA DE PANTALLA COMPLETA ---
function toggleFullscreen() {{
    if (!document.fullscreenElement && !document.webkitFullscreenElement) {{
        const elem = document.documentElement;
        if (elem.requestFullscreen) {{ elem.requestFullscreen(); }}
        else if (elem.webkitRequestFullscreen) {{ elem.webkitRequestFullscreen(); }}
    }} else {{
        if (document.exitFullscreen) {{ document.exitFullscreen(); }}
        else if (document.webkitExitFullscreen) {{ document.webkitExitFullscreen(); }}
    }}
}}

function actualizarBotonFS() {{
    const btn = document.getElementById('btnFullscreen');
    if (document.fullscreenElement || document.webkitFullscreenElement) {{
        btn.innerHTML = '🗗 Salir';
    }} else {{
        btn.innerHTML = '⛶ Pantalla Completa';
    }}
}}

document.addEventListener('fullscreenchange', actualizarBotonFS);
document.addEventListener('webkitfullscreenchange', actualizarBotonFS);

// --- LÓGICA DE MODAL (LIGHTBOX) ---
function abrirModal(src, texto) {{
    const modal = document.getElementById('modalFoto');
    document.getElementById('imgModal').src = src;
    document.getElementById('textoModal').innerText = texto;
    modal.classList.add('active');
}}

function cerrarModal() {{
    document.getElementById('modalFoto').classList.remove('active');
}}

// --- CORAZONES AL HACER CLIC Y FLOTANTES ---
document.addEventListener('click', function(e) {{
    // Crear corazon al dar clic
    crearCorazonEn(e.clientX, e.clientY);
}});

function crearCorazonEn(x, y) {{
    const corazon = document.createElement('div');
    corazon.innerHTML = '💖';
    corazon.style.position = 'fixed';
    corazon.style.left = (x - 12) + 'px';
    corazon.style.top = (y - 12) + 'px';
    corazon.style.fontSize = '24px';
    corazon.style.pointerEvents = 'none';
    corazon.style.zIndex = '3000';
    corazon.style.transition = 'all 1s ease-out';
    document.body.appendChild(corazon);

    setTimeout(() => {{
        corazon.style.transform = `translate(${(Math.random() - 0.5) * 100}px, -100px) scale(1.5)`;
        corazon.style.opacity = '0';
    }}, 20);

    setTimeout(() => {{ corazon.remove(); }}, 1000);
}}

const iconosCorazones = ['❤️', '💖', '💕', '💗', '💓', '✨', '🌹'];
function crearCorazonFondo() {{
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
    setTimeout(() => {{ corazon.remove(); }}, duracion * 1000);
}}
setInterval(crearCorazonFondo, 300);
</script>

</body>
</html>
"""

components.html(html_completo)
