import os
import pandas
import datetime


# converts datetime of images of given person to timestamps
def process_image_file(path):
    input_file = __get_input_csv(path)
    output_file = path + "/output/images.csv"

    image_data = pandas.read_csv(input_file, sep=",", names=["Image", "Timestamp"], skiprows=6)

    results = []
    for i in image_data.values:
        try:
            results.append((i[0], __str_to_timestamp(i[1])))
        except ValueError as e:
            print('skipped a value (image conversion) {}'.format(e))

    __save_to_file(output_file, results)


def __get_input_csv(path):
    files = next(os.walk(path))[2]
    for i in files:
        if i.endswith(".csv"):
            return path+"/"+i


def __str_to_timestamp(string):
    return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S.%f").timestamp()*1000


def __save_to_file(path, values):
    with open(path, "w+") as file:
        for i in values:
            file.write(f"{i[0]}, {int(i[1])}\n")

