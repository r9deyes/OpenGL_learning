# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from ctypes import *
import sys
import time
import array

def sizeof(object):
    return sys.getsizeof(object)

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
IndexArray = None
VertexArray = None
vao = None
vertex = GLfloat_2 * 3
_color = GLfloat_4(1.0, 0.0, 0.0, 1.0)
RotationMatrix = None
rMatrix = array2GL(GLfloat, [[1.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0,0.0,0.0],
                    [0.0, 0.0, 1.0,0.0],
                    [0.0, 0.0, 0.0, 1.0]])

angle = 0
#rMatrix[0][0]=1.0

indexes=None



def rotationMatrix(theta):
    global angle
    angle = angle + theta
    theta = 0 if angle > 360 else angle
    angle = theta
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
        rMatrix=rotationMatrix(15) # rotate2D(rMatrix,15);
        return 0
    if key == GLUT_KEY_DOWN:  # Клавиша вниз
        rMatrix=rotationMatrix(-15) # rotate2D(rMatrix,15);
        return 0  # (rMatrix, -15);      # Вращаем на -5 градусов по оси X
    if key == GLUT_KEY_LEFT:  # Клавиша влево
        global angle
        angle = 0
        rMatrix = rotationMatrix(0)
    if key == GLUT_KEY_RIGHT:  # Клавиша вправо
        if _color[3] < 1.0:
            _color[3] += 0.17
        else:
            _color[3] = 0.0
    print('_color:', _color[0:2])


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
    Color = vec4(VertexColor,1.0); //vec4(1.0,0.0,0.0,1.0);
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
    global IndexArray
    global VertexArray
    global vao
    global indexes

    vao = glGenVertexArrays(1)
    VBO = glGenBuffers(3)
    IndexArray = VBO[0]
    VertexArray = VBO[1]
    ColorArray = VBO[2]
    glBindBuffer(GL_ARRAY_BUFFER, VertexArray)

    def grid_verteces(u=2,v=2):
        t=(GLfloat_3 * (v*u))()
        for i in range(u):
            for j in range(v):
                t[i*u + j] = GLfloat_3(i/float(u), j/float(v), 1.0)
        return t
    def grid_colors(u=2,v=2):
        t=(GLfloat_3 * (v*u))()
        for i in range(u):
            for j in range(v):
                t[i*u + j]=GLfloat_3((i*u + j)/float(u*v),1.0-(i*u + j)/float(u*v),0.5)
        return t
    def grid_indeces(u=2, v=2):
        t=(GLubyte * ((u-1)*(v-1)*6))()
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
    triangle = array2GL(GLfloat,[[-0.2, -0.4, 0.5],
                                [-1.0, -0.8, 0.5],
                                [-0.2, -0.8, 0.5],
                                [0.7, 0.3, 1.0],
                                [0.9, 0.5, 1.0],
                                [0.9, 0.9, 1.0]])
    #grid_verteces(3,3)#(GLfloat_3 * 6)(GLfloat_3(-0.2, -0.4, 0.5),
               #                        GLfloat_3(-1.0, -0.8, 0.5),
               #                        GLfloat_3(-0.2, -0.8, 0.5),
               #                        GLfloat_3(0.7, 0.3, 1.0),
               #                        GLfloat_3(0.9, 0.5, 1.0),
               #                        GLfloat_3(0.9, 0.9, 1.0))
    glBufferData(GL_ARRAY_BUFFER, sizeof(triangle), triangle, GL_STATIC_DRAW)

    colors = array2GL(GLfloat,    [[0.5, 0.0, 0.0],
                                    [0.5, 0.0, 0.0],
                                    [0.5, 0.0, 0.0],
                                    [1.0, 0.5, 0.0],
                                    [1.0, 0.5, 0.0],
                                    [1.0, 0.5, 0.0]])
    #grid_colors(3,3)
             #(GLfloat_3 * 6)(GLfloat_3(0.5, 0.0, 0.0),
             #                GLfloat_3(0.5, 0.0, 0.0),
             #                GLfloat_3(0.5, 0.0, 0.0),
             #                GLfloat_3(1.0, 0.5, 0.0),
             #                GLfloat_3(1.0, 0.5, 0.0),
             #                GLfloat_3(1.0, 0.5, 0.0)
			#				 )
    glBindBuffer(GL_ARRAY_BUFFER, ColorArray)
    glBufferData(GL_ARRAY_BUFFER, sizeof(colors),colors,GL_STATIC_DRAW)
    #glVertexAttribPointer(1, 3 , GL_FLOAT, GL_FALSE, 0, None, 0)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IndexArray)
    #indexes =array2GL(GLuint, [[0, 1, 2], [3, 4, 5]])
        #grid_indeces(3,3)#= (GLubyte * 6)(0, 1, 2,\
             #               3, 4, 5)
    indexes = array.array('B', [0,1,2,3,4,5])
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indexes), indexes, GL_STATIC_DRAW)
    
    glBindVertexArray(vao)
    #glEnableVertexAttribArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, VertexArray)

    # glEnableVertexAttribArray(1)
    # glBindBuffer(GL_ARRAY_BUFFER,ColorArray)
    #
    # colors = (GLfloat_4 * 6)(GLfloat_4(1.0,0.0,0.0,1.0), GLfloat_4(1.0, 0.0, 0.0, 1.0), GLfloat_4(1.0, 0.0, 0.0, 1.0),
    #                          GLfloat_4(1.0, 1.0, 0.0, 1.0), GLfloat_4(1.0, 1.0, 0.0, 1.0),GLfloat_4(1.0, 1.0, 0.0, 1.0))
    # glBufferData(GL_ARRAY_BUFFER,sizeof(colors),colors,GL_STATIC_DRAW)

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
    global VertexColor;
    global VBO
    global VertexArray
    global IndexArray
    global Attrib_vertex
    global _color
    global RotationMatrix
    global rMatrix
    global indexes
    glClear(GL_COLOR_BUFFER_BIT)
    # //! Устанавливаем шейдерную программу текущей
    glUseProgram(Program)

    # //! Передаем юниформ в шейдер
    # print(Unif_color);
    glUniformMatrix4fv(RotationMatrix, GLint(1), GL_FALSE, rMatrix)
    # //! Включаем массив атрибутов
    glEnableVertexAttribArray(Attrib_vertex)

    ##VBO.bind();
    glVertexAttribPointer(Attrib_vertex, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(VertexColor)
    glVertexAttribPointer(VertexColor, 3, GL_FLOAT, GL_FALSE, 0, None)
    #glBindBuffer(GL_ARRAY_BUFFER, VertexArray)

    glDrawElements(GL_TRIANGLES,GLint(1), GL_UNSIGNED_BYTE, indexes)
    #glDrawElements(GL_TRIANGLES,GLint(1), GL_UNSIGNED_BYTE, IndexArray)

    glDisableVertexAttribArray(Attrib_vertex)

    # //! Отключаем шейдерную программу
    glUseProgram(0)

    checkOpenGLerror()

    glutSwapBuffers()


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
