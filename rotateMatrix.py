# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from ctypes import *
import sys
import time
import array
import transforms3d
from OpenGL_tools import *

def sizeof(object):
    #return sys.getsizeof(object)
    return object.__sizeof__()

def array2GL(GLtype, array):
    c = len(array)
    c1 = len(array[0])
    return ((GLtype * c1) * c)(*[(GLtype * c1)(*ar) for ar in array])

##//! Переменные с индентификаторами ID
##//! ID шейдерной программы
Program = None
##//! ID атрибута
Attrib_vertex = None
##//! ID юниформ переменной цвета
VertexColor = None
VBO = None
IndexPointer = None
VertexPointer = None
vao = None
vertex = GLfloat_2 * 3
_color = GLfloat_4(1.0, 0.0, 0.0, 1.0)
RotationMatrix = None
indexesArray= None
rMatrix = array2GL(GLfloat, [[1.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0,0.0,0.0],
                    [0.0, 0.0, 1.0,0.0],
                    [0.0, 0.0, 0.0, 1.0]])

phi = 0
psi = 0
theta = 0
#rMatrix[0][0]=1.0

indexes=None


def rotationMatrix(dphi, dpsi=0,dtheta=0):
    global phi,psi,theta,rMatrix
    phi = 0 if phi + dphi>360 else phi + dphi
    psi = 0 if psi + dpsi>360 else psi + dpsi
    theta = 0 if theta + dtheta>360 else theta + dtheta
    ar = transforms3d.euler.euler2mat(np.radians(theta), np.radians(psi), np.radians(phi))
    res=np.array(rMatrix)
    res[:3,:3] = ar
    return array2GL(GLfloat, res)

def _rotationMatrix(theta,dpsi=0):
    global phi
    phi = phi + theta
    theta = 0 if phi > 360 else phi
    phi = theta
    theta = float(np.radians(theta))
    c, s = float(np.cos(theta)), float(np.sin(theta))
    R =array2GL(GLfloat, [[c, -s,0.0,0.0],
                  [s, c,0.0,0.0],
                  [0.0,0.0,1.0,0.0],
                  [0.0,0.0,0.0,1.0]])
    return R


def specialKeys(key, x, y):
    # Сообщаем о необходимости использовать глобального массива pointcolor
    global rMatrix
    # Обработчики специальных клавиш
    if key == GLUT_KEY_UP:  # Клавиша вверх
        rMatrix=rotationMatrix(9,0) # rotate2D(rMatrix,15);
    if key == GLUT_KEY_DOWN:  # Клавиша вниз
        rMatrix=rotationMatrix(-9,0) # rotate2D(rMatrix,15);
    if key == GLUT_KEY_LEFT:  # Клавиша влево
        rMatrix = rotationMatrix(0,9)
    if key == GLUT_KEY_RIGHT:  # Клавиша вправо
        rMatrix = rotationMatrix(0,-9)
    if key == GLUT_KEY_PAGE_DOWN:  # Клавиша вправо
        rMatrix = rotationMatrix(0,0,-9)
    if key == GLUT_KEY_PAGE_UP:  # Клавиша вправо
        rMatrix = rotationMatrix(0,0,9)
    if key == GLUT_KEY_HOME or key == GLUT_KEY_END:
        global phi,psi,theta
        phi, psi, theta =0, 0, 0
        rMatrix = rotationMatrix(0 ,0,0)
        print('reset')
        return 0
    #print('_color:', _color[0:2])


##//! Функция печати лога шейдера
def shaderLog(shader):

    infologLen = c_int(0)
    charsWritten = 0
    infoLog = None

    infoLog = glGetShaderiv(shader, GL_INFO_LOG_LENGTH, infologLen)

    if infologLen > 1:
        infoLog = '' #* infologLen
    if infoLog is None:
        print("ERROR: Could not allocate I http:#//www.pvsm.ru/opengl/20137nfoLog buffern")
        exit(1)
    # glGetShaderInfoLog(shader, infologLen, charsWritten, infoLog);
    print("InfoLog: ", infoLog, "nnn")
    # delete[]


