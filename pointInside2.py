# Determine if a point lies within a 3D object using a ray casting algorithm
#
# Bereket Abraham

import bpy
import mathutils

def fetchIfObject (passedName= ""):
    try:
        result = bpy.data.objects[passedName]
    except:
        result = None
    return result
    
def pointInsideMesh(point,ob):
    axes = [ mathutils.Vector((1,0,0)) , mathutils.Vector((0,1,0)), mathutils.Vector((0,0,1))  ]
    outside = False
    for axis in axes:
        orig = point
        count = 0
        while True:
            location,normal,index = ob.ray_cast(orig,orig+axis*10000.0)
            if index == -1: break
            count += 1
            orig = location + axis*0.00001
        if count%2 == 0:
            outside = True
            break
    return not outside

myPoint = fetchIfObject("Empty")
myMesh = fetchIfObject("Cube")
if myPoint != None:
    result = pointInsideMesh(myPoint.location,myMesh)
    print (result)
else:
    print ("myPoint does not exist.")
