import os
import streamlit as st
from PIL import Image

# Configuración de la interfaz
st.set_page_config(page_title="BEID", layout="wide")
st.title("📸 BEID")

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

# --- GALERÍA PÚBLICA (Visible para todos) ---
st.subheader("🖼️ Galería BEID")

archivos = [f for f in os.listdir(CARPETA_FOTOS) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))]

if archivos:
    cols = st.columns(4)  # Mostrar en 4 columnas
    for idx, archivo in enumerate(archivos):
        ruta_img = os.path.join(CARPETA_FOTOS, archivo)
        
        with cols[idx % 4]:
            img = Image.open(ruta_img)
            st.image(img, use_container_width=True)
else:
    st.info("No hay fotos registradas todavía.")
