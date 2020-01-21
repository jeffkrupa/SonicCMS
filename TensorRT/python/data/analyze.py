import os


NUM_DATAPOINTS = 7
class ClientData:
    def __init__(self, text):
        lines = text.split('\n')
        asyncLine = 1
        if lines[1] == "numRemoteTime was zero":
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
        self.inferencesReceived = int(lines[4][21:])
        self.timeElapsed = float(lines[5][14:-2])
        self.throughput = float(lines[6][11:-11])

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
        averages[0] += data.remoteTime
        averages[1] += data.remoteTimeReciprocal
        averages[2] += data.asyncRemoteTime
        averages[3] += data.asyncRemoteTimeReciprocal
        averages[4] += data.inferencesReceived
        averages[5] += data.timeElapsed
        averages[6] += data.throughput

    for i in range(NUM_DATAPOINTS):
        averages[i] /= len(clientDatas)

    out = "Remote time: " + str(averages[0]) + " us\n\tRemote time reciprocal: " + str(averages[1]) + " s^-1\nAsync remote time: " + str(averages[2]) + \
            " us\n\tAsync remote time reciprocal: " + str(averages[3]) + " s^-1\nInferences received: " + str(averages[4]) + "\nTime elapsed: " + \
            str(averages[5]) + " s\nThroughput (disregard): " + str(averages[6]) + " s^-1"
    f = open("averaged.txt", 'w')
    f.write(out)
    f.close()

    print(out)



if __name__ == "__main__":
    main()
