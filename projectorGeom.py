
def computeGrid(scn, showGrid, size):
	import pointInside, makeCube, gridGeom, bpy, mathutils, imp
	imp.reload(pointInside)
	imp.reload(makeCube)
	imp.reload(gridGeom)

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
			
			z = gridGeom.helicoid_half(x, y, zmax)
			
			pt = mathutils.Vector((x, y, z))
			table[d1][d2] = 0
			
			for obj in bpy.data.objects:
				if obj.name != 'Lamp' and obj.name != 'Camera' and not 'grid' in obj.name:
					if pointInside.pointInsideMesh(obj, pt) == 1:
						table[d1][d2] = 1
						break
			
			if showGrid:
				name = "grid" + str(d1) + "." + str(d2)
				grid_obj = makeCube.createCube(scn, (x, y, z), 0.5, name)
				# change color
				if table[d1][d2] == 1:
					mat = bpy.data.materials.new('visuals')
					mat.diffuse_color = (1.0, 0.3, 0.0)
					if len(grid_obj.data.materials) < 1:
						grid_obj.data.materials.append(mat)
					else:
						grid_obj.data.materials[0] = mat

	return table
	
	
	
if __name__ == '__main__':
	import bpy
	scn = bpy.context.scene
	t = computeGrid(scn, True, (10,10,10))
	print('results of grid:')
	print(t)
