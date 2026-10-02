import os
import time
from moviepy.editor import *
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import numpy as np
import random

# --- CONFIGURACIÓN DEL PROYECTO ---
# Dimensiones y duración del banner
WIDTH = 2000
HEIGHT = 400
DURATION = 30  # Segundos
SCROLLING_SPEED = 60 # Píxeles por segundo (lento y suave)
# Un ciclo completo del patrón de la cuerda tiene 12 elementos (6 fotos/notas, 6 luces).
# Necesitamos crear una secuencia que sea más ancha que el banner para un loop sin fin.
# Ancho total de la secuencia de imágenes debe ser (n * WIDTH + WIDTH) para un loop suave.
# Definamos el número de ciclos para el loop.
NUM_CYCLES_FOR_LOOP = 3 # Mínimo 2 para loop, 3 para mejor visualización de elementos entrantes.
# Definimos el ancho de un ciclo (una sección completa de fotos y luces).
CYCLE_WIDTH = WIDTH * 1.5 # Que sea un poco más ancho que la pantalla.
TOTAL_SEQUENCE_WIDTH = int(CYCLE_WIDTH * NUM_CYCLES_FOR_LOOP)

# Define la ruta a tus archivos de imagen
# Se recomienda usar nombres descriptivos para los archivos.
IMAGE_FOLDER = 'tu_carpeta_de_fotos' # Reemplazar con tu ruta de carpeta

# --- CREACIÓN DE ACTIVOS ---

