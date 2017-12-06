# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from ctypes import *
import sys
import array
from OpenGL_tools import *

class OpenGL_context:
	Program = None
	VertexPosition = None
	VertexColor = None
	VBO = None
	IndexPointer = None
	VertexPointer = None
	vao = None
	vertex = GLfloat_2 * 3
	indexesArray= None
	rMatrix = glm.mat4(1)
	indexes=None
	cameraPos = glm.vec3(1.0,1.0,1.0)	
	def __init__(s):
		s.VBO= None
		s.rMatrix = glm.mat4(1)
		s.mWorld =  glm.mat4(1)
		s.cameraPos = glm.vec3(1.0,1.0,1.0)	
		s.mWorld = glm.translate(s.mWorld, s.cameraPos)
		#s.mProjection = glm.perspective(0.7853,1.333,0.001,5.0)
		s.mProjection = glm.perspectiveFov(45.0,800,600,0.001,100.0)
		s.mView = glm.lookAt(glm.vec3(5,5,5),
							glm.vec3(0,0,0),
							glm.vec3(0,1,0))
		vw = s.mView * s.mWorld
		s.mNormal = glm.inverse(glm.mat3(glm.vec3(vw[0]), glm.vec3(vw[1]), glm.vec3(vw[2])))
		s.sLight = LightInfo(GLfloat_4(0,1.0,0,1.0))
		s.sMaterial = MaterialInfo()
	
	def specialKeys(s,key, x, y):
		# Сообщаем о необходимости использовать глобального массива pointcolor
		# Обработчики специальных клавиш
		if key == GLUT_KEY_UP:  # Клавиша вверх
			s.mWorld = glm.translate(s.mWorld, glm.vec3(0.2,0,0))
			s.cameraPos[0]+=0.2
		if key == GLUT_KEY_DOWN:  # Клавиша вниз
			s.mWorld = glm.translate(s.mWorld, glm.vec3(0,0.2,0))
			s.cameraPos[1]+=0.2
		if key == GLUT_KEY_LEFT:  # Клавиша влево
			s.mWorld = glm.translate(s.mWorld, glm.vec3(-0.2,0,0))
			s.cameraPos[0]-=0.2
		if key == GLUT_KEY_RIGHT:  # Клавиша вправо
			s.mWorld = glm.translate(s.mWorld, glm.vec3(0,-0.2,0))
			s.cameraPos[1]-=0.2
		if key == GLUT_KEY_PAGE_DOWN:  # Клавиша вправо
			s.mWorld = glm.translate(s.mWorld, glm.vec3(0,0,0.2))
			s.cameraPos[2]+=0.2
		if key == GLUT_KEY_PAGE_UP:  # Клавиша вправо
			s.mWorld = glm.translate(s.mWorld, glm.vec3(0,0,-0.2))
			s.cameraPos[2]-=0.2
		if key == GLUT_KEY_HOME or key == GLUT_KEY_END:
			s.cameraPos = glm.vec3(1.0,1.0,1.0)	
			s.mWorld = glm.translate(glm.mat4(1), s.cameraPos)
			print('reset')
			return 0

	def keys(s,key, x, y):
		if (key == '8'):
			s.mWorld = glm.rotate(s.mWorld,0.2,glm.vec3(0,1,0)) # rotate2D(s.rMatrix,15);
		if (key == '2'):
			s.mWorld=glm.rotate(s.mWorld,-0.2,glm.vec3(0,1,0)) # rotate2D(s.rMatrix,15);
		if (key == '6'):
			s.mWorld = glm.rotate(s.mWorld,0.2,glm.vec3(0,0,1))
		if (key == '4'):
			s.mWorld = glm.rotate(s.mWorld,-0.2,glm.vec3(0,0,1))
		if (key == '7'):
			s.mWorld = glm.rotate(s.mWorld,-0.2,glm.vec3(1,0,0))
		if (key == '9'):
			s.mWorld = glm.rotate(s.mWorld, 0.2, glm.vec3(1, 0, 0))
		if (key == '+'):
			s.mWorld = glm.scale(s.mWorld, glm.vec3(1.2,1.2,1.2))
			s.cameraPos*=1.2
		if (key == '-'):
			s.mWorld = glm.scale(s.mWorld, glm.vec3(0.8,0.8,0.8))
			s.cameraPos*=0.8
		if (key == 'q'):
			exit()

	##//! Функция печати лога шейдера
	def shaderLog(s,shader):
		infologLen = c_int(0)
		charsWritten = 0
		infoLog = None
	
		infoLog = glGetShaderiv(shader, GL_INFO_LOG_LENGTH, infologLen)
	
		if infologLen > 1:
			infoLog = '' #* infologLen
		if infoLog is None:
			print("ERROR: Could not allocate I http:#//www.pvsm.ru/opengl/20137nfoLog buffern")
			exit(1)
		print("InfoLog: ", infoLog, "nnn")
	
	
	##//! Инициализация OpenGL, здесь пока по минимальному=)
	def initGL(s):
		glClearColor(0, 0, 0, 0)
	
	
	##//! Проверка ошибок OpenGL, если есть то выводж в консоль тип ошибки
	def checkOpenGLerror(s):
		errCode = glGetError()
		if not (errCode == GL_NO_ERROR):
			print("OpenGl error! - ", str(gluErrorString(errCode)))
	
	
	# //! Освобождение шейдеров
	def freeShader(s):
		# //! Передавая ноль, мы отключаем шейдрную программу
		glUseProgram(0)
		# //! Удаляем шейдерную программу
		glDeleteProgram(s.Program)
	
	
	# //! Освобождение шейдеров
	def freeVBO(s):
		glBindBuffer(GL_ARRAY_BUFFER, s.VBO)
		glDeleteBuffers(2, s.VBO)
	
	
	def resizeWindow(s,width, height):
		glViewport(0, 0, width, height)
	
	
	def main(s):
		glutInit(sys.argv)
		glutInitDisplayMode(GLUT_RGBA | GLUT_ALPHA | GLUT_DOUBLE)
		glutInitWindowSize(800, 600)
		glutCreateWindow("View port shaders")
		
		# //! Инициализация
		s.initGL()
		s.initVBO(object='cube')
		s.initShader()
		s.initVBO(object='hexadron')
		
		glutReshapeFunc(s.resizeWindow)
		glutDisplayFunc(s.render)
		glutIdleFunc(s.render)
		
		glutSpecialFunc(s.specialKeys)
		glutKeyboardFunc(s.keys)
		glutMainLoop()
		
		# //! Освобождение ресурсов
		freeShader()
		freeVBO()
