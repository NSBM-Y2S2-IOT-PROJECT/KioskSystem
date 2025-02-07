#Problematic
import libfreenect.wrappers.python.freenect as freenect
import cv2
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Initialize variables for hand positions
prev_x, prev_y = 0, 0
rotation_x, rotation_y = 0, 0

def get_depth():
    """Fetch depth data from Kinect."""
    depth, _ = freenect.sync_get_depth()
    return depth

def draw_cube():
    """Draw a 3D cube."""
    global rotation_x, rotation_y
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5)
    glRotatef(rotation_x, 1, 0, 0)
    glRotatef(rotation_y, 0, 1, 0)
    glutWireCube(2)
    glutSwapBuffers()

def track_hands():
    """Track hand movement and update cube rotation."""
    global prev_x, prev_y, rotation_x, rotation_y
    depth = get_depth()
    # Example threshold to detect a "hand" (you'll refine this)
    hand_region = depth[200:400, 200:400]
    hand_pos = np.unravel_index(np.argmin(hand_region), hand_region.shape)
    
    if hand_pos:
        dx, dy = hand_pos[1] - prev_x, hand_pos[0] - prev_y
        rotation_x += dy * 0.1
        rotation_y += dx * 0.1
        prev_x, prev_y = hand_pos[1], hand_pos[0]

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("3D Cube with Hand Gestures")
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(draw_cube)
    glutIdleFunc(track_hands)
    glutMainLoop()

if __name__ == "__main__":
    main()
