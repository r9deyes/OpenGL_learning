# OpenGL tools
import numpy as np
from OpenGL.GL import *
import glm

class glslStruct:
	
	def export(s,f_export,varName):
		for n in s.__dict__.keys():
			s.__dict__[n] = f_export(varName+'.'+n)

	def link(s, value,*args):
		f={'1f':glUniform1fv,
			'2f':glUniform2fv,
			'3f':glUniform3fv,
			'4f':glUniform4fv,
			'1i':glUniform1iv}
		for n in s.__dict__.keys():
			if hasattr(s.__dict__[n],'__len__'):
				f=f+str(len(s.__dict__[n]))+'fv'
			else:
				f=f+'1f'
			print(f,' ',str(s.__dict__[n]))
			f=getattr(OpenGL.GL, f)
			#f(s.__dict__[n],*args,value.__dict__[n])

class LightInfo(glslStruct):
	Position=None
	La = None
	Ld = None
	Ls = None
	def __init__(s,Position=None,La=None,Ld=None,Ls=None):
		s.Position= Position or GLfloat_4(1.0, 1.0, 1.0, 0.0)
		s.La = La or GLfloat_3(0.2,0.2,0.2)
		s.Ld = Ld or GLfloat_3(0.8,0.8,0.8)
		s.Ls = Ls or GLfloat_3(1.0,1.0,1.0)
	def link(s,value,*args):
		ar = [s.Position]+list(args)+[value.Position]
		glUniform4fv(*ar)
		ar = [s.La]+list(args)+[value.La]
		glUniform3fv(*ar)
		ar = [s.Ld]+list(args)+[value.Ld]
		glUniform3fv(*ar)
		ar = [s.Ls]+list(args)+[value.Ls]
		glUniform3fv(*ar)

