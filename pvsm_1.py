# -*- coding: utf-8 -*-
#  include "include/GL/glew.h"
# include "include/GL/glut.h"

# include <iostream>
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import numpy as np

##//! Переменные с индентификаторами ID
##//! ID шейдерной программы
Program = None;
##//! ID атрибута
Attrib_vertex = None;
##//! ID юниформ переменной цвета
VertexColor = None;
VBO = None;
IndexPointer = None;
VertexPointer = None;
vao = None;
vertex = GLfloat_2 * 3;
_color = GLfloat_4(1.0, 0.0, 0.0, 1.0);

def sizeof(obj):
    return sys.getsizeof(obj)

def specialkeys(key, x, y):
    # Сообщаем о необходимости использовать глобального массива pointcolor
    global _color;
    # Обработчики специальных клавиш
    if key == GLUT_KEY_UP:          # Клавиша вверх
        if (_color[0]<1.0):
            _color[0]+=0.17
        else:
            _color[0]=0.0       # Вращаем на 5 градусов по оси X
    if key == GLUT_KEY_DOWN:        # Клавиша вниз
        if (_color[1]<1.0):
            _color[1]+=0.17
        else:
            _color[1]=0.0      # Вращаем на -5 градусов по оси X
    if key == GLUT_KEY_LEFT:        # Клавиша влево
        if (_color[2]<1.0):
            _color[2]+=0.17
        else:
            _color[2]=0.0
    if key == GLUT_KEY_RIGHT:       # Клавиша вправо
        if (_color[3]<1.0):
            _color[3]+=0.17
        else:
            _color[3]=0.0
    #print('_color:',_color[0:2])

##//! Функция печати лога шейдера
def shaderLog(shader):
    infologLen = 0;
    charsWritten = 0;
    infoLog = None;

    infoLog = glGetShaderiv(shader, GL_INFO_LOG_LENGTH, infologLen);

    if (infologLen > 1):
        infoLog = '' * infologLen;
    if (infoLog == None):
        print("ERROR: Could not allocate I http:#//www.pvsm.ru/opengl/20137nfoLog buffern");
        exit(1);
    #glGetShaderInfoLog(shader, infologLen, charsWritten, infoLog);
    print("InfoLog: ", infoLog, "nnn");
    # delete[]
    infoLog;


##//! Инициализация OpenGL, здесь пока по минимальному=)
def initGL():
    glClearColor(0, 0, 0, 0);


##//! Проверка ошибок OpenGL, если есть то выводж в консоль тип ошибки
def checkOpenGLerror():
    errCode = glGetError();
    if (not( errCode == GL_NO_ERROR)):
        print("OpenGl error! - ", str(gluErrorString(errCode)));


##//! Инициализация шейдеров
def initShader():
    ##//! Исходный код шейдеров
    vsSource = \
        "" \
        "layout(location=0) in vec2 coord;" + \
        "void main() {" + \
        "  gl_Position = vec4(coord.xy, 0.0, 1.0);" \
        "}";
    fsSource = \
        "" \
        "uniform vec4 color; " \
        "void main() {" + \
        "  gl_FragColor = color;" + \
        "}";

    ##//! Переменные для хранения идентификаторов шейдеров
    vShader, fShader = GLuint(), GLuint();

    # //! Создаем вершинный шейдер
    vShader = glCreateShader(GL_VERTEX_SHADER);
    # //! Передаем исходный код
    glShaderSource(vShader,  vsSource);
    # //! Компилируем шейдер
    glCompileShader(vShader);

    print("vertex shader n");
    shaderLog(vShader);

    # //! Создаем фрагментный шейдер
    fShader = glCreateShader(GL_FRAGMENT_SHADER);
    # //! Передаем исходный код
    glShaderSource(fShader,fsSource);
    # //! Компилируем шейдер
    glCompileShader(fShader);

    print("fragment shader n");
    shaderLog(fShader);

    # //! Создаем программу и прикрепляем шейдеры к ней
    global Program;
    Program = glCreateProgram();
    glAttachShader(Program, vShader);
    glAttachShader(Program, fShader);

    # //! Линкуем шейдерную программу
    glLinkProgram(Program);

    # //! Проверяем статус сборки
    link_ok = glGetProgramiv(Program, GL_LINK_STATUS);
    if (not link_ok):
        print("error attach shaders n");
        return;
    # ///! Вытягиваем ID атрибута из собранной программы
    attr_name = "coord";

    global Attrib_vertex;
    Attrib_vertex = glGetAttribLocation(Program, attr_name);
    print('glGetAttribLocation Attrib_vertex',Attrib_vertex);
    if (Attrib_vertex == -1):
        print("could not bind attrib " ,attr_name);
        return;
# //! Вытягиваем ID юниформ
    unif_name = "color";
    global  VertexColor;
    VertexColor = glGetUniformLocation(Program, unif_name);
    if (VertexColor == -1):
        print("could not bind uniform " ,unif_name );
        return;
    checkOpenGLerror();


