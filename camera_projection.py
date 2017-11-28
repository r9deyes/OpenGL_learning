# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from ctypes import *
import sys
import array
from OpenGL_tools import *
from OpenGL_context import *

class main(OpenGL_context):
	
	def initShader(s):
		with open('./camera_projection/camera_projection.vert') as f:
			vsSource = f.read()
	
		with open('./camera_projection/camera_projection.frag') as f:
			fsSource = f.read()
	
		vShader = glCreateShader(GL_VERTEX_SHADER)
		glShaderSource(vShader, vsSource)
		glCompileShader(vShader)
		print("vertex shader n")
		s.shaderLog(vShader)
	
		fShader = glCreateShader(GL_FRAGMENT_SHADER)
		glShaderSource(fShader, fsSource)
		glCompileShader(fShader)
		print("fragment shader n")
		s.shaderLog(fShader)
		
		s.Program = glCreateProgram()
		glAttachShader(s.Program, vShader)
		glAttachShader(s.Program, fShader)
		
		glLinkProgram(s.Program)
		
		link_ok = glGetProgramiv(s.Program, GL_LINK_STATUS)
		if not link_ok:
			print("error attach shaders n")
			return
		
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
		
		s.VertexPosition 	= getAttribLocation("VertexPosition")
		s.VertexNormal 		= getAttribLocation("VertexNormal")
		s.RotationMatrix 	= getAttribLocation('RotationMatrix','uni')
		s.Light 			= LightInfo()
		s.Light.export(lambda x: getAttribLocation(x,'uni'),'Light')
		s.Material 			= MaterialInfo()
		s.Material.export(lambda x: getAttribLocation(x,'uni'), 'Material')
		s.World 			= getAttribLocation('World','uni')
		s.View 				= getAttribLocation('View','uni')
		s.Projection 		= getAttribLocation('Projection','uni')
		s.Normal 			= getAttribLocation('Normal','uni')
		
		s.checkOpenGLerror()
	
	
	def initVBO(s):
		s.vao = glGenVertexArrays(1)
		s.VBO = glGenBuffers(4)
		s.IndexPointer = glGenBuffers(1)#s.VBO[0]
		s.VertexPointer = glGenBuffers(1)#s.VBO[1]
		s.ColorPointer = glGenBuffers(1)#s.VBO[2]
		s.NormalPointer = glGenBuffers(1)#s.VBO[3]
	
		VERTEX_COUNT = 18
		s.vertexes =  (c_float * VERTEX_COUNT)(\
									*[-0.2, -0.4, 0.5,\
									-1.0, -0.8, 0.5,\
									-0.2, -0.8, 0.5,\
									0.7, 0.3, 1.0,\
									0.9, 0.5, 1.0,\
									0.9, 0.9, 1.0])

		s.colors = (c_float * VERTEX_COUNT)(\
								*[0.5, 0.0, 0.0,\
								   0.5, 0.0, 0.0,\
								   0.5, 0.0, 0.0,\
								   1.0, 0.5, 0.0,\
								   1.0, 0.5, 0.0,\
								   1.0, 0.5, 0.0])

		s.indexes = (c_ubyte * 6)(*[0,1,2, 3,4,5])

		s.normals = (c_float * VERTEX_COUNT)(\
									*[-0.2, -0.4, 0.5,\
									1.0, -0.8, 0.5,\
									0.2, -0.8, 0.5,\
									0.7, 0.3, 1.0,\
									0.9, 0.5, 1.0,\
									0.9, 0.9, 1.0])

		#s.colors = grid_colors(*grid)

		#s.vertexes, s.indexes, s.colors = hexadron()
		#grid=(10,10)
		#s.vertexes = grid_verteces(*grid)

		#s.indexes = grid_indeces(*grid)
		glBindBuffer(GL_ARRAY_BUFFER, s.VertexPointer)
		glBufferData(GL_ARRAY_BUFFER, sizeof(s.vertexes), array.array('f',s.vertexes).tostring(), GL_STATIC_DRAW)
	
		glBindBuffer(GL_ARRAY_BUFFER, s.ColorPointer)
		glBufferData(GL_ARRAY_BUFFER, sizeof(s.colors), array.array('f', s.colors).tostring(), GL_STATIC_DRAW)
		#glVertexAttribPointer(1, 3 , GL_FLOAT, GL_FALSE, 0, None, 0)

		glBindBuffer(GL_ARRAY_BUFFER, s.NormalPointer)
		glBufferData(GL_ARRAY_BUFFER, sizeof(s.normals), array.array('f', s.normals).tostring(), GL_STATIC_DRAW)
		
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, s.IndexPointer)	
		s.indexesArray = array.array('B',s.indexes)
		glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(s.indexes), s.indexesArray.tostring(), GL_STATIC_DRAW)
		
		glBindVertexArray(s.vao)
		glBindBuffer(GL_ARRAY_BUFFER, s.VertexPointer)
				
		s.checkOpenGLerror()
	
	# //! Отрисовка
	def render(s):
		glClear(GL_COLOR_BUFFER_BIT)
		glUseProgram(s.Program)
			
		glEnableVertexAttribArray(s.VertexPosition)
		glBindBuffer(GL_ARRAY_BUFFER, s.VertexPointer)
		glVertexAttribPointer(s.VertexPosition, 3, GL_FLOAT, GL_FALSE, 0, None)
		
		glEnableVertexAttribArray(s.VertexNormal)
		glBindBuffer(GL_ARRAY_BUFFER, s.VertexNormal)
		glVertexAttribPointer(s.VertexNormal, 3, GL_FLOAT, GL_FALSE, 0, None)

		glUniformMatrix4fv(s.RotationMatrix, GLint(1), GL_FALSE, s.rMatrix)
		glUniformMatrix4fv(s.World, GLint(1), GL_FALSE, s.mWorld)
		glUniformMatrix4fv(s.View, GLint(1), GL_FALSE, s.mView)
		glUniformMatrix4fv(s.Projection, GLint(1), GL_FALSE, s.mProjection)
		glUniformMatrix3fv(s.Normal, 1, GL_FALSE, s.mNormal)
		
		s.Light.link(s.sLight,1,GL_FALSE)
		s.Material.link(s.sMaterial,1,GL_FALSE)
		
		glEnableVertexAttribArray(s.VertexColor)
		glBindBuffer(GL_ARRAY_BUFFER, s.ColorPointer)
		glVertexAttribPointer(s.VertexColor, 3, GL_FLOAT, GL_FALSE, 0, None)
		
		#glEnable(GL_BLEND);
		#glBlendFunc();
		glDrawElements(GL_TRIANGLES, len(s.indexesArray), GL_UNSIGNED_BYTE, s.indexesArray.tostring())
		#glDrawElements(GL_TRIANGLES,GLint(1), GL_UNSIGNED_BYTE, IndexArray)
		glDisableVertexAttribArray(s.VertexPosition)
		glDisableVertexAttribArray(s.VertexColor)
	
		glUseProgram(0)
	
		s.checkOpenGLerror()
	
		glutSwapBuffers()


if __name__ == '__main__':
	app = main()
	app.main()
