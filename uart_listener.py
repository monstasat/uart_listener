#!/usr/bin/python3
import serial
import sys
import glob
import time
import argparse
import datetime

def do_command_line():
    # make a command line parser
    parser = argparse.ArgumentParser(description="Com port")
    parser.add_argument('-tx',help="tx com port to listen",required=True)
    parser.add_argument('-rx',help="rx com port to listen",required=True)
    # parse the command line stored in args,
    # but skip the first element (the filename)
    args = parser.parse_args()
    # call the main program do_activate() to start up the app
    return (args.tx,args.rx)

def do_port_setup(port,name,handler):
    print("Setting up", port, "port...")
    try:
        handler.baudrate = 115200
        handler.port     = port
        handler.parity   = serial.PARITY_NONE
        handler.bytesize = serial.EIGHTBITS
        handler.stopbits = serial.STOPBITS_ONE
        handler.xonxoff  = False
        handler.dsrdtr   = False
        handler.rtscts   = False
        handler.timeout  = 0
    except:
        print(sys.exc_info()[0], sys.exc_info()[1])
        print("error while settings {} port params, exiting".format(name))
        handler.close
        sys.exit()

def do_print_data(dir,data):
    data = "".join("%02x " % b for b in data)
    time = datetime.datetime.now().strftime("%H:%M:%S:%f")
    print("[{}] [{}]: {}\n".format(dir, time, data))

def serial_ports():
    ports = glob.glob('/dev/tty[A-Za-z]*')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass

    return result

running = False

tx,rx = do_command_line()

print("Available ports: ", serial_ports())

tx_handler = serial.Serial()
rx_handler = serial.Serial()

do_port_setup(tx,"TX", tx_handler)
do_port_setup(rx,"RX", rx_handler)

running = True

try: tx_handler.open()
except:
    print(sys.exc_info()[0], sys.exc_info()[1])
    print("failure opening TX port, exiting")
    sys.exit()
try: rx_handler.open()
except:
    print(sys.exc_info()[0], sys.exc_info()[1])
    print("failure opening RX port, exiting")
    sys.exit()

while running is True:
    time.sleep(0.5)
    tx_data = tx_handler.read(10000000)
    rx_data = rx_handler.read(10000000)
    if len(tx_data) > 0:
        do_print_data("TX",tx_data)
    if len(rx_data) > 0:
        do_print_data("RX",rx_data)

tx_handler.close()
rx_handler.close()
