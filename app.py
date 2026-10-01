import os
import time
import streamlit as st
from PIL import Image, ImageOps
import gdown

# Configuración de la página
st.set_page_config(page_title="RECUERDOS", layout="wide")

# --- ANIMACIONES Y ESTILOS CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&display=swap');

/* --- TÍTULO RECUERDOS --- */
.titulo-container {
    text-align: center;
    margin-top: -10px;
    margin-bottom: 25px;
}

.titulo-3d {
    font-family: 'Montserrat', 'Arial Black', sans-serif;
    font-size: 3.8rem;
    font-weight: 900;
    letter-spacing: 6px;
    display: inline-block;
    
    /* Gradiente multicolor */
    background: linear-gradient(120deg, #ff007f, #ffd700, #00ffff, #a855f7, #ff007f);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    
    /* Animación de movimiento de Izquierda a Derecha, colores y brillo */
    animation: 
        moverIzquierdaDerecha 4s ease-in-out infinite alternate,
        moverColores 5s linear infinite,
        brilloNeon 2.5s ease-in-out infinite alternate;
}

/* Animación exclusiva de Izquierda a Derecha */
@keyframes moverIzquierdaDerecha {
    0% {
        transform: translateX(-35px);
    }
    100% {
        transform: translateX(35px);
    }
}

/* Movimiento de los colores del gradiente */
@keyframes moverColores {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Resplandor neón */
@keyframes brilloNeon {
    0% {
        filter: drop-shadow(0px 0px 8px rgba(255, 0, 127, 0.7)) drop-shadow(0px 0px 18px rgba(255, 215, 0, 0.5));
    }
    100% {
        filter: drop-shadow(0px 0px 20px rgba(0, 255, 255, 0.9)) drop-shadow(0px 0px 32px rgba(168, 85, 247, 0.8));
    }
}

/* Centrado e imágenes */
div[data-testid="stImage"] {
    display: flex;
    justify-content: center;
    align-items: center;
}

div[data-testid="stImage"] img {
    border-radius: 20px;
    max-height: 50vh;
    width: 100%;
    object-fit: cover;
    transform-style: preserve-3d;
}

/* Marcos de fotos con resplandor */
div[data-testid="column"]:nth-child(1) div[data-testid="stImage"] img {
    border: 4px solid #ff2a75;
    animation: girarFoto 1.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards, resplandorRosa 3s ease-in-out infinite alternate 1.2s;
}

div[data-testid="column"]:nth-child(2) div[data-testid="stImage"] img {
    border: 4px solid #ffd700;
    animation: girarFoto 1.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards, resplandorDorado 3s ease-in-out infinite alternate 1.2s;
}

div[data-testid="column"]:nth-child(3) div[data-testid="stImage"] img {
    border: 4px solid #a855f7;
    animation: girarFoto 1.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards, resplandorPurpura 3s ease-in-out infinite alternate 1.2s;
}

@keyframes girarFoto {
    0% { transform: perspective(800deg) rotateY(-180deg) scale(0.3); opacity: 0; }
    100% { transform: perspective(800deg) rotateY(0deg) scale(1); opacity: 1; }
}

@keyframes resplandorRosa {
    0% { box-shadow: 0px 0px 15px rgba(255, 42, 117, 0.5); }
    100% { box-shadow: 0px 0px 35px rgba(255, 42, 117, 1); }
}

@keyframes resplandorDorado {
    0% { box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.5); }
    100% { box-shadow: 0px 0px 35px rgba(255, 215, 0, 1); }
}

@keyframes resplandorPurpura {
    0% { box-shadow: 0px 0px 15px rgba(168, 85, 247, 0.5); }
    100% { box-shadow: 0px 0px 35px rgba(168, 85, 247, 1); }
}

/* --- FRASES EN LA PARTE INFERIOR: SOLO LETRAS CON MOVIMIENTO IZQ-DER --- */
.frase-amor-container {
    text-align: center;
    margin-top: 35px;
    margin-bottom: 25px;
    padding: 0px;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    backdrop-filter: none !important;
    min-height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.frase-texto-3d {
    font-family: 'Montserrat', 'Arial Black', sans-serif;
    font-size: 2rem;
    font-weight: 900;
    letter-spacing: 2px;
    display: inline-block;
    
    background: linear-gradient(120deg, #ff007f, #ffd700, #00ffff, #a855f7, #ff007f);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    
    /* Movimiento de izquierda a derecha, gradiente continuo y resplandor neón */
    animation: 
        moverIzquierdaDerecha 3.5s ease-in-out infinite alternate,
        moverColores 5s linear infinite,
        brilloNeon 2.5s ease-in-out infinite alternate;
}

/* Cursor de tipeo */
.cursor-tipeo {
    font-size: 2rem;
    font-weight: 900;
    color: #00ffff;
    margin-left: 4px;
    animation: parpadeo 0.6s infinite;
    text-shadow: 0 0 10px #00ffff;
}

@keyframes parpadeo {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}

/* Elementos flotantes de fondo (estrellas, luna, corazones) */
.sky-container {
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    pointer-events: none; overflow: hidden; z-index: 99999;
}

.sky-item {
    position: absolute; 
    bottom: -60px; 
    animation: floatUp 3.5s linear infinite; 
    opacity: 0.9;
    filter: drop-shadow(0px 0px 8px rgba(255, 230, 150, 0.8));
}

@keyframes floatUp {
    0% { transform: translateY(0) rotate(0deg) scale(0.8); opacity: 0.9; }
    50% { opacity: 1; transform: translateY(-50vh) rotate(180deg) scale(1.1); }
    100% { transform: translateY(-108vh) rotate(360deg) scale(0.9); opacity: 0; }
}
</style>

<!-- TÍTULO EN LA PARTE SUPERIOR -->
<div class="titulo-container">
    <h1 class="titulo-3d">RECUERDOS</h1>
</div>

<div class="sky-container">
    <div class="sky-item" style="left: 6%; font-size: 48px; animation-delay: 0s; animation-duration: 4s;">🌙</div>
    <div class="sky-item" style="left: 38%; font-size: 54px; animation-delay: 1.5s; animation-duration: 4.5s;">🌕</div>
    <div class="sky-item" style="left: 72%; font-size: 50px; animation-delay: 0.8s; animation-duration: 4.2s;">🌙</div>
    <div class="sky-item" style="left: 14%; font-size: 38px; animation-delay: 0.5s; animation-duration: 3.2s;">✨</div>
    <div class="sky-item" style="left: 28%; font-size: 44px; animation-delay: 1.8s; animation-duration: 3.8s;">⭐</div>
    <div class="sky-item" style="left: 50%; font-size: 40px; animation-delay: 0.2s; animation-duration: 3.4s;">🌟</div>
    <div class="sky-item" style="left: 62%; font-size: 42px; animation-delay: 2.2s; animation-duration: 3.9s;">✨</div>
    <div class="sky-item" style="left: 84%; font-size: 46px; animation-delay: 1.1s; animation-duration: 3.6s;">⭐</div>
    <div class="sky-item" style="left: 94%; font-size: 38px; animation-delay: 0.4s; animation-duration: 3.1s;">🌟</div>
    <div class="sky-item" style="left: 20%; font-size: 45px; animation-delay: 1s; animation-duration: 3.7s;">💖</div>
    <div class="sky-item" style="left: 44%; font-size: 48px; animation-delay: 2s; animation-duration: 4s;">❤️</div>
    <div class="sky-item" style="left: 78%; font-size: 42px; animation-delay: 0.7s; animation-duration: 3.5s;">💕</div>
</div>
""", unsafe_allow_html=True)

# --- LISTA DE FRASES ---
FRASES_DE_AMOR = [
    "Eres mi lugar favorito en el mundo. ❤️✨",
    "Cada día a tu lado es un regalo hermoso. 💖🌙",
    "Gracias por hacer mi vida más bonita. 💕⭐",
    "Tú y yo, mi momento preferido del día. 💗🌟",
    "Contigo todo es infinitamente mejor. 💘✨",
    "Mi sonrisa favorita es la que tú me sacas. ✨🌙",
    "El mejor recuerdo siempre es el que construyo a tu lado. 🥰⭐",
    "Simplemente gracias por existir y estar en mi vida. 🌹🌟",
    "Juntos es mi lugar favorito. ❤️✨",
    "Si pudiera elegir un momento, elegiría cualquier instante contigo. 💫🌙",
    "Eres la historia más bonita que el destino escribió en mi vida. 📖✨",
    "Mi felicidad tiene tu nombre y tu sonrisa. 🥰⭐",
    "Amarte es la decisión más fácil y hermosa que he tomado. 💖🌟",
    "En tus ojos encontré mi hogar y en tu abrazo mi paz. 💓🌙",
    "Cada segundo a tu lado vale por mil recuerdos. ⏳❤️✨",
    "No necesito el mundo entero, solo tu mano en la mía. 🤝💕⭐",
    "Le das color, luz y sentido a todos mis días. ☀️💗🌟",
    "Coincidir contigo es lo mejor que me ha pasado. 🌸✨🌙",
    "Eres mi presente, mi futuro y mi pensamiento favorito de cada día. 💖⭐",
    "Haces que lo ordinario se vuelva extraordinario. 💘🌟"
]

# --- DRIVE ---
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

with st.spinner("Descargando fotos desde Google Drive... ❤️✨"):
    descargar_fotos_de_drive()

# --- REPRODUCCIÓN AUTOMÁTICA ---
if os.path.exists(CARPETA_FOTOS):
    archivos_completos = []
    
    for root, dirs, files in os.walk(CARPETA_FOTOS):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'webp')):
                archivos_completos.append(os.path.join(root, file))
    
    if archivos_completos:
        archivos_completos.sort()
        grupos_de_tres = [archivos_completos[i:i + 3] for i in range(0, len(archivos_completos), 3)]
        
        # 1. TRES COLUMNAS PARA LAS FOTOS EN EL CENTRO
        col1, col2, col3 = st.columns(3)
        p1, p2, p3 = col1.empty(), col2.empty(), col3.empty()
        placeholders = [p1, p2, p3]
        
        # 2. CONTENEDOR PARA LAS FRASES JUSTO EN LA PARTE INFERIOR
        contenedor_frase = st.empty()
        
        while True:
            for g_idx, trio in enumerate(grupos_de_tres):
                frase_actual = FRASES_DE_AMOR[g_idx % len(FRASES_DE_AMOR)]
                
                # Limpiar fotos previas
                for p in placeholders:
                    p.empty()
                
                # Mostrar el grupo de fotos
                for i, ruta in enumerate(trio):
                    img = Image.open(ruta)
                    img = ImageOps.exif_transpose(img)
                    placeholders[i].image(img, use_container_width=True)
                
                # Efecto de máquina de escribir para la frase en la parte de abajo
                texto_parcial = ""
                velocidad_letra = 0.04
                
                for letra in frase_actual:
                    texto_parcial += letra
                    contenedor_frase.markdown(
                        f'''
                        <div class="frase-amor-container">
                            <span class="frase-texto-3d">{texto_parcial}</span>
                            <span class="cursor-tipeo">|</span>
                        </div>
                        ''',
                        unsafe_allow_html=True
                    )
                    time.sleep(velocidad_letra)
                
                contenedor_frase.markdown(
                    f'''
                    <div class="frase-amor-container">
                        <span class="frase-texto-3d">{frase_actual}</span>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
                
                # DURACIÓN DUPLICADA: Permanece 12 segundos visibles en pantalla por cada grupo
                tiempo_escritura = len(frase_actual) * velocidad_letra
                tiempo_restante = max(6.0, 12.0 - tiempo_escritura)
                time.sleep(tiempo_restante)
    else:
        st.warning("No se encontraron fotos en la carpeta de Drive.")
