# coding=utf-8
__author__ = 'Termvsrobo'
"""
Описание модуля или функции для документирования
"""

import serial
import time

ser = serial.Serial('COM4', 115200)
ser.write('AT+CMGF=0\r')
time.sleep(0.001)
buf = ser.read(16)
if len(buf)>0:
	ans = buf.split('\r\n')[1]
	print('ans = %s' % ans)