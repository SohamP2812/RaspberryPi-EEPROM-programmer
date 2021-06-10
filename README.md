# RaspberryPi-EEPROM-programmer
Simple EEPROM programmer for the Raspberry Pi. Uses the GPIO pins to communicate with EEPROM. \
Assumes 11 address lines and 8 data lines - but this can be configured however the user wants. \
Data is programmed in DECIMAL format, however certain tweaking by the user can easily adjust this to be programmed with binary/hex format. \
Wait times used through time.sleep() are intended to fulfill read/write timing requirements for the EEPROM chip being programmed. The specific timing properties in the script work with the 'AT28C16' EEPROM chip. The user must adjust the code to fulfill the requirements of the chip they are programming. This information can be easily found on the chips datasheet.

Enjoy!
