### python projector library for projecting image slices in blender	
#	
#	author: Bereket Abraham
#	3D Volumetric Display Project
#	required: Blender >2.6, Python 3.2.3, 32-bit, PIL for python3, 32bit
#


def pointInsideMesh(ob, pt):
	import bpy, mathutils

	def ptInFaceXYBounds(ob, f, pt):
		xmax = ymax = -float('inf')
		xmin = ymin = float('inf')
		
		for vert in f.vertices:
			co = ob.data.vertices[vert].co.copy()
			co.resize_4d()
			co = obMat * co
			co.resize_3d()
			xmax= max(xmax, co.x)
			xmin= min(xmin, co.x)
			ymax= max(ymax, co.y)
			ymin= min(ymin, co.y)
		
		# Now we have the bounds, see if the point is in it.
		return xmin <= pt.x <= xmax and ymin <= pt.y <= ymax

	def faceIntersect(ob, f):
		co_0 = ob.data.vertices[f.vertices[0]].co.copy()
		co_0.resize_4d()
		co_0 = obMat * co_0
		co_0.resize_3d()
		
		co_1 = ob.data.vertices[f.vertices[1]].co.copy()
		co_1.resize_4d()
		co_1 = obMat * co_1
		co_1.resize_3d()
		
		co_2 = ob.data.vertices[f.vertices[2]].co.copy()
		co_2.resize_4d()
		co_2 = obMat * co_2
		co_2.resize_3d()
		
		isect = mathutils.geometry.intersect_ray_tri(co_0, co_1, co_2, ray, obSpacePt, True)
		if not isect and len(f.vertices) == 4:
			co_3 = ob.data.vertices[f.vertices[3]].co.copy()
			co_3.resize_4d()
			co_3 = obMat * co_3
			co_3.resize_3d()
			isect = mathutils.geometry.intersect_ray_tri(co_0, co_2, co_3, ray, obSpacePt, True)
		
		# This is so the ray only counts if its above the point.
		return bool(isect and isect.z > obSpacePt.z)

		
	ray = mathutils.Vector((0,0,-1))
	obSpacePt = pt.copy()
	obMat = mathutils.Matrix(ob.matrix_world)

	# Here we find the number on intersecting faces, return true if an odd number (inside), false (outside) if its true.
	return len([None for f in ob.data.faces if ptInFaceXYBounds(ob, f, obSpacePt) if faceIntersect(ob, f)]) % 2
	

	
def computeGrid(scn, showGrid, size):
	import bpy, mathutils

	xmax = size[0]
	ymax = size[1]
	zmax = size[2]

	table= [ [ 0 for i in range(xmax) ] for j in range(ymax) ]
	# rol, col
	for d1 in range(ymax):
		for d2 in range(xmax):
			# perform calculations
			x = d2 - ((xmax - 1)/2)
			y = d1 - ((ymax - 1)/2)
			
			z = helicoid_half(x, y, zmax)
			
			pt = mathutils.Vector((x, y, z))
			table[d1][d2] = 0
			
			for obj in bpy.data.objects:
				if obj.name != 'Lamp' and obj.name != 'Camera' and not 'grid' in obj.name:
					if pointInsideMesh(obj, pt) == 1:
						table[d1][d2] = 1
						break
			
			if showGrid:
				name = "grid" + str(d1) + "." + str(d2)
				grid_obj = createCube(scn, (x, y, z), 0.5, name)
				# change color
				if table[d1][d2] == 1:
					changeColor(grid_obj, (1.0, 0.3, 0.0))

	return table
	
def deleteGrid():
	import bpy
	for obj in bpy.data.objects:
		if 'grid' in obj.name:
			bpy.data.objects[obj.name].select = True
		else:
			bpy.data.objects[obj.name].select = False

	bpy.ops.object.delete()


################# everything above is useless ###########

def helicoid_half(x, y, zmax):
	import math
	z = (zmax/2/math.pi) * math.atan2(y,x)
	return z
    
def helicoid_full(x, y, zmax):
	import math
	z = (zmax/math.pi) * math.atan(y/x)
	return z
	
def slant(x, y, zmax):
	return x
	
def flat(x, y, zmax):
	return 0


