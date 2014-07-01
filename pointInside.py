# Determine if a point lies within a 3D object using a ray casting algorithm
#
# Bereket Abraham

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


if __name__ == '__main__':
	import bpy	
	ob = bpy.context.active_object
	pt = bpy.context.scene.cursor_location
	inside = pointInsideMesh(ob, pt)
	print('Is cursor inside object? ' + str(inside))