# //! Инициализация VBO


def initVBO():
    global VBO;
    global IndexPointer;
    global VertexPointer;
    global vao;

    vao = glGenVertexArrays(1);
    VBO=glGenBuffers(2);
    IndexArray=VBO[0];
    VertexArray=VBO[1];
    glBindBuffer(GL_ARRAY_BUFFER, VertexArray);
    # //! Вершины нашего треугольника

    triangle = (GLfloat_2 * 6)(  GLfloat_2(0.2, 0.2),
                        GLfloat_2(0.4, 0.8),
                        GLfloat_2(0.2, 0.8),
                        GLfloat_2(0.6, 0.2),
                        GLfloat_2(0.8, 0.2),
                        GLfloat_2(0.8, 0.8));
    # //! Передаем вершины в буфер
    glBufferData(GL_ARRAY_BUFFER, sizeof(triangle),triangle, GL_STATIC_DRAW);

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,IndexArray);
    indexes=(GLuint * 3 * 2)( (0,1,2),
                            (3,4,5));
    glBufferData(GL_ELEMENT_ARRAY_BUFFER,sizeof(indexes),indexes,GL_STATIC_DRAW);

    glBindVertexArray(vao);
    glEnableVertexAttribArray(0);
    glBindBuffer(GL_ARRAY_BUFFER, VertexArray);

    checkOpenGLerror();


# //! Освобождение шейдеров
def freeShader():
    global Program;
    # //! Передавая ноль, мы отключаем шейдрную программу
    glUseProgram(0);
    # //! Удаляем шейдерную программу
    glDeleteProgram(Program);


# //! Освобождение шейдеров
def freeVBO():
    global VBO;
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glDeleteBuffers(2,VBO);



def resizeWindow(width, height):
    glViewport(0, 0, width, height);


# //! Отрисовка
def render():
    global Program;
    global VertexColor;
    global VBO;
    global VertexPointer;
    global IndexPointer;
    global Attrib_vertex;
    global _color;
    glClear(GL_COLOR_BUFFER_BIT);
# //! Устанавливаем шейдерную программу текущей
    glUseProgram(Program);


    # //! Передаем юниформ в шейдер
    #print(Unif_color);
    glUniform4fv(VertexColor, 1, _color);
    #print('color: ',_color[0])
    #VBO=glGenBuffers(1);
    #glBindBuffer(GL_ARRAY_BUFFER, VBO);

    #triangle = vertex(GLfloat_2(-1.0, -1.0),
    #                  GLfloat_2(0.0, 1.0),
    #                  GLfloat_2(1.0, -1.0));
    ##VBO=vbo.VBO(triangle);
    # //! Передаем вершины в буфер
    #glBufferData(GL_ARRAY_BUFFER, sizeof(triangle), triangle, GL_STATIC_DRAW);

    #print('bind VBO render', VBO);
    #glBindBuffer(GL_ARRAY_BUFFER, VBO);
    # //! Включаем массив атрибутов
    #print('Atribe vertex value= ',Attrib_vertex);

    glEnableVertexAttribArray(Attrib_vertex);

    ##VBO.bind();
    # //! Указывая pointer 0 при подключенном буфере, мы указываем что данные в VBO
    glVertexAttribPointer(Attrib_vertex, 2, GL_FLOAT, GL_FALSE, 0, None);
    # //! Отключаем VBO
    glBindBuffer(GL_ARRAY_BUFFER, VertexArray);
    # //! Передаем данные на видеокарту(рисуем)
    glDrawArrays(GL_TRIANGLES, 0, sizeof(GLfloat_2));

    # //! Отключаем массив атрибутов
    glDisableVertexAttribArray(Attrib_vertex);

    # //! Отключаем шейдерную программу
    glUseProgram(0);

    checkOpenGLerror();

    glutSwapBuffers();


def main( ):
    glutInit(sys.argv);
    glutInitDisplayMode(GLUT_RGBA | GLUT_ALPHA | GLUT_DOUBLE);
    glutInitWindowSize(800, 600);
    glutCreateWindow("Simple shaders");

    # //! Обязательно перед инициализации шейдеров

    #glew_status = GLenum(glewInit());
    if (0):#GLEW_OK != glew_status):
        # //! GLEW не проинициализировалась
        print( "Error: " , glewGetErrorString(glew_status) , "n");
        return 1;


    # //! Проверяем доступность OpenGL 2.0
    if (0):#not GLEW_VERSION_2_0):
        # //! OpenGl 2.0 оказалась не доступна
        print("No support for OpenGL 2.0 foundn");
        return 1;

    # //! Инициализация
    initGL();
    initVBO();
    initShader();

    glutReshapeFunc(resizeWindow);
    glutDisplayFunc(render);
    glutIdleFunc(render);

    glutSpecialFunc(specialkeys)

    glutMainLoop();

    # //! Освобождение ресурсов
    freeShader();
    freeVBO();

if __name__=='__main__':
    main();