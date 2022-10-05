from serial import Serial
s = Serial(port='/dev/cu.usbmodem11101', baudrate=9600)

s.flushInput()

while True:
    try:
        ser_bytes = s.readline()
        print(ser_bytes)
    except Exception as e:
        print(e)
        print("Keyboard Interrupt")
        break