def createCube(scn, loc, size, name):
	import bpy

	s = size/2.0
	coords=[(-s,-s,-s), (-s,s,-s), (s,s,-s), (s,-s,-s), \
	(-s,-s,s), (-s,s,s), (s,s,s), (s,-s,s)]

	# Define the faces by vertex index numbers. 4 numbers
	# For triangles you need to repeat the first vertex also in the fourth position.
	# order is CCW, outside looking in
	faces=[(0,1,2,3), (7,6,5,4), (0,4,5,1), (3,7,4,0), (2,6,7,3), (1,5,6,2)]
	me = bpy.data.meshes.new("CubeMesh")

	ob = bpy.data.objects.new(name, me)	# create an object with that mesh
	ob.location = loc
	bpy.context.scene.objects.link(ob)	# Link object to scene

	# Fill the mesh with verts, edges, faces
	me.from_pydata(coords,[],faces)
	me.update(calc_edges=True)
	return ob

	
def testSceneA(scale):
	import bpy, math
	
	loc = (-0.2*scale, 0.2*scale, 0.3*scale)
	ob = createCube(bpy.context.scene, loc, 0.1*scale, 'CubeA')
	
	ob.rotation_euler = (math.pi/4, 0.0, math.pi/4)
	changeColor(ob, (1.0, 0.3, 0))
	return ob

def testSceneB(scale):
	import bpy, math
	
	loc = (-0.2*scale, 0.2*scale, 0.3*scale)
	bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, size=0.1*scale, location=loc)
	ob = bpy.context.object	
	changeColor(ob, (1.0, 0.3, 0))
	return ob

def helicoidSurf(scn, size, name, type):
	import bpy

	xmax = size[0]
	ymax = size[1]
	zmax = size[2]
	coords = []
	faces = []
	cmax = xmax * ymax
	d5 = 0
	
	if type == 0:
		zfunc = helicoid_full
	else:
		zfunc = helicoid_half
	
	# row, col
	for d1 in range(ymax):
		for d2 in range(xmax):
			# perform calculations
			x = d2 - ((xmax - 1)/2)
			y = d1 - ((ymax - 1)/2)
			
			z = zfunc(x, y, zmax)
			coords.append((x,y,z))
			# table[d2][d1]
			
	for d3 in range(ymax):
		for d4 in range(xmax):
			if d3 < (ymax-1) and d4 < (ymax-1):
				faces.append((d5, d5+xmax, d5+xmax+1, d5+1))
			d5 += 1

	# Define the faces by vertex index numbers. 4 numbers
	# For triangles you need to repeat the first vertex also in the fourth position.
	# order is CCW, outside looking in

	me = bpy.data.meshes.new("CurvedMesh")
	ob = bpy.data.objects.new(name, me)	# create an object with that mesh
	ob.location = (0,0,0)
	bpy.context.scene.objects.link(ob)	# Link object to scene

	# Fill the mesh with verts, edges, faces
	me.from_pydata(coords,[],faces)
	me.update(calc_edges=True)
	
	
	# set Solidifier modifier
	bpy.ops.object.select_all(action='DESELECT') 
	bpy.context.scene.objects.active = ob
	bpy.ops.object.modifier_add(type='SOLIDIFY') 
	ob.modifiers[0].thickness = 0.1 
	# Apply
	bpy.ops.object.modifier_apply(apply_as='DATA', modifier=ob.modifiers[0].name) 
	
	# make black and non-reflective
	#mat = bpy.data.materials.new('helixmesh')
	#mat.diffuse_intensity = 0.0
	#mat.specular_intensity = 0.0
	#ob.data.materials.append(mat)
	
	return ob

def changeColor(ob, colors):
	import bpy
	mat = bpy.data.materials.new('colors')
	mat.diffuse_color = colors
	if len(ob.data.materials) < 1:
		ob.data.materials.append(mat)
	else:
		ob.data.materials[0] = mat

		
def makeInvisible(ob):
	import bpy
	mat = bpy.data.materials.new('invisible')
	mat.use_transparency = True
	mat.alpha = 0.0
	mat.specular_alpha = 0.0
	if len(ob.data.materials) < 1:
		ob.data.materials.append(mat)
	else:
		ob.data.materials[0] = mat


