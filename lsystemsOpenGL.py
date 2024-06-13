import OpenGL.GL as GL
import OpenGL.GLUT as GLUT
import OpenGL.GLU as GLU
from PIL import Image
import imageio
import numpy as np

# Parâmetros
window_height = 600
window_width = 800
x, y = -window_width//2, -window_height//2  # Posição inicial
init_angle = 90
distance_input = 20
thickness = 1.6
frame_interval = 100//8
gif_path = str(input("File name: "))


# L-System Regras
axiom_input = "F-F-F-F"
rules = {"F": "F-b+FF-F-FF-Fb-FF+b-FF+F+FF+Fb+FFF", "b": "bbbbbb"}
angle_input = 90
chars_to_draw = ["F"]
chars_to_jump = ["b"]
iterations_input = 3

def apply_rules(input_char):
    if input_char in rules:
        return rules[input_char]
    else:
        return input_char


def process_string(old_str):
    new_str = ""
    for char in old_str:
        new_str = new_str + apply_rules(char)
    return new_str


def create_l_system(iterations, axiom):
    start_string = axiom
    for _ in range(iterations):
        start_string = process_string(start_string)
    return start_string


def draw_l_system(instructions, angle, distance, x0, y0, theta0):
    stack = []
    lines = []

    # Processando as instruções de desenho
    for command in instructions:
        if command in chars_to_draw:
            new_x = x0 + distance * np.cos(np.radians(theta0))
            new_y = y0 + distance * np.sin(np.radians(theta0))
            lines.append(((x0, y0), (new_x, new_y)))
            x0, y0 = new_x, new_y
        elif command in chars_to_jump:
            new_x = x0 + distance * np.cos(np.radians(theta0))
            new_y = y0 + distance * np.sin(np.radians(theta0))
            x0, y0 = new_x, new_y
        elif command == "+":
            theta0 += angle
        elif command == "-":
            theta0 -= angle
        elif command == "[":
            stack.append((x0, y0, theta0))
        elif command == "]":
            x0, y0, theta0 = stack.pop()

    GLUT.glutInit()
    GLUT.glutInitDisplayMode(GLUT.GLUT_RGB)
    GLUT.glutInitWindowSize(window_width, window_height)
    GLUT.glutInitWindowPosition(50, 50)
    GLUT.glutCreateWindow(b"L-System")
    GL.glClearColor(1.0, 1.0, 1.0, 1.0)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)
    GLU.gluOrtho2D(-1000, 1000, -1000, 1000)

    frames = []
    line_counter = 0
    GL.glLineWidth(thickness)
    for line in lines:
        GL.glBegin(GL.GL_LINES)
        GL.glColor3f(0.0, 0.0, 0.0)
        GL.glVertex2f(line[0][0], line[0][1])
        GL.glVertex2f(line[1][0], line[1][1])
        GL.glEnd()
        line_counter += 1
        if line_counter % frame_interval == 0:
            GL.glFlush()
            GL.glReadBuffer(GL.GL_FRONT)
            pixels = GL.glReadPixels(
                0, 0, window_width, window_height, GL.GL_RGB, GL.GL_UNSIGNED_BYTE
            )
            image = Image.frombytes("RGB", (window_width, window_height), pixels)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            frames.append(image)

    print("Writing GIF......")
    imageio.mimsave(gif_path, frames, format='GIF', duration=0.1, loop=0)
    print("Done!!!!")

    GL.glFlush()
    GLUT.glutMainLoop()


def main():
    l_system_string = create_l_system(iterations_input, axiom_input)
    draw_l_system(l_system_string, angle_input, distance_input, x, y, init_angle)


if __name__ == "__main__":
    main()
