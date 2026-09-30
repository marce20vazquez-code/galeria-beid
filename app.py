import os
import streamlit as st
from PIL import Image

# Configuración de la interfaz
st.set_page_config(page_title="Galería de Fotos", layout="wide")
st.title("📸 Galería de Fotos")

# --- CONFIGURACIÓN DE SEGURIDAD ---
# Cambia 'mi_clave_secreta_123' por la contraseña que quieras usar
CLAVE_ADMIN = "mi_clave_secreta_123"

# Crear carpeta de almacenamiento si no existe
CARPETA_FOTOS = "fotos_personas"
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

# --- SECCIÓN DE SUBIDA (Solo visible para el Administrador) ---
if es_admin:
    st.sidebar.markdown("---")
    st.sidebar.header("📤 Subir Nueva Foto")
    nombre_persona = st.sidebar.text_input("Nombre de la persona:")
    foto_subida = st.sidebar.file_uploader("Selecciona la foto", type=["jpg", "jpeg", "png", "webp"])

    if st.sidebar.button("Guardar Foto"):
        if nombre_persona.strip() != "" and foto_subida is not None:
            # Formatear el nombre de archivo
            ext = foto_subida.name.split(".")[-1]
            nombre_limpio = nombre_persona.strip().replace(" ", "_")
            nombre_archivo = f"{nombre_limpio}.{ext}"
            ruta_destino = os.path.join(CARPETA_FOTOS, nombre_archivo)
            
            # Guardar archivo en disco
            with open(ruta_destino, "wb") as f:
                f.write(foto_subida.getbuffer())
                
            st.sidebar.success(f"¡Foto de **{nombre_persona}** guardada correctamente!")
            st.rerun()
        else:
            st.sidebar.error("Escribe un nombre y selecciona una imagen antes de guardar.")

# --- GALERÍA PÚBLICA (Visible para todos) ---
st.subheader("🖼️ Personas Registradas")

archivos = [f for f in os.listdir(CARPETA_FOTOS) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))]

if archivos:
    cols = st.columns(4)  # Mostrar en 4 columnas
    for idx, archivo in enumerate(archivos):
        ruta_img = os.path.join(CARPETA_FOTOS, archivo)
        nombre_mostrar = os.path.splitext(archivo)[0].replace("_", " ")
        
        with cols[idx % 4]:
            img = Image.open(ruta_img)
            st.image(img, use_container_width=True)
            st.caption(f"👤 **{nombre_mostrar}**")
else:
    st.info("No hay fotos registradas todavía.")