# 1. Fondo (Gradiente Radial)
def create_gradient_background(width, height):
    base_color = (12, 0, 31, 255) # Color del borde (casi negro)
    center_color = (26, 0, 51, 255) # Color del centro (púrpura oscuro)
    canvas = Image.new('RGBA', (width, height), base_color)
    inner_width = width // 2
    inner_height = height // 2
    inner_circle = Image.new('RGBA', (inner_width, inner_height), center_color)
    blurred_inner = inner_circle.filter(ImageFilter.GaussianBlur(100))
    canvas.paste(blurred_inner, ((width - inner_width) // 2, (height - inner_height) // 2), blurred_inner)
    return ImageClip(np.array(canvas))

# 2. Texto y Emojis con Glow (Pillow)
# MoviePy TextClip no maneja bien los gradientes complejos y el glow de emojis.
# Creamos el texto completo como una imagen estática con glow.
def create_glowing_text(width, height, text, fontsize, glow_color, text_gradient, emojis=None):
    # Crea un lienzo transparente
    canvas = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    # Carga una fuente que soporte emojis, como 'NotoColorEmoji' o similar.
    # Reemplazar con una ruta de fuente válida si es necesario.
    font_path = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf' # Ejemplo en Linux
    if not os.path.exists(font_path):
        font_path = 'arial.ttf' # Fallback
    font = ImageFont.truetype(font_path, fontsize)
    
    full_text = text
    if emojis:
        full_text += f" {emojis}"
    
    # Obtiene dimensiones del texto
    w_text, h_text = font.getsize(full_text)
    x_text = (width - w_text) // 2
    y_text = (height - h_text) // 2
    
    # Crea el Glow (contorno difuminado)
    draw.text((x_text, y_text), full_text, font=font, fill=glow_color)
    glow_image = canvas.filter(ImageFilter.GaussianBlur(8))
    
    # Crea el texto principal con gradiente
    # Primero crea una máscara del texto
    text_mask = Image.new('L', (width, height), 0)
    draw_mask = ImageDraw.Draw(text_mask)
    draw_mask.text((x_text, y_text), full_text, font=font, fill=255)
    
    # Crea una imagen de gradiente del mismo tamaño que el texto
    gradient = Image.new('RGBA', (width, height), (0,0,0,0))
    draw_grad = ImageDraw.Draw(gradient)
    # Ejemplo de gradiente simple, se puede mejorar
    start_color = (155, 77, 255, 255) # Púrpura
    end_color = (255, 140, 255, 255) # Rosa
    for i in range(h_text):
        draw_grad.line([(x_text, y_text + i), (x_text + w_text, y_text + i)], fill=start_color, width=1)
        # Aquí se puede añadir lógica para el gradiente a través de las letras,
        # como crear una imagen de gradiente de 1 píxel de ancho y escalarla.

    # Compone el texto con gradiente sobre el glow
    final_canvas = Image.new('RGBA', (width, height), (0,0,0,0))
    final_canvas.paste(glow_image, (0,0), glow_image)
    final_canvas.paste(gradient, (0,0), text_mask)
    
    return ImageClip(np.array(final_canvas))

# Creación de Textos
# El texto superior "RECUERDOS"
# Glow: rosa fuerte. Gradiente: Púrpura->Rosa->Blanco->Púrpura (patrón de 4 colores)
header_text = create_glowing_text(WIDTH, int(HEIGHT*0.25), "RECUERDOS", 80, (255, 0, 127, 200), [(155, 77, 255), (255, 140, 255), (255, 255, 255), (155, 77, 255)])
header_text = header_text.set_position(('center', 20)).set_duration(DURATION)

# El texto inferior "Tú y yo, mi momento preferido del día. 💖✨🌙"
# Glow: rosa suave. Gradiente: Púrpura->Rosa->Blanco->Púrpura
footer_text = create_glowing_text(WIDTH, int(HEIGHT*0.15), "Tú y yo, mi momento preferido del día.", 40, (255, 140, 255, 150), [(155, 77, 255), (255, 140, 255), (255, 255, 255), (155, 77, 255)], emojis="💖✨🌙")
footer_text = footer_text.set_position(('center', int(HEIGHT*0.8))).set_duration(DURATION)

# 3. Luces Edison de Colores con Glow (Pillow)
def create_glowing_light(color, glow_color, size=(60, 100), glow_radius=30):
    # Lienzo transparente
    canvas = Image.new('RGBA', (size[0] + 2*glow_radius, size[1] + 2*glow_radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    # Glow (Círculo difuminado detrás)
    center_glow = (size[0] // 2 + glow_radius, size[1] // 2 + glow_radius)
    draw.ellipse((center_glow[0] - glow_radius, center_glow[1] - glow_radius, 
                   center_glow[0] + glow_radius, center_glow[1] + glow_radius), 
                   fill=glow_color)
    glow_image = canvas.filter(ImageFilter.GaussianBlur(15))
    
    # Bombilla (Cuerpo principal)
    # Forma simple de bombilla Edison
    bulb_shape = [
        (glow_radius, glow_radius + size[1] // 4), # Top left
        (glow_radius + size[0] // 4, glow_radius), # Top center
        (glow_radius + 3*size[0] // 4, glow_radius), # Top center
        (glow_radius + size[0], glow_radius + size[1] // 4), # Top right
        (glow_radius + size[0], glow_radius + size[1]), # Bottom right
        (glow_radius + 3*size[0] // 4, glow_radius + size[1]), # Bottom center
        (glow_radius + size[0] // 4, glow_radius + size[1]), # Bottom center
        (glow_radius, glow_radius + size[1]) # Bottom left
    ]
    draw.polygon(bulb_shape, fill=color)
    
    # Añadir filamento y base (con Pillow, dibujo simple)
    # Filamento
    draw.line([(center_glow[0] - 5, center_glow[1] - 15), (center_glow[0] + 5, center_glow[1] + 15)], fill=(255, 255, 255, 150), width=2)
    # Base
    draw.rectangle((center_glow[0] - 10, glow_radius + size[1] - 10, center_glow[0] + 10, glow_radius + size[1]), fill=(50, 50, 50, 255))

    # Compone la bombilla sobre el glow
    final_canvas = Image.new('RGBA', (size[0] + 2*glow_radius, size[1] + 2*glow_radius), (0, 0, 0, 0))
    final_canvas.paste(glow_image, (0, 0), glow_image)
    final_canvas.paste(canvas, (0, 0), canvas)
    
    return ImageClip(np.array(final_canvas))

# Creación de bombillas (roja, azul, dorada, verde, ámbar)
# Colores principales y de glow para cada una
bulb_red = create_glowing_light((255, 77, 77), (255, 0, 0, 100))
bulb_blue = create_glowing_light((77, 166, 255), (0, 0, 255, 100))
bulb_gold = create_glowing_light((255, 215, 0), (255, 215, 0, 100))
bulb_green = create_glowing_light((77, 255, 77), (0, 255, 0, 100))
bulb_amber = create_glowing_light((255, 191, 0), (255, 191, 0, 100))

# 4. Pinza de Madera (Crea una imagen estática simple con Pillow)
def create_clothespin(size=(20, 60)):
    canvas = Image.new('RGBA', size, (0,0,0,0))
    draw = ImageDraw.Draw(canvas)
    # Cuerpo de madera
    draw.rectangle((0, 0, size[0], size[1]), fill=(210, 180, 140))
    # Detalle de muelle de metal (línea gris simple)
    draw.line([(size[0]//2 - 2, 0), (size[0]//2 + 2, size[1])], fill=(100, 100, 100), width=1)
    # Perno de metal (punto gris simple)
    draw.ellipse((size[0]//2 - 3, size[1]//2 - 3, size[0]//2 + 3, size[1]//2 + 3), fill=(150, 150, 150))
    return ImageClip(np.array(canvas))

pin_clip = create_clothespin()

# 5. Marcos Polaroid (Crea marcos estáticos con Pillow)
# Se pueden personalizar con rotación casual y sombras simples.
# No necesitamos rotarlos con Pillow, MoviePy lo hará.
def create_polaroid_frame(image_size=(300, 300), rotate_casual=False, note=False):
    frame_width = int(image_size[0] * 1.1)
    frame_height = int(image_size[1] * 1.25)
    canvas = Image.new('RGBA', (frame_width, frame_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    # Borde blanco
    draw.rectangle((0, 0, frame_width, frame_height), fill=(255, 255, 255))
    
    # Sombra simple (con Pillow, difícil de hacer bien, pero un desenfoque simple sirve)
    shadow = Image.new('RGBA', (frame_width + 10, frame_height + 10), (0, 0, 0, 0))
    draw_shadow = ImageDraw.Draw(shadow)
    draw_shadow.rectangle((5, 5, frame_width + 5, frame_height + 5), fill=(0, 0, 0, 50))
    shadow_image = shadow.filter(ImageFilter.GaussianBlur(5))
    
    # Compone la Polaroid sobre la sombra
    final_canvas = Image.new('RGBA', (frame_width + 20, frame_height + 20), (0, 0, 0, 0))
    final_canvas.paste(shadow_image, (5, 5), shadow_image)
    final_canvas.paste(canvas, (10, 10), canvas)
    
    polaroid_frame_clip = ImageClip(np.array(final_canvas))
    
    # Si es nota, añade texto manuscrito simple
    if note:
        # Carga una fuente manuscrita simple si tienes una.
        note_font_path = '/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf' # Ejemplo en Linux
        if not os.path.exists(note_font_path):
            note_font_path = 'arial.ttf' # Fallback
        
        # Necesitamos volver a PIL para dibujar texto
        canvas_pil = Image.fromarray(np.uint8(final_canvas))
        draw_pil = ImageDraw.Draw(canvas_pil)
        
        note_font = ImageFont.truetype(note_font_path, 25)
        # Reemplazar con el texto de la nota de la imagen
        note_text = "Tú y yo, mi momento preferido del día."
        # Centrar y dibujar
        w_n, h_n = draw_pil.textsize(note_text, font=note_font)
        draw_pil.text(((frame_width + 20 - w_n) // 2, frame_height - 60), note_text, fill=(0,0,0), font=note_font)
        
        # Añadir emojis simples o sparkles (corazón, estrellas, luna)
        sparkles_font_path = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf' # Ejemplo en Linux
        if not os.path.exists(sparkles_font_path):
            sparkles_font_path = 'arial.ttf' # Fallback
        sparkles_font = ImageFont.truetype(sparkles_font_path, 30)
        draw_pil.text(((frame_width + 20 + w_n) // 2 + 10, frame_height - 60), "💖✨🌙", fill=(0,0,0), font=sparkles_font)

        polaroid_frame_clip = ImageClip(np.array(canvas_pil))

    # Rotación casual (con Pillow) si se especifica
    # (En desuso, se hará con MoviePy)
    
    return polaroid_frame_clip

# Creación de marcos (foto estándar y nota)
polaroid_clip = create_polaroid_frame()
note_clip = create_polaroid_frame(note=True)

# 6. Cuerda ( twinesingle ) (Pillow, dibuja una línea simple con textura de cuerda)
# Es más fácil dibujar la cuerda como parte de la composición ultra-ancha de Pillow.

# 7. Composición Ultra-ancha de la Secuencia de Cuerda (Pillow)
def create_seamless_scroll_sequence(total_width, height, cycle_width, image_folder, num_cycles_for_loop):
    # Lienzo ultra-ancho transparente
    canvas = Image.new('RGBA', (total_width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    # Carga las fotos de la carpeta
    images_pil = [Image.open(os.path.join(image_folder, f)) for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not images_pil:
        # Añade fotos de marcador si no hay fotos
        for i in range(5):
            images_pil.append(Image.new('RGBA', (300, 300), (random.randint(0,255), random.randint(0,255), random.randint(0,255), 100)))

    # Crea una composición para un ciclo
    def create_cycle_composition(images, polaroid_clip, note_clip, pin_clip, bulbs):
        cycle_canvas = Image.new('RGBA', (int(cycle_width), height), (0, 0, 0, 0))
        draw_cycle = ImageDraw.Draw(cycle_canvas)
        
        # Dibuja la cuerda ( twinesingle ) (Línea marrón simple con desenfoque ligero)
        # Anchura de línea de cuerda simple
        # x_start_cuerda = random.randint(0, int(cycle_width * 0.1)) # Casual start
        x_start_cuerda = 0 # Inicio exacto
        # x_end_cuerda = cycle_width - random.randint(0, int(cycle_width * 0.1)) # Casual end
        x_end_cuerda = cycle_width # Fin exacto
        y_cuerda = height // 2 # Altura central
        # Línea de cuerda marrón simple
        draw_cycle.line([(x_start_cuerda, y_cuerda), (x_end_cuerda, y_cuerda)], fill=(168, 126, 80), width=3)
        # Desenfoque ligero para textura
        twine_image = twine_canvas.filter(ImageFilter.GaussianBlur(1))
        # Vuelve a pegar sobre el lienzo de ciclo
        cycle_canvas.paste(twine_image, (0, 0), twine_image)
        
        # Distribuye fotos, notas y luces en el ciclo
        # El patrón en image_4.png es: P1 -> RLight -> P2 -> BLight -> P3 -> ALight -> Note -> GLight -> P4 -> RLight -> P5 -> ALight.
        # Es un patrón de unos 12 elementos. Distribuyamos los elementos en posiciones X casuales.
        
        num_photos = 5
        num_notes = 1
        num_lights = num_photos + num_notes
        
        elements_pos_x = sorted([random.randint(0, int(cycle_width)) for _ in range(num_photos + num_notes)])
        lights_pos_x = sorted([pos + random.randint(0, int(cycle_width * 0.15)) for pos in elements_pos_x])

        # Asegura que las fotos y notas se distribuyen y no se solapan excesivamente.
        # (Lógica de distribución casual pero controlada)

        photo_indices = random.sample(range(len(images)), num_photos)
        photo_count = 0
        note_placed = False
        light_index = 0
        
        for i, pos_x in enumerate(elements_pos_x):
            # Posición casual y rotación casual
            y_photo = y_cuerda + random.randint(-10, 10)
            rotate_angle = random.uniform(-5, 5) # Rotación casual en grados

            # Elige si colocar foto o nota (una nota por ciclo)
            place_note = False
            if not note_placed and random.random() < (num_notes / (num_photos + num_notes - i)):
                place_note = True
                note_placed = True
            
            # Crea la composición (Foto/Nota sobre Cuerda con Pinza) PIL Image
            if place_note:
                element_pil = Image.fromarray(np.uint8(note_clip.get_frame(0)))
            else:
                # Componer foto sobre marco Polaroid
                photo_pil = images[photo_indices[photo_count]]
                # Escalar foto para encajar en el marco
                frame_w, frame_h = polaroid_clip.size
                photo_w, photo_h = photo_pil.size
                target_photo_w = int(frame_w * 0.85)
                # target_photo_h = int(frame_h * 0.7)
                target_photo_h = target_photo_w * (photo_h / photo_w) # Mantener aspecto
                
                scaled_photo = photo_pil.resize((target_photo_w, int(target_photo_h)), Image.LANCZOS)
                photo_x = (frame_w - target_photo_w) // 2 + 10 # 10 es el margen de la sombra
                # photo_y = (frame_h - target_photo_h) // 2 + 10
                # Alinear arriba
                photo_y = 10 + 20 # 20 es el borde superior Polaroid

                # Componer foto sobre marco Polaroid
                # polaroid_frame_pil = Image.fromarray(np.uint8(polaroid_clip.get_frame(0)))
                polaroid_frame_pil = polaroid_frame_pil.paste(scaled_photo, (photo_x, photo_y), scaled_photo)
                
                element_pil = polaroid_frame_pil
                photo_count += 1
            
            # Rotar casualmente
            rotated_element = element_pil.rotate(rotate_angle, expand=True)
            
            # Componer sobre el ciclo
            # Posición casual de X
            pos_x_casual = x_start_cuerda + pos_x
            cycle_canvas.paste(rotated_element, (pos_x_casual, int(y_photo - rotated_element.size[1] // 2)), rotated_element)
            
            # Componer Pinza sobre Foto
            pin_pil = Image.fromarray(np.uint8(pin_clip.get_frame(0)))
            # Pinza en casual start top-center de la foto
            pin_x = pos_x_casual + rotated_element.size[0] // 2 - pin_pil.size[0] // 2
            # pin_y = int(y_photo - pin_pil.size[1] // 2)
            pin_y = int(y_photo - pin_pil.size[1]) # Encima de la foto
            cycle_canvas.paste(pin_pil, (pin_x, pin_y), pin_pil)

            # Componer Bombilla intercalada (casual pos_x entre fotos)
            # Elige una bombilla de color casual
            bulb_clip = random.choice(bulbs)
            bulb_pil = Image.fromarray(np.uint8(bulb_clip.get_frame(0)))
            # casual pos_x de bombilla entre fotos
            pos_x_bulb_casual = x_start_cuerda + lights_pos_x[i]
            # y_bulb causal
            y_bulb = y_cuerda + random.randint(10, 30) # Debajo de la cuerda

            cycle_canvas.paste(bulb_pil, (pos_x_bulb_casual, y_bulb), bulb_pil)
        
        return cycle_canvas

    # Bulbos de colores
    bulbs = [bulb_red, bulb_blue, bulb_gold, bulb_green, bulb_amber]
    
    # Crea una composición de ciclo estática
    cycle_compo_pil = create_cycle_composition(images_pil, polaroid_clip, note_clip, pin_clip, bulbs)
    
    # Crea la secuencia ultra-ancha duplicando el ciclo
    for i in range(num_cycles_for_loop):
        canvas.paste(cycle_compo_pil, (int(i * cycle_width), 0), cycle_compo_pil)
        
    return canvas

# --- COMPOSICIÓN DEL BANNER FINAL ---

# Crea el fondo
background_clip = create_gradient_background(WIDTH, HEIGHT)

# Crea la secuencia de imágenes ultra-ancha con Pillow
seamless_sequence_pil = create_seamless_scroll_sequence(TOTAL_SEQUENCE_WIDTH, HEIGHT, CYCLE_WIDTH, IMAGE_FOLDER, NUM_CYCLES_FOR_LOOP)
# seamless_sequence_pil.save('seamless_sequence.png') # Para depuración

# Crea un ImageClip de la secuencia ultra-ancha
seamless_scroll_clip = ImageClip(np.array(seamless_sequence_pil))

# --- ANIMACIÓN DE DESPLAZAMIENTO Y LOOP ---

# MoviePy tiene una forma limpia de hacer loops de imágenes.
# La idea es crear un CompositeVideoClip que contenga el clip de secuencia,
# y luego hacer un loop sobre él.
# Pero necesitamos animar la posición de la secuencia ultra-ancha.
# Y luego, la distancia recorrida debe ser exactamente el ancho de un ciclo (CYCLE_WIDTH)
# para que el loop sea perfecto.

# Composición total del banner (Fondo + Texto Estático + Cuerda con Fotos)
# La cuerda con fotos se coloca en la parte inferior, debajo del texto.

# Composición estática del banner
banner_composition = [
    background_clip,
    header_text,
    footer_text,
    # Cuerda con fotos (scrolling y loop)
]

# Crea unCompositeVideoClip estático para el banner total
# La cuerda con fotos se coloca inicialmente fuera de la pantalla a la derecha.
# Luego, se anima su posición X para que se desplace hacia la izquierda.
# Al final de la animación, el inicio del primer ciclo duplicado debe estar exactamente
# en el mismo lugar que el inicio del primer ciclo original al principio.
# Así que la distancia recorrida es CYCLE_WIDTH.
# El tiempo de animación es T = CYCLE_WIDTH / SCROLLING_SPEED.

# Crea la cuerda con fotos (ImageClip) con posición inicial fuera de pantalla a la derecha
scrolling_string_clip = seamless_scroll_clip.set_position((WIDTH, HEIGHT // 2)).set_duration(DURATION)

# Define la animación de desplazamiento
# Desplazamiento de X: de WIDTH a (WIDTH - CYCLE_WIDTH)
T_loop = CYCLE_WIDTH / SCROLLING_SPEED
if T_loop > DURATION:
    print(f"La duración del loop ({T_loop:.2f}s) es mayor que la duración del video ({DURATION}s). Aumenta la duración o la velocidad.")
    # (O ajusta la lógica)

# Lógica de loop con MoviePy CompositeVideoClip
# Es más simple crear unCompositeVideoClip con el loop ya hecho.
# Creamos unCompositeVideoClip de un solo ciclo y luego hacemos un loop de DURATION.

# Crea unCompositeVideoClip de un solo ciclo y ancho CYCLE_WIDTH
# El fondo es transparente.
def create_composite_cycle_clip(pil_cycle, cycle_width, height, speed):
    composite_cycle = CompositeVideoClip([
        ImageClip(np.array(pil_cycle)).set_duration(cycle_width/speed).set_position('center')
    ], size=(int(cycle_width), height)).set_duration(cycle_width/speed)
    return composite_cycle

# Crea un loop de la secuencia ultra-ancha
# Creamos unCompositeVideoClip con las capas y luego hacemos un loop.
# layers = []
# # Capas de fotos y luces (scrolling)
# # Composición ultra-ancha como una sola ImageClip
# scroller = seamless_scroll_clip.set_position((0, HEIGHT//2)).set_duration(total_sequence_width/SCROLLING_SPEED)
# layers.append(scroller)
# # Capas de texto (estáticas y fijas)
# layers.append(header_text)
# layers.append(footer_text)
# # Capa de fondo
# layers.append(background_clip)
# total_banner = CompositeVideoClip(layers, size=(WIDTH, HEIGHT))
# total_banner = total_banner.set_duration(DURATION)

# Lógica de desplazamiento y loop simple:
# Anima X position of ultra_wide image. Use % total_sequence_width or % cycle_width or (total_sequence_width - WIDTH).
# seamless_loop_clip = seamless_scroll_clip.fl_pos(lambda t: ((-SCROLLING_SPEED * t) % (total_sequence_width - WIDTH), HEIGHT // 2))

# La forma más robusta de hacer un loop de imagen con MoviePy es:
# Crea un composite de la imagen y un loop del composite.
# scroller_composite = CompositeVideoClip([seamless_scroll_clip.set_position((0, HEIGHT//2))], size=(total_sequence_width, HEIGHT))
# seamless_loop_clip = scroller_composite.loop().set_duration(DURATION)
# # Luego, desplaza X position. X goes from 0 to total_sequence_width over time. Use fl_x.
# seamless_loop_clip = seamless_loop_clip.fl_x(lambda t: (-SCROLLING_SPEED * t) % total_sequence_width )

# Composición final total con loop simple
total_banner = CompositeVideoClip([
    background_clip,
    header_text,
    footer_text,
    # La cuerda con fotos (scrolling y loop sin fin)
    #seamless_scroll_clip.set_position((0, HEIGHT//2)).set_duration(DURATION).fl_pos(lambda t: ((-SCROLLING_SPEED * t) % TOTAL_SEQUENCE_WIDTH, HEIGHT // 2))
    # La imagen ultra-ancha no se desplaza por completo. Solo se desplaza CYCLE_WIDTH.
    # El X posición casual es Casual Start X. Luego se desplaza -T * SCROLLING_SPEED.
    seamless_scroll_clip.set_position((random.randint(0, int(CYCLE_WIDTH * 0.1)), HEIGHT//2)).set_duration(DURATION).fl_pos(lambda t: ((-SCROLLING_SPEED * t) % CYCLE_WIDTH, HEIGHT // 2))

], size=(WIDTH, HEIGHT)).set_duration(DURATION)

# --- GUARDAR EL VIDEO FINAL ---
# total_banner.preview() # Para depuración
total_banner.write_videofile("galeria_recuerdos_scroller.mp4", fps=24, codec='libx264', audio=False)

# print(f"Video guardado como: galeria_recuerdos_scroller.mp4")
