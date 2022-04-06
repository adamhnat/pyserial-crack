from sys import stdin
from time import sleep
import serial
import itertools
import string
import argparse


def main():
    all_args = argparse.ArgumentParser(prog='pyserialcrack',usage='%(prog)s [options]',description='python serial port password cracker')
    all_args.add_argument("-d","--device",required=True,help="Device ex. /dev/ttyUSB0")
    all_args.add_argument("-b", "--baudrate", required=False, default=115200, help="Port baudrate")
    all_args.add_argument("-t", "--timeout", required=False, default=5, help="Port communication timeout")
    all_args.add_argument('-v', '--verbose', action='count', default=0, required=False, help="increase output verbosity")
    all_args.add_argument('-x', '--bruteforce', required=False, help="bruteforce crack - specify length of pwd")
    all_args.add_argument('-w', '--wordlist', required=False, help="path to wordlist file")
    all_args.add_argument('-z', '--stdin', required=False, action='count', help="get password from stdin ex. crunch")
    
    args = all_args.parse_args()

    def vprint(obj):
        if args.verbose:
            print(obj,end='')
        return

    ser = serial.Serial(port=args.device, baudrate=args.baudrate, timeout=args.timeout)

    def testPassword(pwd:str):
        ser.flush()
        testpwd = ''.join(possible_password)+'\r\n'
        ser.write(bytes(testpwd,'ascii'))
        vprint("\r testing password: " + ''.join(possible_password))
        output = ser.read_until(b'### Please input boot password:###\r\n')
        if(output[-36:] != b'### Please input boot password:###\r\n'):
            print("PASSWORD: " + possible_password)
            return 1
        return 0


    input("Power on router and press enter")

    ser.read_until(b'*** Press 1 means entering boot mode***\r\n')
    ser.flush()
    ser.write(b'1')

    sleep(5)
    #loop for pwd guess
    if(args.bruteforce):
        for possible_password in itertools.product(string.ascii_letters, repeat=args.bruteforce): 
            if ( testPassword(possible_password) ==1 ):
                break
    elif(args.wordlist): #not tested
        for possible_password in open(args.wordlist,'r'):
            if ( testPassword(possible_password) ==1 ):
                break
    elif(args.stdin): 
        for possible_password in stdin:
            if ( testPassword(possible_password) ==1 ):
                break

if __name__ == '__main__':
    main()
