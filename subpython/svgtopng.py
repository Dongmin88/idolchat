import cairo
import math

def create_avatar(filename, size=200, bg_color=(0.2, 0.3, 0.8, 1), face_color=(1, 0.8, 0.6, 1)):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
    ctx = cairo.Context(surface)

    # Background
    ctx.set_source_rgba(*bg_color)
    ctx.arc(size/2, size/2, size/2, 0, 2*math.pi)
    ctx.fill()

    # Face
    ctx.set_source_rgba(*face_color)
    ctx.arc(size/2, size/2, size/2.5, 0, 2*math.pi)
    ctx.fill()

    # Eyes
    eye_size = size/10
    ctx.set_source_rgba(0, 0, 0, 1)  # Black color for eyes
    ctx.arc(size/2 - eye_size*1.5, size/2 - eye_size, eye_size, 0, 2*math.pi)
    ctx.arc(size/2 + eye_size*1.5, size/2 - eye_size, eye_size, 0, 2*math.pi)
    ctx.fill()

    # Mouth
    ctx.set_source_rgba(0.8, 0.3, 0.2, 1)  # Red color for mouth
    ctx.arc(size/2, size/2 + size/5, size/6, 0, math.pi)
    ctx.stroke()

    # Save the image
    surface.write_to_png(filename)

# Create the avatar
create_avatar("avatar.png", size=200)
print("Avatar created successfully: avatar.png")