"""
sensor.py

A simple serial interface to the capillary capacitance sensors. 
"""
import serial
import time

SENSORCAL = (2.0*4.096)/(2.0**24.0)

class SensorComm(serial.Serial):

    def __init__(self, port='/dev/ttyUSB1', timeout=0.1):
        super(SensorComm,self).__init__(port=port,timeout=timeout)
        self.open()
        time.sleep(2.0)    # Wait for serial reset
        self.emptyBuffer() # Throw out any garabage in the buffer
        self.sensorCal = SENSORCAL

    def emptyBuffer(self):
        while self.inWaiting() > 0:
            line = self.readline()

    def readData(self):
        """
        Read data buffer and convert to python dictionary
        """
        data = None
        if self.inWaiting() > 0:
            line = self.readline()
            try:
                data = eval(line[:-2])
                if data['type'] == 'sensor':
                    data['value'] = self.sensorCal*data['value']
            except:
                # Possibly garbled - throw it away
                pass
        return data


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    """
    Test sensor and logger classes
    """
    sensor = SensorComm()
    logger = Logger('log.txt')
    timeStop = time.time() + 30.0
    while time.time() < timeStop:
        data = sensor.readData()
        if data is not None:
            try:
                logger.addData(data['number'],data)
                logger.printLengths()
            except KeyError:
                pass
            time.sleep(0.01)
        logger.write()

    logger.writeRemaining()


