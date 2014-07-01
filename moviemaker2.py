### OpenCV, moviemaker	
#	
#	author: Bereket Abraham
#	3D Volumetric Display Project
#	required: Python 2.7, 32-bit, OpenCV for python
#

#!/usr/bin/python
import cv

#dirc = "C:/Users/Bereket/Documents/BlenderModels/run0/"
dirc = "C:/Users/Bereket/Documents/3D Display/test_runs/"
#cv.LoadImage('picture.png', cv.CV_LOAD_IMAGE_COLOR)
name = "test4"

im0 = cv.LoadImage(dirc+name+".png")
if not im0:
    print "Could not load im0"


fps = 60.0
frame_size = cv.GetSize(im0)
#codec = CV_FOURCC('D', 'I', 'V', 'X')
codec = 0
writer = cv.CreateVideoWriter(dirc+name+".avi", codec, fps, frame_size, True)
if not writer:
    print "Error in creating video writer"
    sys.exit(1)
else:
	for i in range(600):
		cv.WriteFrame(writer, im0)

#cv.ReleaseVideoWriter(writer)
