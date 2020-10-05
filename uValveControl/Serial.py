'''
Created on 9 set 2020

@author: andrea
'''
import serial

ser = serial.Serial('/dev/ttyACM0',19200, timeout=1)
ser.write(b'\r')#ritorno carrello
ser.write('\x04'.encode())#modalita corretta rasmissione ctrl-d (ctrl-a = soh \x01
print('Presentazione.. ', ser.readlines())

while True:
    val = input('Inserisci Comando (e=exit) --> ')
    ser.write('test'.encode())
    print('Risp -> ',ser.readlines())
    if val=='e':
        ser.close()
        break
print('Fine')
