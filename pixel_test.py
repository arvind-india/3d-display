# Testing the python PIL library
#
# Bereket Abraham

import sys
sys.path.append("C:/Python32/Lib/site-packages")
import numpy
print(dir(numpy))

import sys
is_64bits = sys.maxsize > 2**32


from PIL import Image
i = Image.open(r'C:\Users\Bereket\Documents\BlenderModels\test1.png')
pixels = i.load() # this is not a list, nor is it list()'able
width, height = i.size
pixels
all_pixels = []
for x in range(width):
    for y in range(height):
        cpixel = pixels[x, y]
        all_pixels.append(cpixel)



from PIL import Image, _imaging
imgb = Image.new('RGB', (5,5))
for x in range(5):
	for y in range(5):
		imgb.putpixel((x, y), (255, 64, 64))


imgb.save(r'C:\Users\Bereket\Documents\BlenderModels\test2.png', 'PNG')


####


img = bpy.data.images.new(name='test1', width=5, height=5)
colors = []
for i in range(25):
	colors.append(255/256)
	colors.append(64/256)
	colors.append(64/256)
	colors.append(1.0)

img.pixels = colors
img.filepath = r'C:\Users\Bereket\Documents\BlenderModels\test1.png'
img.file_format = 'PNG'
# img.color_mode = 'RGB'
img.save_render(img.filepath, scene=None)



img = bpy.data.images.load(r'C:\Users\Bereket\Documents\BlenderModels\test2.png')
img.pixels
