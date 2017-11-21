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
	
	
	
	def specialKeys(key, x, y):
		# Сообщаем о необходимости использовать глобального массива pointcolor
		global s.rMatrix
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
	def keys(key, x, y):
		if (key == 'i'):
			return 0
		if (key == 'j'):
			return 0
		if (key == 'k'):
			return 0
		if (key == 'l'):
			return 0
	
	
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
	
	
	# //! Освобождение шейдеров
	def freeShader():
		global s.Program
		# //! Передавая ноль, мы отключаем шейдрную программу
		glUseProgram(0)
		# //! Удаляем шейдерную программу
		glDeleteProgram(s.Program)
	
	
	# //! Освобождение шейдеров
	def freeVBO():
		global s.VBO
		glBindBuffer(GL_ARRAY_BUFFER, s.VBO)
		glDeleteBuffers(2, s.VBO)
	
	
	def resizeWindow(width, height):
		glViewport(0, 0, width, height)
	
	
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
		glutKeyboardFunc(keys)
		glutMainLoop()
	
		# //! Освобождение ресурсов
		freeShader()
		freeVBO()

class main(OpenGL_context):
	
	def __init__(s):
		super(OpenGL_context,s).__init__()
	
	def initShader():
		with open('./camera_projection.vert') as f:
			vsSource = f.read()
	
		with open('./camera_projection.frag') as f:
			fsSource = f.read()
	
		vShader = glCreateShader(GL_VERTEX_SHADER)
		glShaderSource(vShader, vsSource)
		glCompileShader(vShader)
		print("vertex shader n")
		shaderLog(vShader)
	
		fShader = glCreateShader(GL_FRAGMENT_SHADER)
		glShaderSource(fShader, fsSource)
		glCompileShader(fShader)
		print("fragment shader n")
		shaderLog(fShader)
	
		s.Program = glCreateProgram()
		glAttachShader(s.Program, vShader)
		glAttachShader(s.Program, fShader)
	
		# //! Линкуем шейдерную программу
		glLinkProgram(s.Program)
	
		# //! Проверяем статус сборки
		link_ok = glGetProgramiv(s.Program, GL_LINK_STATUS)
		if not link_ok:
			print("error attach shaders n")
			return
		# ///! Вытягиваем ID атрибута из собранной программы
		def getAttribLocation(varName,type='att',check=0):
			if (type=='att'):
				var = glGetAttribLocation(s.Program, varName)
			elif(type=='uni'):
				var = glGetUniformLocation(s.Program, varName)
			
			if var == -1:
				print("could not bind attrib ", varName)
			if (check):
				print('glGetAttribLocation ',varName , var)
			return var
	
		global VertexPosition
		VertexPosition = getAttribLocation("VertexPosition")
	
		global  VertexNormal
		VertexNormal = GetAttribLocation(s.Program, "VertexColor")
		rMatrixName = 'RotationMatrix'
		global s.RotationMatrix
	
		s.RotationMatrix = glGetUniformLocation(s.Program, rMatrixName)
		print(':rMAtrix index: ', RotationMatrix)
		if RotationMatrix == -1:
			print("could not bind attrib ", rMatrixName)
			return
		checkOpenGLerror()
	
	
	# //! Инициализация VBO
	
	
	def initVBO():
		global s.VBO
		global s.IndexPointer
		global s.VertexPointer
		global s.vao
		global s.indexes
		global s.indexesArray
		global s.ColorPointer
	
		s.vao = glGenVertexArrays(1)
		s.VBO = glGenBuffers(3)
		s.IndexPointer = s.VBO[0]
		s.VertexPointer = s.VBO[1]
		s.ColorPointer = s.VBO[2]
		glBindBuffer(GL_ARRAY_BUFFER, s.VertexPointer)
	
		s.vertexes =  (c_float * 18)(*[-0.2, -0.4, 0.5,\
									-1.0, -0.8, 0.5,\
									-0.2, -0.8, 0.5,\
									0.7, 0.3, 1.0,\
									0.9, 0.5, 1.0,\
									0.9, 0.9, 1.0])
		#s.vertexes, s.indexes, s.colors = hexadron()
		#grid=(10,10)
		#s.vertexes = grid_verteces(*grid)
		glBufferData(GL_ARRAY_BUFFER, sizeof(s.vertexes), array.array('f',s.vertexes).tostring(), GL_STATIC_DRAW)
	
		s.colors = (c_float * 18)(*[0.5, 0.0, 0.0,\
								   0.5, 0.0, 0.0,\
								   0.5, 0.0, 0.0,\
								   1.0, 0.5, 0.0,\
								   1.0, 0.5, 0.0,\
								   1.0, 0.5, 0.0])
		#s.colors = grid_colors(*grid)
		glBindBuffer(GL_ARRAY_BUFFER, s.ColorPointer)
		glBufferData(GL_ARRAY_BUFFER, sizeof(s.colors), array.array('f', s.colors).tostring(), GL_STATIC_DRAW)
		#glVertexAttribPointer(1, 3 , GL_FLOAT, GL_FALSE, 0, None, 0)
	
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, s.IndexPointer)
	
		s.indexes = (c_ubyte * 6)(*[0,1,2, 3,4,5])
		#s.indexes = grid_indeces(*grid)
		s.indexesArray = array.array('B',s.indexes)
	
		glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(s.indexes), s.indexesArray.tostring(), GL_STATIC_DRAW)
		
		glBindVertexArray(s.vao)
	
		glBindBuffer(GL_ARRAY_BUFFER, s.VertexPointer)
	
		checkOpenGLerror()
	
	
	
	# //! Отрисовка
	def render():
		global s.Program
		global s.VertexColor
		global s.VertexPointer, s.ColorPointer, s.IndexPointer
		global s.VertexPosition, _color, s.RotationMatrix
		global s.rMatrix
		global s.indexes
		global s.indexesArray
		glClear(GL_COLOR_BUFFER_BIT)
		glUseProgram(s.Program)
	
		# //! Передаем юниформ в шейдер
		# print(Unif_color);
		glUniformMatrix4fv(s.RotationMatrix, GLint(1), GL_FALSE, s.rMatrix)
		# //! Включаем массив атрибутов
		glEnableVertexAttribArray(s.VertexPosition)
		glBindBuffer(GL_ARRAY_BUFFER, s.VertexPointer)
		glVertexAttribPointer(s.VertexPosition, 3, GL_FLOAT, GL_FALSE, 0, None)
	
		glEnableVertexAttribArray(s.VertexColor)
		glBindBuffer(GL_ARRAY_BUFFER, s.ColorPointer)
		glVertexAttribPointer(s.VertexColor, 3, GL_FLOAT, GL_FALSE, 0, None)
		#glBindBuffer(GL_ARRAY_BUFFER, VertexArray)
		#glPolygonMode(GL_FRONT, GL_LINE)
		glDrawElements(GL_TRIANGLES, len(s.indexesArray), GL_UNSIGNED_BYTE, s.indexesArray.tostring())
		#glDrawElements(GL_TRIANGLES,GLint(1), GL_UNSIGNED_BYTE, IndexArray)
		glDisableVertexAttribArray(s.VertexPosition)
		glDisableVertexAttribArray(s.VertexColor)
	
	
		# //! Отключаем шейдерную программу
		glUseProgram(0)
	
		checkOpenGLerror()
	
		glutSwapBuffers()


if __name__ == '__main__':
	app = main()
	app.main()
