from OpenGL.GL import *
from OpenGL.GLUT import *

GLuint vertShader = glCreateShader(GL_VERTEX_SHADER)
if (0==vertShader):
    raise Error
v = GLchar()
loadSa