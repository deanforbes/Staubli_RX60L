#!/usr/bin/python
# ------------------------ upload --------------------

import time
import serial
import sys

f=open("streamserver.pg","r")
vplusconsole = serial.Serial(port='/dev/ttyS0', baudrate=38400, timeout=1,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)

d=f.readlines()

def waitconsoleready() :
	retval=vplusconsole.read()
	sys.stdout.write(retval)
	while not retval=="." and not retval=="?" and not retval=="*"  :
		retval=vplusconsole.read()
		sys.stdout.write(retval)
	retval=vplusconsole.readline()
	sys.stdout.write("REC : "+retval)

def waitconsolefinished() :
	retval=vplusconsole.read()
	sys.stdout.write(retval)
	while not retval=="." :
		retval=vplusconsole.read()
		sys.stdout.write(retval)
	retval=vplusconsole.readline()
	sys.stdout.write("REC : "+retval)

def writeconsolecommand(command) :
	vplusconsole.write(command)
	vplusconsole.write("\r\n")

vplusconsole.write("\r\n")
time.sleep(0.25)
writeconsolecommand("ABORT")
waitconsoleready();
time.sleep(0.25)
writeconsolecommand("Y")
waitconsoleready();
time.sleep(0.25)
writeconsolecommand("KILL")
waitconsoleready();
time.sleep(0.25)
writeconsolecommand("DELETE streamserver")
waitconsoleready();
time.sleep(0.25)
writeconsolecommand("Y")
waitconsoleready();
time.sleep(0.25)
writeconsolecommand("EDIT streamserver")
waitconsoleready();

for currentline in d:
	print(currentline)
	writeconsolecommand(currentline)
	waitconsoleready();
	#time.sleep(0.05)

writeconsolecommand("E")
waitconsoleready()

time.sleep(1.0)

writeconsolecommand("exec streamserver")

waitconsolefinished()

vplusconsole.close()
f.close()


