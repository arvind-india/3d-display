# Tesing out the python interface ofr Blender, in order to automate workflows and extract data

import bpy.data

bpy.data.scenes[0].objects["Torus"].data.vertices[0].co.x
bpy.data.objects["Cube2"].data.vertices[0].co.z -= 2.0

# location variable holds a reference to the object too.
location = bpy.context.object.location
location *= 2.0

# Copying the value drops the reference so the value can be passed to
# functions and modified without unwanted side effects.
location = bpy.context.object.location.copy()



# run from cmd line
# blender --python /home/me/my_script.py
