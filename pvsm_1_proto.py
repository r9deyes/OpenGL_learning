#include "include/GL/glew.h"
#include "include/GL/glut.h"

#include <iostream>
from OpenGL.GL import *
from OpenGL.GLU import *
########################	from OpenGL.GLUT import *
from OpenGL.arrays import vbo
########################	import numpy as np

##//! Переменные с индентификаторами ID
##//! ID шейдерной программы
global Program=GLuint();
##//! ID атрибута
global Attrib_vertex=GLint();
##//! ID юниформ переменной цвета
global VertexColor=GLint;
##//! ID Vertex Buffer Object
##VBO=GLuint;

##//! Вершина
class vertex:
	x=GLfloat();
	y=GLfloat();
	def __init__(s,x=None,y=None):
		s.x=GLfloat(x);
		s.y=GLfloat(y);
#};

##//! Функция печати лога шейдера
def shaderLog(unsigned int shader):
	infologLen   = 0;
	charsWritten = 0;
	infoLog=None;
	
	glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &infologLen);
	########################	infoLog=--//--
	if(infologLen > 1)
	{ 
		infoLog = new char[infologLen];
		########################	infoLog = '' * infologLen;
		if(infoLog == None)
		{
			std::cout<<"ERROR: Could not allocate I"+\
			"http:#//www.pvsm.ru/opengl/20137nfoLog buffern";
			exit(1);
		}
		glGetShaderInfoLog(shader, infologLen, &charsWritten, infoLog);
		########################	#
		std::cout<< "InfoLog: " << infoLog << "nnn";
		delete[] infoLog;
  }
}

##//! Инициализация OpenGL, здесь пока по минимальному=)
def initGL():
	glClearColor(0, 0, 0, 0);

##//! Проверка ошибок OpenGL, если есть то выводж в консоль тип ошибки
def checkOpenGLerror():
	GLenum errCode; ########################	errCode = glGetError();
	if((errCode=glGetError()) != GL_NO_ERROR):
		std::cout << "OpenGl error! - " << gluErrorString(errCode);

##//! Инициализация шейдеров
def initShader():
	##//! Исходный код шейдеров
	vsSource = \
		"attribute vec2 coord;n"+\
		"void main() {n"+\
		"  gl_Position = vec4(coord.xy, 0.0, 1.0);n"+\
		"}n";
	fsSource = \
		"uniform vec4 color;n"+\
		"void main() {n"+\
		"  gl_FragColor = color;n"+\
		"}n";
	##//! Переменные для хранения идентификаторов шейдеров
	vShader, fShader=GLuint(),GLuint();
	
	#//! Создаем вершинный шейдер
	vShader = glCreateShader(GL_VERTEX_SHADER);
	#//! Передаем исходный код
	glShaderSource(vShader, 1, &vsSource, None); ###### glShaderSource(vShader,  vsSource);
	#//! Компилируем шейдер
	glCompileShader(vShader);
	
	std::cout << "vertex shader n";
	shaderLog(vShader);
	
	#//! Создаем фрагментный шейдер
	fShader = glCreateShader(GL_FRAGMENT_SHADER);
	#//! Передаем исходный код
	glShaderSource(fShader, 1, &fsSource, None); ##glShaderSource(fShader,fsSource);
	#//! Компилируем шейдер
	glCompileShader(fShader);

	std::cout << "fragment shader n";
	shaderLog(fShader);

	#//! Создаем программу и прикрепляем шейдеры к ней
	######################	global Program;
	Program = glCreateProgram();
	glAttachShader(Program, vShader);
	glAttachShader(Program, fShader);

	#//! Линкуем шейдерную программу
	glLinkProgram(Program);

	#//! Проверяем статус сборки
	int link_ok;
	glGetProgramiv(Program, GL_LINK_STATUS, &link_ok); ####link_ok = glGetProgramiv(Program, GL_LINK_STATUS);
	if(!link_ok)
	{
		std::cout << "error attach shaders n";
		return;
	}
	#///! Вытягиваем ID атрибута из собранной программы 
	const char* attr_name = "coord";
	Attrib_vertex = glGetAttribLocation(Program, attr_name);
	if(Attrib_vertex == -1)
	{
		std::cout << "could not bind attrib " << attr_name << std::endl;
		return;
	}
	#//! Вытягиваем ID юниформ
	const char* unif_name = "color";
	######################		global  Unif_color;
	VertexColor = glGetUniformLocation(Program, unif_name);
	if(VertexColor == -1)
	{
		std::cout << "could not bind uniform " << unif_name << std::endl;
		return;
	}
	
	checkOpenGLerror();


