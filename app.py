import os
import time
import streamlit as st
from PIL import Image

# Configuración de la interfaz
st.set_page_config(page_title="BEID", layout="wide")
st.title("📸 BEID")

# --- ANIMACIÓN CSS (Para dar el efecto de movimiento) ---
st.markdown("""
    <style>
    div[data-testid="stImage"] img {
        /* Efecto de aparición y zoom lento de 2 segundos */
        animation: zoomFade 2s ease-in-out forwards;
        border-radius: 10px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
    }
    @keyframes zoomFade {
        0% { opacity: 0.2; transform: scale(0.95); }
        20% { opacity: 1; }
        100% { opacity: 1; transform: scale(1.05); }
    }
    </style>
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

# --- GALERÍA PÚBLICA (Visor una por una con Auto-Play) ---
st.subheader("🖼️ Galería BEID")

archivos = [f for f in os.listdir(CARPETA_FOTOS) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))]

if archivos:
    # Estado para rastrear la foto actual
    if "foto_index" not in st.session_state:
        st.session_state.foto_index = 0

    # Evitar índice fuera de rango
    if st.session_state.foto_index >= len(archivos):
        st.session_state.foto_index = 0

    # Botones de navegación arriba de la imagen
    col_prev, col_info, col_next = st.columns([1, 2, 1])
    
    with col_prev:
        if st.button("⬅️ Anterior", use_container_width=True):
            st.session_state.foto_index = (st.session_state.foto_index - 1) % len(archivos)
            st.rerun()

    with col_info:
        st.markdown(
            f"<h4 style='text-align: center; margin: 0;'>Foto {st.session_state.foto_index + 1} de {len(archivos)}</h4>", 
            unsafe_allow_html=True
        )
        
        # Botón para activar/desactivar la reproducción automática
        st.write("") # Espaciador
        auto_play = st.toggle("▶️ Reproducción Automática (2s)", value=False)

    with col_next:
        if st.button("Siguiente ➡️", use_container_width=True):
            st.session_state.foto_index = (st.session_state.foto_index + 1) % len(archivos)
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Mostrar la foto centrada en tamaño destacado
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        ruta_img = os.path.join(CARPETA_FOTOS, archivos[st.session_state.foto_index])
        img = Image.open(ruta_img)
        st.image(img, use_container_width=True)

    # LÓGICA DE REPRODUCCIÓN AUTOMÁTICA
    if auto_play:
        time.sleep(2) # Pausa por 2 segundos
        # Avanzar al siguiente índice
        st.session_state.foto_index = (st.session_state.foto_index + 1) % len(archivos)
        st.rerun() # Recarga la página para mostrar la nueva foto
else:
    st.info("No hay fotos registradas todavía.")
