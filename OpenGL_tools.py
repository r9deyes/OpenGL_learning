# OpenGL tools
import numpy as np
from OpenGL.GL import *
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

def load_obj(filename):
	"""
		return verteces, elements, normals
	"""
	with open(filename) as f:
		line=f.readline()
		vertices = []
		normals = []
		elements=[]
		while (line):
			if (line[0:2] == "v "):
				v= line[2:].split()
				verteces += [float(v[0]), float(v[1]), float(v[2]), 1.0]
			elif (line[0:2] == "f "):
				v= line[2:].split()
				elements += [int(v[0])-1, int(v[1])-1, int(v[2])-1]
			elif (line[0:3] == 'vn '):
				v= line[3:].split()
				normals += [float(v[0]), float(v[1]), float(v[2]), 1.0]
			elif (line[0] == '#'):
			{
				#/* ignoring this line */
			}
			else:
			{
				#/* ignoring this line */
			}
			line=f.readline()
		if (len(normals)<len(verteces)):
			for i in range(0,len(elements),3):
				ia = elements[i  ]*4
				ib = elements[i+1]*4
				ic = elements[i+2]*4
				normal = normalize(np.cross(\
				(vertices[ib] - vertices[ia],vertices[ib+1] - vertices[ia+1],vertices[ib+2] - vertices[ia+2]),\
				(vertices[ic] - vertices[ia],vertices[ic+1] - vertices[ia+1],vertices[ic+2] - vertices[ia+2])))
				normals[ia] = normals[ib] = normals[ic] = normal
	return verteces, elements, normals

def normalize(v):
	norm = np.linalg.norm(v)
	if norm == 0: 
		return v
	return v / norm

def hexadron():
	vertexes = [0, 0.6, 0.35	,#/0
	0.42, 0.42, 0.35 ,#/1
	0.6, 0, 0.35	 ,#2
	0.42, -0.42, 0.35,#3
	0, -0.6, 0.35	,#4
	-0.42, -0.42, 0.35,#/5
	-0.6, 0, 0.35	,#6
	-0.42, 0.42, 0.35,#7
	#***median_hexadron***//   
	0, 1, 0		, #8
	0.71, 0.71, 0  , #9
	1, 0, 0		, #10
	0.71, -0.7, 0  , #11
	0,-1,0		 , #12
	-0.71, -0.71, 0, #13
	-1, 0, 0	   , #14
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