'''
This file just finds all the .dat files in the data directory and averages together their values,
printing the result and saving it to averages.txt. Run it with 

    python analyze.py
'''

import os


NUM_DATAPOINTS = 8

class ClientData:
    def __init__(self, text):
        lines = text.split('\n')
        self.outputTime = float(lines[1][13:-3])
        asyncLine = 2
        if lines[2] == "numRemoteTime was zero":
            self.remoteTime = 0
            self.remoteTimeReciprocal = 0
            asyncLine += 1
        else:
            raise Exception("Non-async remote times are not implemented")
            self.remoteTime = None
            self.remoteTimeReciprocal = None
            asyncLine += 2
        if lines[asyncLine] == "numAsyncRemoteTime was zero":
            self.asyncRemoteTime = 0
            self.asyncRemoteTimeReciprocal = 0
        else:
            self.asyncRemoteTime = float(lines[asyncLine][19:-2])
            self.asyncRemoteTimeReciprocal = float(lines[asyncLine+1][16:-5])
        self.inferencesReceived = int(lines[-4][21:])
        self.timeElapsed = float(lines[-3][14:-2])
        self.throughput = float(lines[-2][11:-11])

def main():
    clientDatas = []
    for f in os.listdir("."):
        if os.path.isfile(f) and f[-4:] == ".dat":
            g = open(f, 'r')
            text = g.read()
            g.close()
            clientDatas.append(ClientData(text))

    averages = [0]*NUM_DATAPOINTS
    for data in clientDatas:
        averages[0] += data.outputTime
        averages[1] += data.remoteTime
        averages[2] += data.remoteTimeReciprocal
        averages[3] += data.asyncRemoteTime
        averages[4] += data.asyncRemoteTimeReciprocal
        averages[5] += data.inferencesReceived
        averages[6] += data.timeElapsed
        averages[7] += data.throughput

    for i in range(NUM_DATAPOINTS):
        averages[i] /= len(clientDatas)

    out = "Output time: " + str(averages[0]) + " us\nRemote time: " + str(averages[1]) + " us\n\tRemote time reciprocal: " + str(averages[2]) + \
            " s^-1\nAsync remote time: " + str(averages[3]) + \
            " us\n\tAsync remote time reciprocal: " + str(averages[4]) + " s^-1\nInferences received: " + str(averages[5]) + "\nTime elapsed: " + \
            str(averages[6]) + " s\nThroughput (disregard): " + str(averages[7]) + " s^-1"
    f = open("averaged.txt", 'w')
    f.write(out)
    f.close()

    print(out)



if __name__ == "__main__":
    main()
