import serial
import time

ser = serial.Serial('COM4', 9600)

ser.write('AT+CMGF=0\r')
time.sleep(0.1)
A = ser.read(16)
print(A)

ser.write('07919732929090F001000B919732141077F900080012041F04400438043204350442002100210021' + '\x1a')
time.sleep(0.1)
ans = ser.read(200)
print(ans)
