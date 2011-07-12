import serial
import time
import scipy
from sensor_comm import SensorComm

SERVO_DEV = '/dev/ttyUSB0'
SENSOR_DEV = '/dev/ttyUSB1'
ARDUINO_RESET_T = 2.0

class Servo(serial.Serial):

    def __init__(self,dev=SERVO_DEV,baudrate=9600): 
        super(Servo, self).__init__(dev,baudrate)
        self.open()
        time.sleep(ARDUINO_RESET_T)

    def setPosMicroseconds(self, val):
        cmdStr = '[%d]'%(val,)
        self.write(cmdStr)



# -----------------------------------------------------------------------------
if __name__ == '__main__':

    import scipy

    pos_top_us = 1000
    pos_start_us = 1400
    step_us = 50
    move_sleep_t = 8.0
    num_samples = 300 
    filename = 'step_data.txt'
    chan = 2

    servo = Servo()
    sensor = SensorComm(SENSOR_DEV)

    print "moving to top" 
    servo.setPosMicroseconds(pos_top_us)
    time.sleep(3.0)

    print "moving to start"
    servo.setPosMicroseconds(pos_start_us)
    time.sleep(5.0)
    print "starting calibration"
    print "-"*60


    with open(filename,'w') as f:
        for i in range(0,12):
            pos = pos_start_us + i*step_us
            servo.setPosMicroseconds(pos)
            time.sleep(move_sleep_t)
            sensor.emptyBuffer()
            data = sensor.readNumValues(num_samples,chan)
            data = scipy.array(data)
            print data.shape
            
            data_mean = data.mean()
            print 'Pos: %d, data: %f'%(pos,data_mean)
            f.write('%d %f\n'%(pos, data_mean))

    servo.setPosMicroseconds(pos_top_us)



