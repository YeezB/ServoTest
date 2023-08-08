import microbit
import math

freq = 50
init = 0
class DFdriver:
    def __init__(self):
        global init
        self.I2C = microbit.i2c
        self.I2C.init(freq=100000,sda=pin20,scl=pin19)
        if not init:
            self.i2cW(0x00, 0x00)
            self.freq(freq)
            init = 1

    def i2cW(self, reg, value):
        buf = bytearray(2)
        buf[0] = reg
        buf[1] = value
        self.I2C.write(0x40,buf)

    def i2cR(self, reg):
        buf = bytearray(1)
        buf[0] = reg
        self.I2C.write(0x40,buf)
        return self.I2C.read(0x40,1)

    def freq(self, freq):
        pre = math.floor(((25000000/4096/(freq * 0.915))-1) + 0.5)
        oldmode = self.i2cR(0x00)
        self.i2cW(0x00, (oldmode[0] & 0x7F) | 0x10)
        self.i2cW(0xFE, pre)
        self.i2cW(0x00, oldmode[0])
        sleep(5)
        self.i2cW(0x00, oldmode[0] | 0xa1)

    def pwm(self, channel, on, off):
        if ((channel < 0) or (channel > 15)):
            return
        buf = bytearray(5)
        buf[0] = 0x06 + 4 * channel
        buf[1] = on & 0xff
        buf[2] = (on >> 8) & 0xff
        buf[3] = off & 0xff
        buf[4] = (off >> 8) & 0xff
        self.I2C.write(0x40,buf)

class DFServo:
    def __init__(self, Ser):
        self._ser = 9 - Ser
        self._dri = DFdriver()

    def angle(self, deg):
        if(deg>160):
            deg = 160
        v_us = (deg * 10 + 600)
        value = math.floor(v_us * 4095 / (1000000 / freq))
        self._dri.pwm(self._ser + 7, 0, value)


