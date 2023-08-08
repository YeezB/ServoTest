from microbit import *
import DFServo

S8 = DFServo(8)

while True:
    S8.angle(45)
    sleep(1000)
    S8.angle(145)
    sleep(1000)