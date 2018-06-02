import pandas
from statistics import mean


# converts values in input_file from ohm to microseconds and saves them to output_file
def ohm_to_microsiemens(input_file, output_file, unit="millisec", sep=","):
    skin_data = pandas.read_csv(input_file, sep=sep, dtype={"value": float})
    if len(skin_data.values) == 0:
        return

    result = []
    for i in skin_data.values:
        timestamp = i[0]
        if unit == "sec":
            timestamp *= 1000
        result.append((timestamp, __ohm_to_microsiemens_value(i[1])))

    result = __values_to_diffs(result)

    __save_to_file(output_file, result)


# converts single value in ohm to microsiemens
def __ohm_to_microsiemens_value(ohm):
    return (1/ohm)*1000000.0


# converts values in input_file from nanowatt to bpm and saves them to output_file
def nanowatt_to_beats(input_file, output_file):
    heart = pandas.read_csv(input_file, sep=';', dtype={"timestamp": float}, error_bad_lines=False, warn_bad_lines=False)

    extremes = __get_local_extremes(heart.values)
    diastolic_points = __get_diastolic_points(extremes)
    bpm = __dialistic_points_to_beats(diastolic_points)
    bpm = __values_to_diffs(bpm)

    __save_to_file(output_file, bpm)


# converts values in input_file from microvolt to bpm and saves them to output_file
def microvolt_to_beats(input_file, output_file):
    heart = pandas.read_csv(input_file, sep=',', dtype={"value": float})

    results = []

    last_beat = 0
    is_beat = False
    for i in heart.values:
        if i[1] >= 650 and not is_beat:
            if last_beat != 0:
                bpm = __interval_to_bpm(i[0] - last_beat)
                if 50 < bpm < 150:
                    results.append((i[0], round(bpm, 2)))
            last_beat = i[0]
            is_beat = True
        if i[1] <= 650 and is_beat:
            is_beat = False

    results = __values_to_diffs(results)

    __save_to_file(output_file, results)


# converts timestamps in input_file from seconds to milliseconds and saves them to output_file
def sec_to_millisec(input_file, output_file, sep=",", mean=False):
    heart = pandas.read_csv(input_file, sep=sep, dtype={"value": float})
    result = []

    for i in heart.values:
        result.append((i[0]*1000, i[1]))

    if mean:
        result = __values_to_diffs(result)

    __save_to_file(output_file, result)


def diff_values(input_file, output_file, sep=","):
    heart = pandas.read_csv(input_file, sep=sep, dtype={"value": float})
    if len(heart.values) == 0:
        return

    result = __values_to_diffs(heart.values)
    __save_to_file(output_file, result)


# returns bpm basing on interval in milliseconds between heartbeat
def __interval_to_bpm(interval):
    return 60000.0/interval


# returns bpm basing on interval in seconds between heartbeat
def __interval_to_bpm_sec(interval):
    return 60.0/interval


# saves given list as csv file
def __save_to_file(path, values):
    with open(path, "w+") as file:
        file.write("timestamp, value\n")
        for i in values:
            file.write(f"{int(i[0])}, {i[1]}\n")


# finds all local extremes in given function
def __get_local_extremes(data):
    results = []

    for i in range(1, (len(data)-1)):
        # check for local minimum
        if data[i-1][1] > data[i][1] and data[i+1][1] > data[i][1]:
            results.append((data[i][0], data[i][1], "min"))
        if data[i - 1][1] < data[i][1] and data[i + 1][1] < data[i][1]:
            results.append((data[i][0], data[i][1], "max"))

    return results


# finds extremes that are diastolic points
def __get_diastolic_points(extremes):
    diastolic_points = []

    minima = []
    for i in extremes:
        if i[2] == "min":
            if i[1] < -2:
                minima.append(i)
        else:
            if i[1] > 0:
                point = __get_lowest_min(minima)
                if point is not None:
                    diastolic_points.append(point)
                minima.clear()

    return diastolic_points


# gets minimum that has the lowest value
def __get_lowest_min(minima):
    lowest = (0, 999)

    for i in minima:
        try:
            if i[1] < lowest[1]:
                lowest = (float(i[0]), i[1])
        except ValueError:
            continue

    if lowest[1] < 0:
        return lowest
    return None


# converts list of diastolic points to beats per minute
def __dialistic_points_to_beats(points):
    results = []
    for i in range(1, len(points)):
        try:
            bpm_value = __interval_to_bpm_sec(points[i][0]-points[i-1][0])
            if 50 < bpm_value < 130:
                results.append((round(points[i][0]*1000), round(bpm_value, 2)))
        except TypeError:
            continue

    return results


# converts list of (timestamp, value) to list of (timestamp, avg-value)
def __values_to_diffs(values: []):
    originals = []
    for i in values:
        originals.append(i[1])

    avg = mean(originals)
    results = []

    for i in values:
        results.append((i[0], round(i[1] - avg, 2)))

    return results
