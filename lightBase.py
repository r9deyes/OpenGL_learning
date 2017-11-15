# -*- coding: utf-8 -*-
import np as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import numpy as np
import glm
import time


def sizeof(object):
    return sys.getsizeof(object)
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
rMatrix = np.array([[1.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0,0.0,0.0],
                    [0.0, 0.0, 1.0,0.0],
                    [0.0, 0.0, 0.0, 1.0]])
angle = 0
#rMatrix[0][0]=1.0



def rotationMatrix(theta):
    global angle
    angle = angle + theta
    theta = 0 if angle > 360 else angle
    angle = theta
    theta = np.radians(theta)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array([[c, -s,0.0,0.0],
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

    infologLen = 0
    charsWritten = 0
    infoLog = None

    infoLog = glGetShaderiv(shader, GL_INFO_LOG_LENGTH, c_int(infologLen))

    if infologLen > 1:
        infoLog = '' * infologLen
    if infoLog is None:
        print("ERROR: Could not allocate I http:#//www.pvsm.ru/opengl/20137nfoLog buffern")
        exit(1)
    # glGetShaderInfoLog(shader, infologLen, charsWritten, infoLog);
    print("InfoLog: ", infoLog, "nnn")
    # delete[]
    infoLog


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
    with open('./lightBase.vert') as f:
        vsSource =f.read()
    fsSource = """in vec3 LightIntensity;
out vec4 FragColor;
void main()
{
    FragColor=vec4(LightIntensity,1.0);
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
    def getAttribLocation(varName,type='att',check=0):
        if (type=='att'):
            var = glGetAttribLocation(Program, varName)
        elif(type=='uni'):
            var = glGetUniformLocation(Program, varName)
        
        if var == -1:
            print("could not bind attrib ", varName)
        if (check):
            print('glGetAttribLocation ',varName , var)
        return var

    global Attrib_vertex
    Attrib_vertex = getAttribLocation("VertexPosition")

    global  VertexColor;
    VertexColor = getAttribLocation("VertexColor");
    
    global RotationMatrix
    RotationMatrix = getAttribLocation("RotationMatrix",'uni')
    
    
    
    checkOpenGLerror()

# //! Инициализация VBO


def initVBO():
    global VBO
    global IndexArray
    global VertexArray
    global vao

    vao = glGenVertexArrays(1)
    VBO = glGenBuffers(2)
    IndexArray = VBO[0]
    VertexArray = VBO[1]
    #ColorArray = VBO[2]
    glBindBuffer(GL_ARRAY_BUFFER, VertexArray)
    # //! Вершины нашего треугольника

    triangle = (GLfloat_3 * 8)(GLfloat_3(0.0, -0.2, -0.2),
                               GLfloat_3(0.0, -0.4, -0.8),
                               GLfloat_3(0.0, -0.2, -0.8),
                               GLfloat_3(0.8, -0.3, -0.5),
                               GLfloat_3(0.0, 0.7, 0.3),
                               GLfloat_3(0.0, 0.9, 0.5),
                               GLfloat_3(0.0, 0.9, 0.9),
                               GLfloat_3(-0.8, 0.8, 0.6))
    # //! Передаем вершины в буфер
    glBufferData(GL_ARRAY_BUFFER, sizeof(triangle), triangle, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IndexArray)
    indexes = (GLuint * 3 * 8)((0, 1, 2), (3, 1, 2), (3, 0, 1), (3, 0, 2),
                               (4, 5, 6), (7, 4, 5), (7, 4, 6), (7, 5, 6))
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indexes), indexes, GL_STATIC_DRAW)


    glBindVertexArray(vao)
    glEnableVertexAttribArray(0)
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
    glClear(GL_COLOR_BUFFER_BIT)
    # //! Устанавливаем шейдерную программу текущей
    glUseProgram(Program)

    # //! Передаем юниформ в шейдер
    # print(Unif_color);
    glUniformMatrix4fv(RotationMatrix, 1, GL_FALSE, rMatrix)
    # //! Включаем массив атрибутов
    glEnableVertexAttribArray(Attrib_vertex)
    #glEnableVertexAttribArray(VertexColor)
    ##VBO.bind();
    glVertexAttribPointer(Attrib_vertex, 2, GL_FLOAT, GL_FALSE, 0, None)
    #glBindBuffer(GL_ARRAY_BUFFER, VertexArray)

    glDrawArrays(GL_TRIANGLES, 0, sizeof(GLfloat_2))

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

class LightInfo:
    Position=None
    La = None
    Ld = None
    Ls = None
    def __init__(s,Position=None,La=None,Ld=None,Ls=None):
        s.Position= Position or GLfloat_4(1.0, 1.0, 1.0, 0.0)
        s.La = La or GLfloat_3(0.2,0.2,0.2)
        s.Ld = Ld or GLfloat_3(0.8,0.8,0.8)
        s.Ls = Ls or GLfloat_3(1.0,1.0,1.0)
    
    def export(s,f_export,varName):
        for n in s.__dict__.keys():
            i=glGetUniformLocation(Program,varName+'.'+n)
            glUniform3fv(i,1,s.__dict__[n])
class MaterialInfo:
    shininess=None
    Ka = None
    Kd = None
    Ks = None
    def __init__(s,shininess=None,Ka=None,Kd=None,Ks=None):
        s.shininess= shininess or GLfloat(1.0)
        s.Ka = Ka or GLfloat_3(0.2,0.2,0.2)
        s.Kd = Kd or GLfloat_3(0.8,0.8,0.8)
        s.Ks = Ks or GLfloat_3(1.0,1.0,1.0)
    
    def export(s,f_export,varName):
        for n in s.__dict__.keys():
            f_export(varName+'.'+n)

if __name__ == '__main__':
    main()