#//! Инициализация VBO
def initVBO():
  ##################	 global VBO;
  glGenBuffers(1, &VBO); ##VBO = --//--
  glBindBuffer(GL_ARRAY_BUFFER, VBO);
  #//! Вершины нашего треугольника
  vertex triangle[3] = { ######		vertex = GLfloat_2 * 3;
    {-1.0f,-1.0f},       ######
    { 0.0f, 1.0f},       ######triangle = vertex(GLfloat_2(-1.0,-1.0),
    { 1.0f,-1.0f}        ######                    GLfloat_2(0.0,  1.0),
  };                     ######                    GLfloat_2(1.0,-1.0));
  #//! Передаем вершины в буфер
  glBufferData(GL_ARRAY_BUFFER, sizeof(triangle), triangle, GL_STATIC_DRAW);

  checkOpenGLerror();

#//! Освобождение шейдеров
void freeShader()
{
  #//! Передавая ноль, мы отключаем шейдрную программу
  glUseProgram(0); 
  #//! Удаляем шейдерную программу
  glDeleteProgram(Program);
}

#//! Освобождение шейдеров
void freeVBO()
{
  ###############	global VBO;
  glBindBuffer(GL_ARRAY_BUFFER, 0); ######### --//--, VBO);
  glDeleteBuffers(1, &VBO);
}

void resizeWindow(int width, int height)
{
  glViewport(0, 0, width, height);
}

#//! Отрисовка
void render()
{
  #################global Program;
  #################global VBO;
  #################global Attrib_vertex;
  #################global Unif_color;
  glClear(GL_COLOR_BUFFER_BIT);
  #//! Устанавливаем шейдерную программу текущей
  glUseProgram(Program); 
  
  static float red[4] = {1.0f, 0.0f, 0.0f, 1.0f}; ######	= GLfloat_4(...
  #//! Передаем юниформ в шейдер
  glUniform4fv(VertexColor, 1, red);

  #//! Включаем массив атрибутов
  glEnableVertexAttribArray(Attrib_vertex);
    #//! Подключаем VBO
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
      #//! Указывая pointer 0 при подключенном буфере, мы указываем что данные в VBO
      glVertexAttribPointer(Attrib_vertex, 2, GL_FLOAT, GL_FALSE, 0, 0);
    #//! Отключаем VBO
    glBindBuffer(GL_ARRAY_BUFFER, 0);
    #//! Передаем данные на видеокарту(рисуем)
    glDrawArrays(GL_TRIANGLES, 0, sizeof (vertex));

  #//! Отключаем массив атрибутов
  glDisableVertexAttribArray(Attrib_vertex);

  #//! Отключаем шейдерную программу
  glUseProgram(0); 

  checkOpenGLerror();

  glutSwapBuffers();
}

int main( int argc, char **argv )
{
  glutInit(&argc, argv);
  glutInitDisplayMode(GLUT_RGBA | GLUT_ALPHA | GLUT_DOUBLE);
  glutInitWindowSize(800, 600);
  glutCreateWindow("Simple shaders");

  #//! Обязательно перед инициализации шейдеров
  GLenum glew_status = glewInit();
  if(GLEW_OK != glew_status) 
  {
     #//! GLEW не проинициализировалась
    std::cout << "Error: " << glewGetErrorString(glew_status) << "n";
    return 1;
  }

  #//! Проверяем доступность OpenGL 2.0
  if(!GLEW_VERSION_2_0) 
   {
     #//! OpenGl 2.0 оказалась не доступна
    std::cout << "No support for OpenGL 2.0 foundn";
    return 1;
  }

  #//! Инициализация
  initGL();
  initVBO();
  initShader();
  
  glutReshapeFunc(resizeWindow);
  glutDisplayFunc(render);
  glutMainLoop();
  
  #//! Освобождение ресурсов
  freeShader();
  freeVBO();
}