class MaterialInfo(glslStruct):
	shininess=None
	Ka = None
	Kd = None
	Ks = None
	def __init__(s,shininess=None,Ka=None,Kd=None,Ks=None):
		s.shininess= shininess or GLfloat(1.0)
		s.Ka = Ka or GLfloat_3(0.2,0.2,0.2)
		s.Kd = Kd or GLfloat_3(0.8,0.8,0.8)
		s.Ks = Ks or GLfloat_3(1.0,1.0,1.0)			
	def link(s,value,*args):
		glUniform1f(s.shininess,value.shininess)
		ar = [s.Ka]+list(args)+[value.Ka]
		glUniform3fv(*ar)
		ar = [s.Kd]+list(args)+[value.Kd]
		glUniform3fv(*ar)
		ar = [s.Ks]+list(args)+[value.Ks]
		glUniform3fv(*ar)
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
		return vertices, elements, normals
	"""
	with open(filename) as f:
		line=f.readline()
		vertices = []
		normals = []
		elements=[]
		while (line):
			if (line[0:2] == "v "):
				v= line[2:].split()
				vertices += [float(v[0]), float(v[1]), float(v[2])]
			elif (line[0:2] == "f "):
				v= line[2:].split()
				elements += [int(v[0].split('/')[0])-1, int(v[1].split('/')[0])-1, int(v[2].split('/')[0])-1]
			elif (line[0:3] == 'vn '):
				v= line[3:].split()
				normals += [float(v[0]), float(v[1]), float(v[2])]
			elif (line[0] == '#'):
				line=f.readline()
				continue #/* ignoring this line */
			else:
				line=f.readline()
				continue #/* ignoring this line */
			line=f.readline()
		if (len(normals)<len(vertices)):
			for i in range(0,len(elements),3):
				ia = elements[i  ]*3
				ib = elements[i+1]*3
				ic = elements[i+2]*3
				normal = normalize(np.cross(\
				(vertices[ib] - vertices[ia],vertices[ib+1] - vertices[ia+1],vertices[ib+2] - vertices[ia+2]),\
				(vertices[ic] - vertices[ia],vertices[ic+1] - vertices[ia+1],vertices[ic+2] - vertices[ia+2])))
				normals[ia] = normals[ib] = normals[ic] = normal
	return vertices, elements, normals

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
	
def sizeof(object):
	#return sys.getsizeof(object)
	return object.__sizeof__()

def array2GL(GLtype, array):
	c = len(array)
	c1 = len(array[0])
	return ((GLtype * c1) * c)(*[(GLtype * c1)(*ar) for ar in array])

#def lookAt(matrix, eyePosition3D, center3D, upVector3D):
#	matrix2 = np.matrix([[1.0, 0.0, 0.0, 0.0],
#						[0.0, 1.0,0.0,0.0],
#						[0.0, 0.0, 1.0,0.0],
#						[0.0, 0.0, 0.0, 1.0]])
#	
#	forward = np.array(center3D) - np.array(eyePosition3D)
#	
#	forward=normalize(forward)
#	side = np.cross(forward, upVector3D)
#	side=normalize(side)
#	
#	up = np.cross(side, forward)
#	matrix2[0,0], matrix2[1,0], matrix2[2,0], matrix2[3,0] = side[0], side[1], side[2], 0.0
#	matrix2[0,1], matrix2[1,1], matrix2[2,1], matrix2[3,1] = up[0], up[1], up[2], 0.0
#	matrix2[0,2], matrix2[1,2], matrix2[2,2], matrix2[3,2] = -forward[0], -forward[1], -forward[2], 0.0
#	matrix2[0,3] =matrix2[1,3]= matrix2[2,3]= matrix2[3,0] =0.0
#	matrix2[3,3]=1.0
#	
#	matrix2 =  [[side[0], side[1],side[2],-np.dot(side,eyePosition3D)],
#				[up[0], up[1], up[2], -np.dot(up,eyePosition3D)],
#				[-forward[0],-forward[1],-forward[2],-np.dot(forward,eyePosition3D)],
#				[0.0, 0.0, 0.0, 1.0]]
#	
#	return matrix2
#
#def translate(matrix, vector, firstpos=np.array([0,0,0])):
#	res = np.matrix(matrix.copy())
#	for i in range(len(firstpos)):
#		matrix[i,-1] = firstpos[i]
#	return matrix * vector
#	
#def scale(matrix, coef):
#	return matrix * coef

#class rotations:
#	phi, psi, theta = 0, 0, 0
#	rMatrix =  None
#	def __init__(self):
#		self.rMatrix = array2GL(GLfloat, [[1.0, 0.0, 0.0, 0.0],
#									[0.0, 1.0,0.0,0.0],
#									[0.0, 0.0, 1.0,0.0],
#									[0.0, 0.0, 0.0, 1.0]])
#		self.phi, self.psi, self.theta = 0, 0, 0
#	
#	def __call__(self,dphi, dpsi=0,dtheta=0):
#		self.phi = 0 if self.phi + dphi>360 else self.phi + dphi
#		self.psi = 0 if self.psi + dpsi>360 else self.psi + dpsi
#		self.theta = 0 if self.theta + dtheta>360 else self.theta + dtheta
#		ar = transforms3d.euler.euler2mat(np.radians(self.theta), np.radians(self.psi), np.radians(self.phi))
#		res=np.array(self.rMatrix)
#		res[:3,:3] = ar
#		return array2GL(GLfloat, res)
#	
#	def _rotationMatrix(theta,dpsi=0):
#		self.phi = self.phi + theta
#		theta = 0 if self.phi > 360 else self.phi
#		self.phi = theta
#		theta = float(np.radians(theta))
#		c, s = float(np.cos(theta)), float(np.sin(theta))
#		R =array2GL(GLfloat, [[c, -s,0.0,0.0],
#					[s, c,0.0,0.0],
#					[0.0,0.0,1.0,0.0],
#					[0.0,0.0,0.0,1.0]])
#		return R
if __name__=="__main__":
	pass