import pandas


def ohmToMicroSiemens(ohm):
    return (1/ohm)*1000000.0


def microvoltToBeats(inputFile, outputFile):
    heart = pandas.read_csv(inputFile, sep=',', dtype={"timestamp": int, "value": float})

    results = []

    lastBeat = 0
    isBeat = False
    for i in heart.values:
        if i[1] >= 800 and not isBeat:
            if lastBeat != 0:
                results.append((i[0], __intervalToBpm(i[0]-lastBeat)))
            lastBeat = i[0]
            isBeat = True
        if i[1] <= 800 and isBeat:
            isBeat = False

    __saveToFile(outputFile, results)
    return


def __intervalToBpm(interval):
    return 60000.0/interval


def __saveToFile(path, values):
    with open(path, "w+") as file:
        file.write("timestamp, value\n")
        for i in values:
            file.write(f"{i[0]}, {round(i[1], 2)}\n")
    return

