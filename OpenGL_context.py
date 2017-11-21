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

class OpenGL_context:
	Program = None
	VertexPosition = None
	VertexColor = None
	VBO = None
	IndexPointer = None
	VertexPointer = None
	vao = None
	vertex = GLfloat_2 * 3
	RotationMatrix = None
	indexesArray= None
	rMatrix = array2GL(GLfloat, [[1.0, 0.0, 0.0, 0.0],
						[0.0, 1.0,0.0,0.0],
						[0.0, 0.0, 1.0,0.0],
						[0.0, 0.0, 0.0, 1.0]])
	
	rotationMatrix = rotations()
	indexes=None
	
	def __init__(s):
		s.VBO= None
		s.rMatrix = array2GL(GLfloat, [[1.0, 0.0, 0.0, 0.0],
						[0.0, 1.0,0.0,0.0],
						[0.0, 0.0, 1.0,0.0],
						[0.0, 0.0, 0.0, 1.0]])
	
	def specialKeys(s,key, x, y):
		# Сообщаем о необходимости использовать глобального массива pointcolor
		# Обработчики специальных клавиш
		if key == GLUT_KEY_UP:  # Клавиша вверх
			s.rMatrix=rotationMatrix(9,0) # rotate2D(s.rMatrix,15);
		if key == GLUT_KEY_DOWN:  # Клавиша вниз
			s.rMatrix=rotationMatrix(-9,0) # rotate2D(s.rMatrix,15);
		if key == GLUT_KEY_LEFT:  # Клавиша влево
			s.rMatrix = rotationMatrix(0,9)
		if key == GLUT_KEY_RIGHT:  # Клавиша вправо
			s.rMatrix = rotationMatrix(0,-9)
		if key == GLUT_KEY_PAGE_DOWN:  # Клавиша вправо
			s.rMatrix = rotationMatrix(0,0,-9)
		if key == GLUT_KEY_PAGE_UP:  # Клавиша вправо
			s.rMatrix = rotationMatrix(0,0,9)
		if key == GLUT_KEY_HOME or key == GLUT_KEY_END:
			rotationMatrix.phi = 0
			rotationMatrix.psi = 0
			rotationMatrix.theta=0
			s.rMatrix = rotationMatrix(0,0,0)
			print('reset')
			return 0
	def keys(s,key, x, y):
		if (key == 'i'):
			return 0
		if (key == 'j'):
			return 0
		if (key == 'k'):
			return 0
		if (key == 'l'):
			return 0
	
	
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
		s.initVBO()
		s.initShader()
		
		glutReshapeFunc(s.resizeWindow)
		glutDisplayFunc(s.render)
		glutIdleFunc(s.render)
		
		glutSpecialFunc(s.specialKeys)
		glutKeyboardFunc(s.keys)
		glutMainLoop()
		
		# //! Освобождение ресурсов
		freeShader()
		freeVBO()
