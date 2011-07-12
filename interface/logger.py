"""
Implements a simple data logger for saving data from a group of sensors.  

Will Dickson IO Rodeo Inc.
"""
class Logger(object):

    def __init__(self,filename,sensorLabels = (0,2)):
        self.filename = filename
        self.sensorLabels = sensorLabels 
        self.dataLists = {} 
        for val in sensorLabels:
            self.dataLists[val] = []
        self.saveCount = 0
        self.fid = open(self.filename, 'w')

    def close(self):
        self.fid.close()

    def addData(self,num, data):
        """
        Add data to logger
        """
        self.dataLists[num].append(data)

    def printLengths(self):
        """
        Print lengths of all data lists
        """
        print self.getLengths()

    def getLengths(self):
        return [len(self.dataLists[k]) for k in self.dataLists] 

    def write(self):
        """
        Write data to file
        """
        lengths = self.getLengths() 
        minLength = min(lengths)
        for i in range(0,minLength):
            # Get data to save
            saveData = {}
            for k, dataList in self.dataLists.iteritems():
                saveData[k] = dataList[0]
            # Check that save count matches, if so remove and save otherwise leave in queue
            self.saveCount += 1
            for k, data in saveData.iteritems():
                if data['count'] == self.saveCount:
                    self.dataLists[k].pop(0)
                    self.fid.write('%d %d %f '%(data['count'], data['time'], data['value']))
                elif data['count'] > self.saveCount:
                    self.fid.write('%d NaN NaN '%(self.saveCount,))
                else:
                    raise RuntimeError, 'data[count] < self.saveCount'
            self.fid.write('\n')

    def writeRemaining(self):
        """
        Write all data to file. This function should be used when the trials have
        been completed and is to flush any remaining data to file.
        """
        lengths = self.getLengths()
        maxLength = max(lengths)
        for i in range(0,maxLength):
            saveData = {}
            for k, dataList in self.dataLists.iteritems():
                if dataList:
                    saveData[k] = dataList[0]
                else:
                    saveData[k] = None
            self.saveCount += 1
            for k, data in saveData.iteritems():
                if data is not None :
                    if data['count'] == self.saveCount:
                        self.dataLists[k].pop(0)
                        self.fid.write('%d %d %f '%(data['count'], data['time'], data['value']))
                    else:
                        self.fid.write('%d NaN NaN '%(self.saveCount,))
                else:
                    self.fid.write('%d NaN NaN '%(self.saveCount,))
            self.fid.write('\n')



