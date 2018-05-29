import pandas
import math


def ohm_to_microsiemens(ohm):
    return (1/ohm)*1000000.0


def nanowatt_to_beats(input_file, output_file):
    heart = pandas.read_csv(input_file, sep=';', dtype={"timestamp": int, "value": float})

    results = []

    last_timestamp = 0
    last_value = 0
    last_bpm = 0
    rising = True

    for i in heart.values:
        if i[1] > -5:
            continue

        if last_timestamp == 0:
            last_timestamp = i[0]
            last_value = i[1]
        else:
            if last_value > i[1]:
                rising = False
            elif last_value < i[1]:
                if not rising:
                    bpm_value = __interval_to_bpm_sec(i[0] - last_timestamp)
                    if (math.fabs(bpm_value - last_bpm) <= 30 or last_bpm == 0) and (50 < bpm_value < 150):
                        results.append((round(i[0]*1000), bpm_value))
                    last_timestamp = i[0]
                rising = True

    __save_to_file(output_file, results)
    return


def microvolt_to_beats(input_file, output_file):
    heart = pandas.read_csv(input_file, sep=',', dtype={"timestamp": int, "value": float})

    results = []

    last_beat = 0
    is_beat = False
    for i in heart.values:
        if i[1] >= 800 and not is_beat:
            if last_beat != 0:
                bpm = __interval_to_bpm(i[0] - last_beat)
                if bpm < 200:
                    results.append((i[0], bpm))
            last_beat = i[0]
            is_beat = True
        if i[1] <= 800 and is_beat:
            is_beat = False

    __save_to_file(output_file, results)
    return


def __interval_to_bpm(interval):
    return 60000.0/interval


def __interval_to_bpm_sec(interval):
    return 60.0/interval


def __save_to_file(path, values):
    with open(path, "w+") as file:
        file.write("timestamp, value\n")
        for i in values:
            file.write(f"{i[0]}, {round(i[1], 2)}\n")
    return

