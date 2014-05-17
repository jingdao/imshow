#!/usr/bin/python
#
#	Python script to display images on the console 
#	using terminal escape sequences
#
#	Usage: python imshow.py <image-file>
#
from PIL import Image
import sys
import os
import subprocess
try:
	im=Image.open(sys.argv[1])
except (IOError, IndexError):
	print('invalid image file specified')
	sys.exit(1)

proc=subprocess.Popen(['tput','lines'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
height=int(proc.communicate(None)[0])-1
proc=subprocess.Popen(['tput','cols'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
width=int(proc.communicate(None)[0])
imSampled=im.resize((width,height),Image.ANTIALIAS)
if not imSampled.mode=='RGBA':
	imSampled=imSampled.convert('RGBA')
pixmap=imSampled.getdata()
sys.stdout.write('\033[2J\033[1;1H')
numChar=0
row=1
for pixel in pixmap:
	r=pixel[0]*6/256
	g=pixel[1]*6/256
	b=pixel[2]*6/256
	alpha=pixel[3]
	combined=16+36*r+6*g+b
	if alpha==0:
		sys.stdout.write('\033[49m ')
	else:
		sys.stdout.write('\033[48;5;'+str(combined)+'m ')
	numChar+=1
	if numChar==width:
		row+=1
		sys.stdout.write('\033['+str(row)+';1H')
		numChar=0
sys.stdout.write('\033['+str(height+1)+';1H')
sys.stdout.write('\033[0m')	

