from time import sleep
import serial
import io
import itertools
import string

ser = serial.Serial(port='/dev/ttyFAKE0', baudrate=115200,timeout=5)

#todo: wait for serial to enter 1
input("Power on router and press enter")

#while(True):
#    currentline = ser.readline()
#    if (currentline == b'*** Press 1 means entering boot mode***\r\n'):
#        ser.flush()
#        ser.write(b'1')
#        break
ser.read_until(b'*** Press 1 means entering boot mode***\r\n')
ser.flush()
ser.write(b'1')

sleep(5)
#loop for pwd guess
for possible_password in itertools.product(string.ascii_letters, repeat=3): 
    #print(possible_password)
    ser.flush()
    testpwd = ''.join(possible_password)+'\r\n'
    ser.write(bytes(testpwd,'ascii'))
    print("testing password: " + testpwd)
    #output=ser.read_all()
    output = ser.read_until(b'### Please input boot password:###\r\n')
    if(output[-36:] != b'### Please input boot password:###\r\n'):
        print("PASSWORD: " + possible_password)
        break


