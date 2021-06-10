import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

addressLines = [18, 15, 14, 16, 12, 1, 7, 8, 25, 24, 23] # Address pins
IO = [4, 17, 27, 22, 10, 20, 2, 3] # Data IO pins
OE = 11 # Output Enable pin
WE = 21 # Write Enable pin
GPIO.setup(addressLines, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(OE, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(WE, GPIO.OUT, initial=GPIO.HIGH)


def setAddress(address):
    format = '{0:011b}'.format(address)
    temp = str(format)

    i = 0
    for bit in temp:
        if(int(bit) == 1):
            GPIO.output(addressLines[i], GPIO.HIGH)
            i += 1
        if(int(bit) == 0):
            GPIO.output(addressLines[i], GPIO.LOW)
            i += 1
    time.sleep(0.05)

def readEEPROM(address):
    setAddress(address)
    GPIO.setup(IO, GPIO.IN)
    GPIO.output(OE, GPIO.LOW)
    time.sleep(0.05)
    data = ""
    for dataPin in IO:
        if GPIO.input(dataPin):
            data = data + '1'
            # print("1", end="")
        if GPIO.input(dataPin) == 0:
            data = data + '0'
            # print("0", end="")
    print(hex(int(data, 2)) + ' ', end="")


def writeEEPROM(address, data):
    GPIO.output(OE, GPIO.HIGH)
    GPIO.setup(IO, GPIO.OUT, initial=GPIO.LOW)
    setAddress(address)
    format = '{0:08b}'.format(data)
    temp = str(format)

    i = 0
    for bit in temp:
        if(int(bit) == 1):
            GPIO.output(IO[i], GPIO.HIGH)
            i += 1
        if(int(bit) == 0):
            GPIO.output(IO[i], GPIO.LOW)
            i += 1
    GPIO.output(WE, GPIO.LOW)
    time.sleep(0.005)
    GPIO.output(WE, GPIO.HIGH)


# DECIMAL values to be programmed into memory locations. 
# These are 16 arbitary values, but array can be configured to any data the user wants to load into the EEPROM
program = [126, 48, 109, 121, 51, 91, 95,
           112, 127, 123, 119, 31, 78, 61, 79, 71]

# CLEAR MEM 0-255
for addr in range(0, 256):
    writeEEPROM(addr, 0)

# Arbitrary wait time that seemed to fix certain bugs due to signal timing.
time.sleep(2)

# Write EEPROM with data for first 16 address spaces
for prog in range(0, 16):
    writeEEPROM(prog, program[prog])


# Arbitrary wait time that seemed to fix certain bugs due to signal timing.
# Can be set to any value, but 10 seconds seemed safe
time.sleep(10)

# READ MEM 0-255
for x in range(0, 256, 16):
    for y in range(0, 16, 1):
        readEEPROM(x + y)
    print("\n")

# Can be uncommented for final GPIO cleanup, but I have found this to cause bugs (perhaps due to unpredictable write signalling)
# GPIO.cleanup()
