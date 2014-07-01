import bpy
# delete all of the grid boxess\

def clearGrid():

    for obj in bpy.data.objects:
    	if 'grid' in obj.name:
    		bpy.data.objects[obj.name].select = True
    	else:
    		bpy.data.objects[obj.name].select = False
    
    bpy.ops.object.delete()
    
