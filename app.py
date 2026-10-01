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
/* Importar tipografía Montserrat para el estilo 3D */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&display=swap');

/* --- TÍTULO 3D, MULTICOLOR, ANIMADO Y CON BRILLO --- */
.titulo-container {
    text-align: center;
    margin-top: -10px;
    margin-bottom: 30px;
    perspective: 800px;
}

.titulo-3d {
    font-family: 'Montserrat', 'Arial Black', sans-serif;
    font-size: 3.8rem;
    font-weight: 900;
    letter-spacing: 6px;
    display: inline-block;
    
    /* Texto con gradiente de colores en movimiento */
    background: linear-gradient(120deg, #ff007f, #ffd700, #00ffff, #a855f7, #ff007f);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    
    /* Animaciones combinadas: Giro 3D, Gradiente y Resplandor */
    animation: 
        animGiro3D 4s ease-in-out infinite alternate,
        moverColores 5s linear infinite,
        brilloNeon 2.5s ease-in-out infinite alternate;
        
    filter: drop-shadow(0px 10px 15px rgba(0, 0, 0, 0.5));
}

/* Movimiento 3D y flotación */
@keyframes animGiro3D {
    0% {
        transform: rotateX(15deg) rotateY(-12deg) translateY(0px) scale(0.98);
    }
    50% {
        transform: rotateX(0deg) rotateY(10deg) translateY(-8px) scale(1.02);
    }
    100% {
        transform: rotateX(-15deg) rotateY(-8deg) translateY(-15px) scale(1.05);
    }
}

/* Desplazamiento continuo de los colores del gradiente */
@keyframes moverColores {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Efecto de resplandor y brillo multicolor */
@keyframes brilloNeon {
    0% {
        filter: drop-shadow(0px 0px 8px rgba(255, 0, 127, 0.7)) drop-shadow(0px 0px 18px rgba(255, 215, 0, 0.5));
    }
    100% {
        filter: drop-shadow(0px 0px 20px rgba(0, 255, 255, 0.9)) drop-shadow(0px 0px 32px rgba(168, 85, 247, 0.8));
    }
}

/* Centrado de imágenes en columnas */
div[data-testid="stImage"] {
    display: flex;
    justify-content: center;
    align-items: center;
}

/* Base de imágenes */
div[data-testid="stImage"] img {
    border-radius: 20px;
    max-height: 52vh;
    width: 100%;
    object-fit: cover;
    transform-style: preserve-3d;
}

/* --- MARCOS DE COLORES INDIVIDUALES Y RESPLANDOR PARA CADA FOTO --- */
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
    0% { box-shadow: 0px 0px 15px rgba(255, 42, 117, 0.5); transform: translateY(0px); }
    100% { box-shadow: 0px 0px 35px rgba(255, 42, 117, 1), 0px 0px 15px #ff2a75; transform: translateY(-8px); }
}

@keyframes resplandorDorado {
    0% { box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.5); transform: translateY(0px); }
    100% { box-shadow: 0px 0px 35px rgba(255, 215, 0, 1), 0px 0px 15px #ffd700; transform: translateY(-8px); }
}

@keyframes resplandorPurpura {
    0% { box-shadow: 0px 0px 15px rgba(168, 85, 247, 0.5); transform: translateY(0px); }
    100% { box-shadow: 0px 0px 35px rgba(168, 85, 247, 1), 0px 0px 15px #a855f7; transform: translateY(-8px); }
}

/* --- FRASES CON ESTILO IDÉNTICO AL TÍTULO (3D, GRADIENTE Y BRILLO) --- */
.frase-amor-container {
    text-align: center;
    margin-top: 25px;
    margin-bottom: 20px;
    padding: 18px 25px;
    background: rgba(15, 15, 25, 0.45);
    border-radius: 22px;
    border: 1.5px solid rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.4);
    min-height: 90px;
    display: flex;
    align-items: center;
    justify-content: center;
    perspective: 800px;
}

.frase-texto-3d {
    font-family: 'Montserrat', 'Arial Black', sans-serif;
    font-size: 1.8rem;
    font-weight: 900;
    letter-spacing: 2px;
    display: inline-block;
    
    /* Mismo gradiente multicolor que el título */
    background: linear-gradient(120deg, #ff007f, #ffd700, #00ffff, #a855f7, #ff007f);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    
    /* Mismo movimiento de colores y resplandor neón */
    animation: 
        moverColores 5s linear infinite,
        brilloNeon 2.5s ease-in-out infinite alternate,
        animGiro3D 4s ease-in-out infinite alternate;
}

/* Cursor parpadeante */
.cursor-tipeo {
    font-size: 1.8rem;
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

/* Lluvia de lunas, estrellas y corazones */
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

<!-- RENDERIZADO DEL TÍTULO 3D MULTICOLOR -->
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

# --- LISTA DE FRASES DE AMOR ---
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

# --- CONEXIÓN A GOOGLE DRIVE ---
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
        
        col1, col2, col3 = st.columns(3)
        p1, p2, p3 = col1.empty(), col2.empty(), col3.empty()
        placeholders = [p1, p2, p3]
        
        contenedor_frase = st.empty()
        
        while True:
            for g_idx, trio in enumerate(grupos_de_tres):
                frase_actual = FRASES_DE_AMOR[g_idx % len(FRASES_DE_AMOR)]
                
                for p in placeholders:
                    p.empty()
                
                for i, ruta in enumerate(trio):
                    img = Image.open(ruta)
                    img = ImageOps.exif_transpose(img)
                    placeholders[i].image(img, use_container_width=True)
                
                texto_parcial = ""
                velocidad_letra = 0.035
                
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
                
                tiempo_escritura = len(frase_actual) * velocidad_letra
                tiempo_restante = max(2.0, 6.0 - tiempo_escritura)
                time.sleep(tiempo_restante)
    else:
        st.warning("No se encontraron fotos en la carpeta de Drive.")
