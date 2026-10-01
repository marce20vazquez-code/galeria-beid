import os
import time
import streamlit as st
from PIL import Image, ImageOps
import gdown

# Configuración de la página
st.set_page_config(page_title="BEID", layout="centered")
st.title("📸 BEID")

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

# --- ANIMACIONES Y ESTILOS CSS ---
st.markdown("""
<style>
/* Centrado de la imagen */
div[data-testid="stImage"] {
    display: flex;
    justify-content: center;
    align-items: center;
}

/* Movimiento suave estilo Ken Burns a la foto */
div[data-testid="stImage"] img {
    border-radius: 20px;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.5);
    max-height: 70vh;
    object-fit: contain;
    animation: kenBurns 6s ease-in-out infinite alternate;
}

@keyframes kenBurns {
    0% { transform: scale(1) translateY(0px); opacity: 0.88; }
    50% { transform: scale(1.05) translateY(-6px); opacity: 1; }
    100% { transform: scale(1.08) translateY(6px); opacity: 0.95; }
}

/* Estilo base de la caja de las frases */
.frase-amor {
    text-align: center;
    font-size: 25px;
    font-weight: 600;
    color: #ff3366;
    font-family: 'Georgia', serif;
    margin-top: 18px;
    margin-bottom: 20px;
    padding: 14px 22px;
    background: rgba(255, 255, 255, 0.12);
    border-radius: 18px;
    border: 1px solid rgba(255, 215, 0, 0.4);
    box-shadow: 0px 8px 25px rgba(255, 51, 102, 0.3);
    backdrop-filter: blur(8px);
    min-height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Cursor parpadeante */
.cursor-tipeo {
    font-weight: 300;
    color: #ffd700;
    margin-left: 3px;
    animation: parpadeo 0.6s infinite;
}

@keyframes parpadeo {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}

/* Animaciones para las frases */
.anim-estilo-0 {
    animation: entradaRebote 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275), flotarSuave 3s ease-in-out infinite alternate 0.8s;
}
@keyframes entradaRebote {
    0% { opacity: 0; transform: scale(0.3) translateY(30px); }
    100% { opacity: 1; transform: scale(1) translateY(0); }
}

.anim-estilo-1 {
    animation: entradaSubir 0.9s ease-out, brilloResplandor 2.5s ease-in-out infinite alternate 0.9s;
}
@keyframes entradaSubir {
    0% { opacity: 0; transform: translateY(40px); }
    100% { opacity: 1; transform: translateY(0); }
}

.anim-estilo-2 {
    animation: entradaGiro3D 1s ease-out, flotarSuave 3.2s ease-in-out infinite alternate 1s;
}
@keyframes entradaGiro3D {
    0% { opacity: 0; transform: perspective(400deg) rotateX(-80deg); }
    100% { opacity: 1; transform: perspective(400deg) rotateX(0deg); }
}

.anim-estilo-3 {
    animation: entradaIzquierda 0.9s cubic-bezier(0.68, -0.55, 0.265, 1.55), flotarSuave 2.8s ease-in-out infinite alternate 0.9s;
}
@keyframes entradaIzquierda {
    0% { opacity: 0; transform: translateX(-50px) scale(0.9); }
    100% { opacity: 1; transform: translateX(0) scale(1); }
}

@keyframes flotarSuave {
    0% { transform: translateY(0px); text-shadow: 0px 2px 10px rgba(255, 51, 102, 0.4); }
    100% { transform: translateY(-8px); text-shadow: 0px 6px 20px rgba(255, 215, 0, 0.8); }
}

@keyframes brilloResplandor {
    0% { transform: translateY(0px); text-shadow: 0px 2px 8px rgba(255, 51, 102, 0.4); }
    100% { transform: translateY(-6px); text-shadow: 0px 0px 22px rgba(255, 255, 255, 0.9), 0px 0px 30px rgba(255, 215, 0, 1); }
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
        
        contenedor_foto = st.empty()
        contenedor_frase = st.empty()
        
        while True:
            for idx, ruta in enumerate(archivos_completos):
                frase_actual = FRASES_DE_AMOR[idx % len(FRASES_DE_AMOR)]
                estilo_anim = f"anim-estilo-{idx % 4}"
                
                img = Image.open(ruta)
                img = ImageOps.exif_transpose(img)
                contenedor_foto.image(img, use_container_width=True)
                
                texto_parcial = ""
                velocidad_letra = 0.035
                
                for letra in frase_actual:
                    texto_parcial += letra
                    contenedor_frase.markdown(
                        f'<div class="frase-amor {estilo_anim}">{texto_parcial}<span class="cursor-tipeo">|</span></div>',
                        unsafe_allow_html=True
                    )
                    time.sleep(velocidad_letra)
                
                contenedor_frase.markdown(
                    f'<div class="frase-amor {estilo_anim}">{frase_actual}</div>',
                    unsafe_allow_html=True
                )
                
                tiempo_escritura = len(frase_actual) * velocidad_letra
                tiempo_restante = max(1.5, 5.5 - tiempo_escritura)
                time.sleep(tiempo_restante)
    else:
        st.warning("No se encontraron fotos. Asegúrate de haber subido imágenes a tu carpeta de Drive.")
