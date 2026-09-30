import base64
import time
from PIL import Image
import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="Para mi persona favorita ❤️", page_icon="💖", layout="centered"
)

# Estilos visuales
st.markdown(
    """
    <style>
    .stApp { background-color: #fff0f3; }
    @keyframes floatHearts {
        0% { transform: translateY(0px) scale(0.8); opacity: 1; }
        50% { transform: translateY(-20px) scale(1.1); opacity: 0.8; }
        100% { transform: translateY(-40px) scale(0.8); opacity: 0; }
    }
    .heart-bg {
        font-size: 30px;
        animation: floatHearts 3s infinite ease-in-out;
        display: inline-block;
    }
    .title-text {
        color: #ff4b4b;
        text-align: center;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    </style>
""",
    unsafe_allow_html=True,
)


def lanzar_confeti_y_globos():
  st.components.v1.html(
      """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            confetti({
                particleCount: 100,
                spread: 70,
                origin: { y: 0.6 },
                colors: ['#ff4b4b', '#ff758f', '#ffb3c1', '#ffffff', '#ffd166']
            });
        </script>
    """,
      height=0,
  )


st.markdown(
    "<h1 class='title-text'>❤️ Nuestra Galería de Momentos Especiales</h1>",
    unsafe_allow_html=True,
)
st.write(
    "<p style='text-align: center; color: #555;'>Sube tus fotos para revivir"
    " momentos juntos ✨</p>",
    unsafe_allow_html=True,
)

archivos_subidos = st.file_uploader(
    "📸 Selecciona las fotos que quieras mostrar:",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True,
)

if archivos_subidos:
  if "foto_index" not in st.session_state:
    st.session_state["foto_index"] = 0

  total_fotos = len(archivos_subidos)

  st.markdown("---")
  st.markdown(
      "<div style='text-align: center;'>"
      "<span class='heart-bg'>🎈</span>"
      "<span class='heart-bg'>💖</span>"
      "<span class='heart-bg'>🎈</span>"
      "<span class='heart-bg'>💕</span>"
      "<span class='heart-bg'>🎈</span>"
      "</div>",
      unsafe_allow_html=True,
  )

  idx_actual = st.session_state["foto_index"]
  foto_actual = archivos_subidos[idx_actual]
  imagen = Image.open(foto_actual)

  st.image(
      imagen,
      caption=f"Foto {idx_actual + 1} de {total_fotos} ❤️",
      use_container_width=True,
  )
  lanzar_confeti_y_globos()

  col_prev, col_info, col_next = st.columns([1, 2, 1])

  with col_prev:
    if st.button("⬅️ Anterior", use_container_width=True):
      if st.session_state["foto_index"] > 0:
        st.session_state["foto_index"] -= 1
        st.rerun()

  with col_info:
    st.markdown(
        f"<h4 style='text-align: center; color: #d62828;'>{idx_actual + 1} /"
        f" {total_fotos}</h4>",
        unsafe_allow_html=True,
    )

  with col_next:
    if st.button("Siguiente ➡", use_container_width=True, type="primary"):
      if st.session_state["foto_index"] < total_fotos - 1:
        st.session_state["foto_index"] += 1
        st.rerun()
      else:
        st.balloons()
        st.success("¡Llegaron al final de sus momentos juntos! 🥰❤️")
