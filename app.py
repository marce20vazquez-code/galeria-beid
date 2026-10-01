import os
import time
import streamlit as st
from PIL import Image

# Configuración de la interfaz
st.set_page_config(page_title="BEID", layout="centered")
st.title("📸 BEID")

# --- ANIMACIÓN CSS Y LLUVIA DE CORAZONES ---
st.markdown("""
    <style>
    /* Efecto de la foto (zoom y movimiento) */
    div[data-testid="stImage"] img {
        animation: zoomFade 2s ease-in-out forwards;
        border-radius: 15px;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.4);
        max-height: 75vh;
        object-fit: contain;
    }
    @keyframes zoomFade {
        0% { opacity: 0.2; transform: scale(0.95); }
        20% { opacity: 1; }
        100% { opacity: 1; transform: scale(1.05); }
    }

    /* Contenedor de la lluvia de corazones de fondo */
    .heart-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: hidden;
        z-index: 99999;
    }

    .heart {
        position: absolute;
        bottom: -20px;
        color: #ff3366;
        font-size: 24px;
        animation: floatUp 4s linear infinite;
        opacity: 0.8;
    }

    @keyframes floatUp {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(-100vh) rotate(360deg);
            opacity: 0;
        }
    }
    </style>

    <!-- Script para generar corazones flotantes continuos en pantalla -->
    <div class="heart-container">
        <div class="heart" style="left: 10%; animation-delay: 0s; animation-duration: 3.5s;">❤️</div>
        <div class="heart" style="left: 25%; animation-delay: 1.2s; animation-duration: 4s;">💖</div>
        <div class="heart" style="left: 40%; animation-delay: 0.5s; animation-duration: 3s;">💗</div>
        <div class="heart" style="left: 60%; animation-delay: 2s; animation-duration: 4.5s;">❤️</div>
        <div class="heart" style="left: 75%; animation-delay: 0.8s; animation-duration: 3.8s;">💘</div>
        <div class="heart" style="left: 90%; animation-delay: 1.5s; animation-duration: 4.2s;">💖</div>
    </div>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE SEGURIDAD ---
CLAVE_ADMIN = "Marcelino"

# Crear carpeta de almacenamiento con el nombre BEID si no existe
CARPETA_FOTOS = "BEID"
if not os.path.exists(CARPETA_FOTOS):
    os.makedirs(CARPETA_FOTOS)

# Comprobar si se ingresó la clave vía parámetro en el enlace (?admin=clave)
es_admin = st.query_params.get("admin") == CLAVE_ADMIN

# Barra lateral: Autenticación de administrador
st.sidebar.header("🔐 Acceso Administrador")

if not es_admin:
    clave_ingresada = st.sidebar.text_input("Contraseña de admin", type="password")
    if clave_ingresada == CLAVE_ADMIN:
        es_admin = True
        st.sidebar.success("¡Modo Administrador activado!")
    elif clave_ingresada != "":
        st.sidebar.error("Contraseña incorrecta.")

# --- SECCIÓN DE SUBIDA MÚLTIPLE (Solo visible para el Administrador) ---
if es_admin:
    st.sidebar.markdown("---")
    st.sidebar.header("📤 Subir Fotos")
    
    fotos_subidas = st.sidebar.file_uploader(
        "Selecciona la(s) foto(s)", 
        type=["jpg", "jpeg", "png", "webp"], 
        accept_multiple_files=True
    )

    if st.sidebar.button("Guardar Fotos"):
        if fotos_subidas:
            cant_guardadas = 0
            for foto in fotos_subidas:
                ruta_destino = os.path.join(CARPETA_FOTOS, foto.name)
                
                # Guardar en disco
                with open(ruta_destino, "wb") as f:
                    f.write(foto.getbuffer())
                cant_guardadas += 1
                
            st.sidebar.success(f"¡Se guardaron {cant_guardadas} foto(s) correctamente!")
            st.rerun()
        else:
            st.sidebar.error("Selecciona al menos una foto antes de guardar.")

# --- GALERÍA PÚBLICA AUTOMÁTICA ---
st.subheader("🖼️ Galería BEID")

archivos = [f for f in os.listdir(CARPETA_FOTOS) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))]

if archivos:
    # Estado para rastrear la foto actual
    if "foto_index" not in st.session_state:
        st.session_state.foto_index = 0

    # Evitar índice fuera de rango
    if st.session_state.foto_index >= len(archivos):
        st.session_state.foto_index = 0

    # Mostrar la foto completa sin recortar
    ruta_img = os.path.join(CARPETA_FOTOS, archivos[st.session_state.foto_index])
    img = Image.open(ruta_img)
    st.image(img, use_container_width=True)

    # LÓGICA DE REPRODUCCIÓN AUTOMÁTICA (Invisible y siempre activa)
    time.sleep(2) # Pausa por 2 segundos
    # Avanzar al siguiente índice
    st.session_state.foto_index = (st.session_state.foto_index + 1) % len(archivos)
    st.rerun() # Recarga la página para mostrar la nueva foto
else:
    st.info("No hay fotos registradas todavía.")