##//! Инициализация OpenGL, здесь пока по минимальному=)
def initGL():
    glClearColor(0, 0, 0, 0)


##//! Проверка ошибок OpenGL, если есть то выводж в консоль тип ошибки
def checkOpenGLerror():
    errCode = glGetError()
    if not (errCode == GL_NO_ERROR):
        print("OpenGl error! - ", str(gluErrorString(errCode)))


##//! Инициализация шейдеров
def initShader():
    ##//! Исходный код шейдеров
    vsSource = """layout(location=0) in vec3 VertexPosition;
    layout(location=1) in vec3 VertexColor;
out vec4 Color;
uniform mat4 RotationMatrix;
void main()
{
    Color = vec4(VertexColor, 1.0);//*0.5 + vec4(1.0, 1.0, 1.0, 1.0);
    gl_Position=  RotationMatrix * vec4(VertexPosition,1.0);
}"""


    fsSource = """in vec4 Color;
void main()
{
    gl_FragColor=Color;
}"""

    ##//! Переменные для хранения идентификаторов шейдеров
    vShader, fShader = GLuint(), GLuint()

    # //! Создаем вершинный шейдер
    vShader = glCreateShader(GL_VERTEX_SHADER)
    # //! Передаем исходный код
    glShaderSource(vShader, vsSource)
    # //! Компилируем шейдер
    glCompileShader(vShader)

    print("vertex shader n")
    shaderLog(vShader)

    # //! Создаем фрагментный шейдер
    fShader = glCreateShader(GL_FRAGMENT_SHADER)
    # //! Передаем исходный код
    glShaderSource(fShader, fsSource)
    # //! Компилируем шейдер
    glCompileShader(fShader)

    print("fragment shader n")
    shaderLog(fShader)

    # //! Создаем программу и прикрепляем шейдеры к ней
    global Program
    Program = glCreateProgram()
    glAttachShader(Program, vShader)
    glAttachShader(Program, fShader)

    # //! Линкуем шейдерную программу
    glLinkProgram(Program)

    # //! Проверяем статус сборки
    link_ok = glGetProgramiv(Program, GL_LINK_STATUS)
    if not link_ok:
        print("error attach shaders n")
        return
    # ///! Вытягиваем ID атрибута из собранной программы
    attr_name = "VertexPosition"

    global Attrib_vertex
    Attrib_vertex = glGetAttribLocation(Program, attr_name)
    print('glGetAttribLocation Attrib_vertex', Attrib_vertex)
    if Attrib_vertex == -1:
        print("could not bind attrib ", attr_name)
        return
    # //! Вытягиваем ID юниформ

    global  VertexColor
    VertexColor = glGetAttribLocation(Program, "VertexColor")
    if (VertexColor == -1):
       print("could not bind  " ,"VertexColor" )
       return
    rMatrixName = 'RotationMatrix'
    global RotationMatrix

    RotationMatrix = glGetUniformLocation(Program, rMatrixName)
    print(':rMAtrix index: ', RotationMatrix)
    if RotationMatrix == -1:
        print("could not bind attrib ", rMatrixName)
        return
    checkOpenGLerror()


# //! Инициализация VBO


