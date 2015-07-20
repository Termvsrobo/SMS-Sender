Python 2.7.8 (default, Jun 30 2014, 16:03:49) [MSC v.1500 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> import serial
>>> import time
>>> ser = serial.Serial('COM4', 112500)
>>> ser.write('AT\r')
3L
>>> ser.read(128)
'AT\r\r\nOK\r\n'
>>> ser.write('AT+CMGF=0\r')
10L
>>> ser.read(128)
'AT+CMGF=0\r\r\nOK\r\n'
>>> ser.write('AT+CMGS=32\r')
11L
>>> ser.read(256)
'AT+CMGS=32\r\r\n> '
>>> ser.write('07919732929090F011000B919732141077F90008AA12041F04400438043204350442002100210021\x1a')
81L
>>> ser.read(256)
'07919732929090F011000B919732141077F90008AA12041F04400438043204350442002100210021\x1a\r\n+CMGS: 81\r\n\r\nOK\r\n'
>>> 
