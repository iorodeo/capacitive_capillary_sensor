import math

class LowpassFilter(object):

    """
    Implements a simple lowpass filter.
    """
    def __init__(self, fc=1.0, state=0.0):
        self.fc = fc
        self.tc = 2.0*math.pi*self.fc
        
        self.state = state 

    def update(self,value,dt):
        alpha = dt/((1.0/self.tc) + dt)
        self.state = alpha*value + (1.0 - alpha)*self.state
        return self.state