def initVBO():
    global VBO
    global IndexPointer
    global VertexPointer
    global vao
    global indexes
    global indexesArray
    global ColorPointer

    vao = glGenVertexArrays(1)
    VBO = glGenBuffers(3)
    IndexPointer = VBO[0]
    VertexPointer = VBO[1]
    ColorPointer = VBO[2]
    glBindBuffer(GL_ARRAY_BUFFER, VertexPointer)

    triangle =  (c_float * 18)(*[-0.2, -0.4, 0.5,\
                                -1.0, -0.8, 0.5,\
                                -0.2, -0.8, 0.5,\
                                0.7, 0.3, 1.0,\
                                0.9, 0.5, 1.0,\
                                0.9, 0.9, 1.0])
    triangle, indexes, colors = hexadron()
    #grid=(10,10)
    #triangle = grid_verteces(*grid)
    glBufferData(GL_ARRAY_BUFFER, sizeof(triangle), array.array('f',triangle).tostring(), GL_STATIC_DRAW)

    ##colors = (c_float * 18)(*[0.5, 0.0, 0.0,\
    ##                           0.5, 0.0, 0.0,\
    ##                           0.5, 0.0, 0.0,\
    ##                           1.0, 0.5, 0.0,\
    ##                           1.0, 0.5, 0.0,\
    ##                           1.0, 0.5, 0.0])
    #colors = grid_colors(*grid)
    glBindBuffer(GL_ARRAY_BUFFER, ColorPointer)
    glBufferData(GL_ARRAY_BUFFER, sizeof(colors), array.array('f', colors).tostring(), GL_STATIC_DRAW)
    #glVertexAttribPointer(1, 3 , GL_FLOAT, GL_FALSE, 0, None, 0)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IndexPointer)

    #indexes = (c_ubyte * 6)(*[0,1,2, 3,4,5])
    #indexes = grid_indeces(*grid)
    indexesArray = array.array('B',indexes)

    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indexes), indexesArray.tostring(), GL_STATIC_DRAW)
    
    glBindVertexArray(vao)

    glBindBuffer(GL_ARRAY_BUFFER, VertexPointer)

    checkOpenGLerror()


# //! Освобождение шейдеров
def freeShader():
    global Program
    # //! Передавая ноль, мы отключаем шейдрную программу
    glUseProgram(0)
    # //! Удаляем шейдерную программу
    glDeleteProgram(Program)


# //! Освобождение шейдеров
def freeVBO():
    global VBO
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glDeleteBuffers(2, VBO)


def resizeWindow(width, height):
    glViewport(0, 0, width, height)


# //! Отрисовка
def render():
    global Program
    global VertexColor
    global VertexPointer
    global ColorPointer
    global IndexPointer
    global Attrib_vertex
    global _color
    global RotationMatrix
    global rMatrix
    global indexes
    global indexesArray
    glClear(GL_COLOR_BUFFER_BIT)
    # //! Устанавливаем шейдерную программу текущей
    glUseProgram(Program)

    # //! Передаем юниформ в шейдер
    # print(Unif_color);
    glUniformMatrix4fv(RotationMatrix, GLint(1), GL_FALSE, rMatrix)
    # //! Включаем массив атрибутов
    glEnableVertexAttribArray(Attrib_vertex)
    glBindBuffer(GL_ARRAY_BUFFER, VertexPointer)
    glVertexAttribPointer(Attrib_vertex, 3, GL_FLOAT, GL_FALSE, 0, None)

    glEnableVertexAttribArray(VertexColor)
    glBindBuffer(GL_ARRAY_BUFFER, ColorPointer)
    glVertexAttribPointer(VertexColor, 3, GL_FLOAT, GL_FALSE, 0, None)
    #glBindBuffer(GL_ARRAY_BUFFER, VertexArray)
    #glPolygonMode(GL_FRONT, GL_LINE)
    glDrawElements(GL_TRIANGLES, len(indexesArray), GL_UNSIGNED_BYTE, indexesArray.tostring())
    #glDrawElements(GL_TRIANGLES,GLint(1), GL_UNSIGNED_BYTE, IndexArray)
    glDisableVertexAttribArray(Attrib_vertex)
    glDisableVertexAttribArray(VertexColor)


    # //! Отключаем шейдерную программу
    glUseProgram(0)

    checkOpenGLerror()

    glutSwapBuffers()

