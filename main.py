import sys
import struct
import serial
import glob
import time
import numpy as np

# V1.0.0-alpha

# perfomance improvements : try to understand why a non connected device is increasing CPU needs to 50%

class Serial:
    """ 

    Send pixels data to an arduino via serial port 

    COMMANDS
    00
    Displays the frame currently in the buffer
    Replies: 00

    02
    Setup led strip length
    Replies: nothing

    01 n1 n2 b1 g1 r1 b2 g2 r2 ... bn gn rn
    Reads n pixels into the frame buffer
    Replies: nothing

    FF
    Clears the display and terminates the animation
    Replies: nothing

    """

    def __init__(self, verbose=False, desirated_framerate=0.016, number_of_pixels=30, port="", baud_rate=1000000):
        self.serial_port = port
        self.serial_class = None
        self.desirated_framerate = desirated_framerate
        self.trying_to_connect = False
        self.is_connected = False
        self.clear_command = b'\xff'
        self.show_command = b'\x00'
        self.send_number_of_pixel_command = b'\x02'
        self.send_data_command = b'\x01'
        self._number_of_pixels = number_of_pixels
        self.number_of_pixel_command = (
            self._number_of_pixels).to_bytes(2, byteorder="big")
        self.pixels = np.tile(.0, (3, number_of_pixels))
        self.raw_data = []
        self.baud_rate = baud_rate
        self.verbose = verbose

        self.gamma_table = [
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
            1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
            2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
            5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
            10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
            17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
            25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
            37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
            51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
            69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
            90, 92, 93, 95, 96, 98, 99, 101, 102, 104, 105, 107, 109, 110, 112, 114,
            115, 117, 119, 120, 122, 124, 126, 127, 129, 131, 133, 135, 137, 138, 140, 142,
            144, 146, 148, 150, 152, 154, 156, 158, 160, 162, 164, 167, 169, 171, 173, 175,
            177, 180, 182, 184, 186, 189, 191, 193, 196, 198, 200, 203, 205, 208, 210, 213,
            215, 218, 220, 223, 225, 228, 231, 233, 236, 239, 241, 244, 247, 249, 252, 255]

        self.setup()

    @staticmethod
    def tryPort(port_name):
        """ Try the availabilty of a given port and if it's not available, return a list of available ones """
        try:
            s = serial.Serial(port_name)
            s.close()
        except (OSError, serial.SerialException):
            print(
                "Serial port not found or busy, please check your config file -> ", port_name)
            print("Here's the ports available ->",
                  Serial.listAvailablePortsName())
            quit()

    @staticmethod
    def listAvailablePortsName():
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            # this excluses all ttys that are not tagged usbserial like arduinos
            ports = glob.glob('/dev/tty.*usbserial*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    @staticmethod
    def printDeviceList():
        """ Print available devices """
        print('Serial ports available :')

        ports = Serial.listAvailablePortsName()
        for port in ports:
            print("- '" + port + "'")

    @staticmethod
    def testDevice(name):
        """ Test a given device """
        Serial.tryPort(name)

        number_of_pixels = 40
        serialOutputs = []

        pixels = np.tile(1, (3, number_of_pixels))
        pixels *= 125
        pixels[0, 0] = 255  # Set 1st pixel red
        pixels[1, 1] = 255  # Set 2nd pixel green
        pixels[2, 2] = 255  # Set 3rd pixel blue

        start_time = time.time()

        serialClass = Serial(True, 0.016, number_of_pixels, name)
        print("Testing serial device -> ", name)

        while True:
            pixels = np.roll(pixels, 1, axis=1)
            serialClass.update(pixels)
            current_time = time.time()
            if(serialClass.isOnline()):
                message = "Device online"
                message += " since " + \
                    str(int(current_time - start_time)) + "s"
            else:
                message = "Device offline"
                start_time = time.time()

            print(message)
            time.sleep(.016)

    def isOnline(self):
        """ Return if device is online or not """
        return self.is_connected

    def setup(self):
        """ Setup """

        try:
            self.serial_class = serial.Serial(
                self.serial_port, self.baud_rate, timeout=1, bytesize=serial.EIGHTBITS)
        except IOError:
            self.is_connected = False
            if(self.verbose):
                print(
                    "Hey it seem's that your cable is not plugged on port ", self.serial_port)
            time.sleep(5)
            return

        self.serial_class.setDTR(False)
        time.sleep(1)
        self.serial_class.flushInput()
        self.serial_class.setDTR(True)
        if(self.verbose):
            print("Setup begin for %s" % self.serial_port)
        while True:
            message = self.serial_class.readline()
            if("Setup ok" in str(message)):
                break
        if(self.verbose):
            print("Setup finished")
        while (message != self.show_command):
            message = self.serial_class.read(1)
        if(self.verbose):
            print("Begin transmision...")

    def getVector(self, array, col):
        """ Get R G B Vector from multi dimensional array """
        vector = []
        imax = len(array)
        for i in range(imax):
            vector.append(array[i][col])
        return vector

    def getRawPixels(self, array):
        """ Transform pixels into the right data set

            input: [
                [r, ... * n_pixels],
                [g, ... * n_pixels],
                [b, ... * n_pixels]
            ]
            output: [
                [r, g, b, ... * n_pixels],
            ]
         """
        self.raw_data = []
        array = np.clip(array, 0, 255).astype(int)
        for i in range(self._number_of_pixels):
            self.raw_data += self.getVector(array, i)

    def applyGammaCorrection(self, pixels):
        """Apply led gamma correction
           Function to review, not very pythonic"""
        new_pixels = np.clip(pixels, 0, 255).astype(int)
        for i in range(len(pixels[0])):
            new_pixels[0][i] = self.gamma_table[new_pixels[0][i]]
            new_pixels[1][i] = self.gamma_table[new_pixels[1][i]]
            new_pixels[2][i] = self.gamma_table[new_pixels[2][i]]
        return new_pixels

    def update(self, pixels):
        """ Send frame to arduino """
        self.pixels = np.tile(.0, (3, len(pixels[0])))
        self._number_of_pixels = len(pixels[0])
        self.pixels = self.applyGammaCorrection(pixels)
        if(not self.trying_to_connect and self.serial_class):
            try:
                self.serial_class.write(self.show_command)
                self.serial_class.read(1)
                number_of_pixel_command = self._number_of_pixels.to_bytes(
                    2, byteorder="big")
                self.getRawPixels(self.pixels)
                message = self.send_data_command[:1] + \
                    number_of_pixel_command[:2] + bytes(self.raw_data)
                self.serial_class.write(message)
                self.is_connected = True
            except IOError:
                # TO DO : Remove display and find a way to display if it's ONLINE or not
                #print("Hey it seem's that your cable has been unpluged on port ", self.serial_port)
                # print("except")
                self.trying_to_connect = True
                self.is_connected = False
                self.setup()
                self.trying_to_connect = False
                return


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--list", help="list available serial devices", action="store_true")
    parser.add_argument(
        "-t", "--test", help="test a given serial port", type=str)

    args = parser.parse_args()

    if(args.list):
        Serial.printDeviceList()

    if(args.test):
        Serial.testDevice(args.test)
