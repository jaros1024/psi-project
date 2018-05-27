import pandas
import math


def ohmToMicroSiemens(ohm):
    return (1/ohm)*1000000.0


def nanowattToBeats(inputFile, outputFile):
    heart = pandas.read_csv(inputFile, sep=';', dtype={"timestamp": int, "value": float})

    results = []

    lastTimestamp = 0
    lastValue = 0
    lastBpm = 0
    rising = True

    for i in heart.values:
        if i[1] > -5:
            continue

        if lastTimestamp == 0:
            lastTimestamp = i[0]
            lastValue = i[1]
        else:
            if lastValue > i[1]:
                rising = False
            elif lastValue < i[1]:
                if not rising:
                    bpmValue = __intervalToBpmSec(i[0]-lastTimestamp)
                    if (math.fabs(bpmValue - lastBpm) <= 30 or lastBpm == 0) and (50 < bpmValue < 150):
                        results.append((round(i[0]*1000), bpmValue))
                    lastTimestamp = i[0]
                rising = True

    __saveToFile(outputFile, results)
    return


def microvoltToBeats(inputFile, outputFile):
    heart = pandas.read_csv(inputFile, sep=',', dtype={"timestamp": int, "value": float})

    results = []

    lastBeat = 0
    isBeat = False
    for i in heart.values:
        if i[1] >= 800 and not isBeat:
            if lastBeat != 0:
                bpm = __intervalToBpm(i[0]-lastBeat)
                if bpm < 200:
                    results.append((i[0], bpm))
            lastBeat = i[0]
            isBeat = True
        if i[1] <= 800 and isBeat:
            isBeat = False

    __saveToFile(outputFile, results)
    return


def __intervalToBpm(interval):
    return 60000.0/interval

def __intervalToBpmSec(interval):
    return 60.0/interval


def __saveToFile(path, values):
    with open(path, "w+") as file:
        file.write("timestamp, value\n")
        for i in values:
            file.write(f"{i[0]}, {round(i[1], 2)}\n")
    return

