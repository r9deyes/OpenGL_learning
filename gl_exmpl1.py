from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo

global unif_color
global Program

class vertex:
    x=GLfloat()
    y=GLfloat()
    def __init__(s,*ar):
        s.x = GLfloat(ar[0])
        s.y = GLfloat(ar[1])

def initGL():
    glClearColor(0.0,0.0,0.0,0.0)

#def checkOpenGLerror():

def initShader():
    vsSource ="attribute vec2 coord;    void main()    {        gl_Position=vec4(coord,0.0,1.0);    }    "
    fsShader = "uniform vec4 color;    void main()    {        gl_FragColor=color;    }"
    vShader,fShader = GLuint(),GLuint()
    vShader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vShader,vsSource,)
    glCompileShader(vShader)
    print('vertex shader '+str(vShader))
    fShader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fShader,fsShader)
    glCompileShader(fShader)
    print('fragment shader '+ str(fShader))
    Program = glCreateProgram()
    glAttachShader(Program,vShader)
    glAttachShader(Program,fShader)
    glLinkProgram(Program)

def initVBO():
    glGenBuffers(1, vbo.VBO)
    glBindBuffer(GL_ARRAY_BUFFER, vbo.VBO)
    triangle=(vertex(1.0,-1.0),
              vertex(0.0,1.0),
              vertex(1.0,-1.0))
    glBufferData(GL_ARRAY_BUFFER,len(triangle), triangle,GL_STATIC_DRAW)

def resizeWindow(width, height):
    glViewport(0,0,600,400)

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    #glColor3f(1.0,0.0,0.0)
    #object = glutWireSphere(1,50,50)

    glUseProgram(Program)
    glUniform4fv(unif_color,1,[1.0, 0.0, 0.0, 1.0])
    #glEnableVertexAttribArray(

    glutSwapBuffers()

def freeVBO():
    glBindBuffer(GL_ARRAY_BUFFER,0)
    glDeleteBuffers(1,vbo.VBO)

if __name__=='__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA|GLUT_DOUBLE)
    glutInitWindowSize(800,600)
    glutCreateWindow('Simple shaders')
    initGL()
    initVBO()
    initShader()
    glutReshapeFunc(resizeWindow)
    glutDisplayFunc(render)
    glutMainLoop()
    #freeShader()
    #freeVBO()