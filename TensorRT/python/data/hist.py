import matplotlib
matplotlib.use('Agg') # No display

import os
import matplotlib.pyplot as plt
import numpy as np

runTimes = []   # Bar chart data
avgTimes = []   # Time histogram data
invAvgTimes = []# Throughput histogram data
numFiles = 0    # Number of machines
numRuns = -1    # Number of events per machine

for f in os.listdir('.'):
    if os.path.isdir(f):
        continue
    if not ".dat" in f:
        continue

    numFiles += 1
    g = open(f, 'r')
    text = g.read().split('\n')
    g.close()
    runLines = text[5:-4]
    if numRuns == -1:
        numRuns = len(runLines)
        runTimes = [0] * numRuns
    else:
        assert numRuns == len(runLines)# Assert that every machine ran the same number of events
    
    thisTime = 0
    invThisTime = 0
    lineNum = 0
    for line in runLines:
        record = False
        recording = ""
        for i in range(len(line)):
            if record:
                recording += line[i]
            if i > 0 and line[i] == ' ' and line[i-1] == ':':
                record = True
            elif line[i] == ' ':
                record = False
        runTimes[lineNum] += float(recording) / 1000 # Units of milliseconds
        thisTime += float(recording) / 1000 # Units of ms
        invThisTime += 1000 * 1000 / float(recording) # Units of s^-1
        lineNum += 1

    avgTimes.append(thisTime / numRuns)
    invAvgTimes.append(invThisTime / numRuns)

for i in range(len(runTimes)):
    runTimes[i] /= numFiles

y_pos = np.arange(numRuns)
plt.bar(y_pos, runTimes, align="center", alpha=0.75)

labels = [str(i) for i in range(numRuns)]

plt.xticks(y_pos, labels)
plt.xlabel("Run number")
plt.ylabel('Time (ms)')
plt.title('Time of each event, averaged over all machines')

plt.show()
plt.savefig("event-times.png")
plt.close()

plt.hist(avgTimes, 40, alpha=0.75)
plt.xlabel("Time (ms)")
plt.ylabel("Frequency")
plt.title("Histogram of average server times for each client")

plt.show()
plt.savefig("client-time-hist.png")
plt.close()

plt.hist(invAvgTimes, 20, alpha=0.75)
plt.xlabel("Throughput (s^-1)")
plt.ylabel("Frequency")
plt.title("Histogram of average throughput for each client")
plt.show()
plt.savefig("throughput-hist.png")


