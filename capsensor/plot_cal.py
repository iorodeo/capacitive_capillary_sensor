import sys
import scipy
import matplotlib.pylab as pylab

motor_cal = (2.34/100.0)*(5.0/55.0)
#sensor_cal = (2.0*4.096)/(2.0**24.0)

pos_list = []
val_list = []

# Load and plot data sets
for filename in sys.argv[1:]:
    print 'loading: ', filename

    data = scipy.loadtxt(filename)
    pos = motor_cal*data[:,0]
    val = data[:,1]
    pos = pos - pos[0]
    val = val - val[0]
    pos = pos[1:]
    val = val[1:]
    pos_list.extend(list(pos))
    val_list.extend(list(val))

    pylab.plot(pos, val,'ro')
    pylab.ylabel('capacitance change (pF)')
    pylab.xlabel('volume change (uL)')
    pylab.xlim(-0.05,pos.max()+0.05)
    pylab.grid('on')

    # Fit data
    fit = scipy.polyfit(pos,val,1)
    pos_fit = scipy.linspace(min(pos), max(pos), 500)
    val_fit = scipy.polyval(fit, pos_fit)
    pylab.plot(pos_fit, val_fit, 'k')

pylab.show()
