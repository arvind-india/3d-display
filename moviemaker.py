### OpenCV, moviemaker	
#	
#	author: Bereket Abraham
#	3D Volumetric Display Project
#	required: Python 2.7, 32-bit, OpenCV for python
#

#!/usr/bin/python
import cv

dirc = "C:/Users/Bereket/Documents/BlenderModels/run2/"
#dirc = ""
#cv.LoadImage('picture.png', cv.CV_LOAD_IMAGE_COLOR)

im0 = cv.LoadImage(dirc+"image0.png")
if not im0:
    print "Could not load im0"
im1 = cv.LoadImage(dirc+"image1.png")
if not im1:
    print "Could not load im1"
im2 = cv.LoadImage(dirc+"image2.png")
if not im2:
    print "Could not load im2"
im3 = cv.LoadImage(dirc+"image3.png")
if not im3:
    print "Could not load im3"
im4 = cv.LoadImage(dirc+"image4.png")
if not im4:
    print "Could not load im4"
im5 = cv.LoadImage(dirc+"image5.png")
if not im5:
    print "Could not load im5"


fps = 60.0
frame_size = cv.GetSize(im0)
#codec = CV_FOURCC('D', 'I', 'V', 'X')
codec = 0
writer = cv.CreateVideoWriter(dirc+"run_final.avi", codec, fps, frame_size, True)
if not writer:
    print "Error in creating video writer"
    sys.exit(1)
else:
	for i in range(200):
		cv.WriteFrame(writer, im0)
		cv.WriteFrame(writer, im1)
		cv.WriteFrame(writer, im2)
		cv.WriteFrame(writer, im3)
		cv.WriteFrame(writer, im4)
		cv.WriteFrame(writer, im5)

#cv.ReleaseVideoWriter(writer)
