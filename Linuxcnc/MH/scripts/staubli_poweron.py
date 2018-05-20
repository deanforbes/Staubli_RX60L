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
	while not retval=="." and not retval=="?" :
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
writeconsolecommand("ENABLE POWER")
waitconsoleready();
time.sleep(10.0)
writeconsolecommand("DO SPEED 10 ALWAYS")
waitconsoleready();
time.sleep(0.25)
writeconsolecommand("DO READY")
waitconsoleready();
time.sleep(0.25)
waitconsolefinished()

vplusconsole.close()
f.close()