def hexadron():
    vertexes = [0, 0.6, 0.35    ,#/0
    0.42, 0.42, 0.35 ,#/1
    0.6, 0, 0.35     ,#2
    0.42, -0.42, 0.35,#3
    0, -0.6, 0.35    ,#4
    -0.42, -0.42, 0.35,#/5
    -0.6, 0, 0.35    ,#6
    -0.42, 0.42, 0.35,#7
    #***median_hexadron***//   
    0, 1, 0        , #8
    0.71, 0.71, 0  , #9
    1, 0, 0        , #10
    0.71, -0.7, 0  , #11
    0,-1,0         , #12
    -0.71, -0.71, 0, #13
    -1, 0, 0       , #14
    -0.71,0.71,0   , #15
    #***bottom***//
    0, 0, -0.65   ]  #16
    indeces =[0,1,2,  2,7,3,  3,7,5,  3,4,5,  5,6,7,  7,0,2]
    for i in range(1, 17): 
        if (i > 8 and i<16):
            #this.t.faces[i] = new int[3];
            indeces+=[i-1,i,16]
        if(i<8): 
            #//this.t.faces[i] = new int[4];
            indeces +=[i,i-1,i+7]
            indeces +=[i+8,i-1,i+7]
        if (i == 8):
            indeces +=[ 7, 0, 15 ]
            indeces +=[ 7, 8, 15 ]
        if (i == 16):
            indeces += [ 15, 8, 16 ]
    colors = [1.0, 1.0, 1.0, #0
              1.0, 1.0, 1.0,#1
              1.0, 1.0, 1.0,#2
              1.0, 1.0, 1.0,#3
              1.0, 1.0, 1.0,#4
              1.0, 1.0, 1.0,#5
              1.0, 1.0, 1.0,#6
              1.0, 1.0, 1.0,#7
              0.7, 0.7, 1.0,#8
              0.7, 0.7, 1.0,#9
              0.7, 0.7, 1.0,#10
              0.7, 0.7, 1.0,#11
              0.7, 0.7, 1.0,#12
              0.7, 0.7, 1.0,#13
              0.7, 0.7, 1.0,#14
              0.7, 0.7, 1.0,#15
              0.9, 0.4, 1.0] #16
    return vertexes, indeces, colors
    
def landscape(u=2,v=2):
    def grid_verteces(u=2,v=2):
        t=(c_float * (v*u*3))()
        for i in range(u):
            for j in range(0,v*3,3):
                t[i*u + j] = c_float(i/float(u))
                t[i*u + j+1]=c_float(j/float(v))
                t[i*u + j+2]=c_float(0.5)
        return t
    def grid_colors(u=2,v=2):
        t=(c_float * (v*u*3))()
        for i in range(u):
            for j in range(0,v*3,3):
                t[i*u + j] = c_float((i*u + j)/float(u*v))
                t[i*u + j+1]=c_float(1.0-(i*u + j)/float(u*v))
                t[i*u + j+2]=c_float(0.5)
        return t
    def grid_indeces(u=2, v=2):
        t=(c_ubyte * ((u-1)*(v-1)*6))()
        for i in range(u-1):
            for j in range(v-1):
                indexa = j * (u - 1) + i
                indexb = j * u + i
                t[indexa * 6 + 0] = indexb
                t[indexa * 6 + 1] = indexb + 1 + u
                t[indexa * 6 + 2] = indexb + 1

                t[indexa * 6 + 3] = indexb
                t[indexa * 6 + 4] = indexb + u
                t[indexa * 6 + 5] = indexb + u + 1
        return t
    return grid_verteces(u,v), grid_indeces(u,v), grid_colors(u,v)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_ALPHA | GLUT_DOUBLE)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Simple shaders")

    # //! Обязательно перед инициализации шейдеров

    # glew_status = GLenum(glewInit());
    if 0:  # GLEW_OK != glew_status):
        # //! GLEW не проинициализировалась
        #print("Error: ", glewGetErrorString(glew_status), "n")
        return 1

    # //! Проверяем доступность OpenGL 2.0
    if 0:  # not GLEW_VERSION_2_0):
        # //! OpenGl 2.0 оказалась не доступна
        print("No support for OpenGL 2.0 foundn")
        return 1

    # //! Инициализация
    initGL()
    initVBO()
    initShader()

    glutReshapeFunc(resizeWindow)
    glutDisplayFunc(render)
    glutIdleFunc(render)

    glutSpecialFunc(specialKeys)

    glutMainLoop()

    # //! Освобождение ресурсов
    freeShader()
    freeVBO()


if __name__ == '__main__':
    main()
