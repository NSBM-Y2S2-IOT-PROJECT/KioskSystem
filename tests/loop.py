from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

angle = 0  # Rotation angle for the cube

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

def draw_cube():
    global angle
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5)
    glRotatef(angle, 1, 1, 0)  # Rotate the cube
    glutWireCube(2)  # Draw a wireframe cube
    glutSwapBuffers()
    angle += 1  # Increment the rotation angle

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Rotating 3D Cube")
    init()
    glutDisplayFunc(draw_cube)
    glutIdleFunc(draw_cube)  # Keep redrawing the scene
    glutMainLoop()

if __name__ == "__main__":
    main()