def setParameters(ob1, ob2, grid_res, cam_height, xres, yres):	# ob1 - ob2
	import bpy
	
	# positioning
	cam = bpy.data.objects['Camera']
	lamp = bpy.data.objects['Lamp']
	cam.location = (0,0,cam_height)
	cam.rotation_euler = (0,0,0)
	lamp.location = (0,0,cam_height+5)
	lamp.rotation_euler = (0,0,0)
	cam.data.type = 'ORTHO'	# 'PERSP'
	cam.data.ortho_scale = grid_res

	# lamp, make area/hemi and brighter?
	bpy.data.lamps['Lamp'].type = 'AREA'
	bpy.data.lamps['Lamp'].shadow_method = 'NOSHADOW'
	bpy.data.lamps['Lamp'].distance = cam_height
	bpy.data.lamps['Lamp'].size = grid_res
	
	# set Difference boolean modifier
	bpy.ops.object.select_all(action='DESELECT') 
	bpy.context.scene.objects.active = ob1
	bpy.ops.object.modifier_add(type='BOOLEAN') 
	ob1.modifiers[0].object = ob2		# beware modifier stack order
	ob1.modifiers[0].operation = 'DIFFERENCE' 
	# Apply
	#bpy.ops.object.modifier_apply(apply_as='DATA', modifier=ob1.modifiers[0].name) 

	
	# set image render properties
	rend = bpy.context.scene.render
	rend.image_settings.file_format = 'PNG'
	rend.image_settings.color_mode = 'RGBA' # use alpha channel for color
	rend.image_settings.compression = 0
	rend.resolution_x = xres
	rend.resolution_y = yres
	rend.resolution_percentage = 100
	

def processFrame(xres, yres, image_num, fpi, home_dir):
	import sys
	# windows specific
	sys.path.append("C:/Python32/Lib/site-packages")
	# now able to import external libs
	
	from PIL import Image, _imaging
	
	colormap = [''] * xres * yres * 3    # RGB
	for i in range(fpi):
		color = int(i/(fpi/3))
		# open frame image
		img = Image.open(home_dir +'/frame'+ str(i+image_num*fpi) +'.png')
		pix = img.load() # this is not a list, nor is it list()'able
		width, height = img.size
		j = 0
		for x in range(xres):
			for y in range(yres):
				if x >= width or y >= height:	# LSB vs MSB
					colormap[j*3 + color] = colormap[j*3 + color] + '0'
				else:
					alpha = pix[x, y][3]
					if alpha > 252:     # opaque
						colormap[j*3 + color] = colormap[j*3 + color] + '0'
					else:				# transparent
						colormap[j*3 + color] = colormap[j*3 + color] + '1'
				j += 1
	
	# create new composite image
	imgb = Image.new('RGB', (xres, yres), (0,0,0))
	pix = imgb.load()
	
	# convert colormap from str to byte to int
	# pixel (RGB), time order (BRG)
	j = 0
	for x in range(xres):
		for y in range(yres):
			r = int(colormap[j*3 + 0], 2)
			g = int(colormap[j*3 + 1], 2)
			b = int(colormap[j*3 + 2], 2)
			pix[x, y] = (r, g, b)
			j += 1
	
	# save image
	imgb.save(home_dir +'/image'+ str(image_num) +'.png')
	


def execute():
	import bpy, math
		
	xres = 480
	yres = 320
	grid_res = 100
	hd_ratio = 1	# height to diameter ratio
	home_dir = r'C:/Users/Bereket/Documents/BlenderModels/run0'
	fpi = 24		# frames per screen image
	fpr = 72		# frames per revolution
	num_rev = 1		# number of revolutions
	fps = 60
	image_num = 0	# current image number
	
	# just for testing
	bpy.ops.object.select_all(action='SELECT')
	bpy.data.objects['Lamp'].select = False
	bpy.data.objects['Camera'].select = False
	bpy.ops.object.delete()
	
	# create projector surface
	ob_surf = helicoidSurf(bpy.context.scene, (grid_res, grid_res, grid_res*hd_ratio), "HSurf", 1)
	
	# import objects / create cube
	ob2 = testSceneA(grid_res)
	# just one for now, in future flip diff between objects
	# set parameters
	makeInvisible(ob2)
	setParameters(ob_surf, ob2, grid_res, grid_res, xres, yres)
	
	print('Computing frames...')
	inc = 2*math.pi/fpr
	for s in range(num_rev):
		for t in range(fpr):
			ob_surf.rotation_euler = (0.0, 0.0, t*inc)
			count = s*fpr + t
			bpy.context.scene.render.filepath = home_dir +'/frame'+ str(count) +'.png'
			bpy.ops.render.render(write_still=True)
			
			if (count+1) % fpi == 0:
				# multiplex images
				processFrame(xres, yres, image_num, fpi, home_dir)
				image_num += 1
	
	# form .mov movie with exact frame timing




if __name__ == '__main__':
	
	# find working directory, path
	execute()
	