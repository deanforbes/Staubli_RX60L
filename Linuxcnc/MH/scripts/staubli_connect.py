#!/usr/bin/python
import linuxcnc
import time
import serial
import sys
import math
import numpy

# ------------------------ STREAMING -------------------

dummyrun=False

if not dummyrun:
    vplusconsole = serial.Serial(port='/dev/ttyS2', baudrate=38400, timeout=1,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)

def waitconsoleready() :
	retval=vplusconsole.read()
	sys.stdout.write(retval)
	while not retval=="." and not retval=="?" and not retval=="K" and not retval=="\r":
		retval=vplusconsole.read()
		sys.stdout.write(retval)
	retval=vplusconsole.readline()
	sys.stdout.write("REC : "+retval)

def writeconsolecommand(command) :
	vplusconsole.write(command)
	#vplusconsole.write("\r\n")

s = linuxcnc.stat()

n=0

ms = time.time()*1000.

x=0
y=0
z=0

while (True):
    s.poll()
    currentpos = s.position
    currentfeed = s.current_vel
    currentoffset=s.g5x_offset

    spd=currentfeed
    lastx=x
    lasty=y
    lastz=z
    print currentpos
    x=-currentpos[1]+500.0
    y=currentpos[0]+50.0
    z=currentpos[2]+150.0
    a=currentpos[3]
    print(x,y,z)
    dx=x-lastx
    dy=y-lasty
    dz=z-lastz
    dist=math.sqrt(dx*dx+dy*dy+dz*dz)
    poscommand="1 %.2f %.2f %.2f %.2f" % (spd,x,y,z)
    sys.stdout.write(poscommand+" t")
    if not dummyrun:
        writeconsolecommand(poscommand+"\r\n")
    lastms=ms
    ms = time.time()*1000.
    if dummyrun:
        time.sleep(0.1)
    sys.stdout.write(str(ms-lastms)+" d"+str(dist)+" v"+str(0.001*dist/(ms-lastms))+"\r\n")
    n=n+1
    if(n>10) :
      if not dummyrun:
          waitconsoleready()

    #time.sleep(0.1)
