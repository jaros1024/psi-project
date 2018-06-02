import pandas
import os
import numpy as np


def extract_data_for_single_image(path, time_range=10):
    """"
    functions assumes that data is converted and 'output' folder in given path exists
    :param path: path to single person folder
    :param time_range: time range which will be extracted in seconds
    :returns dictionary with picture names as keys and tuple of data arrays as data ([bpm],[gsr])"""
    output = {}
    inner_root_path = os.path.join(path,'output')
    bmp_filepath = os.path.join(inner_root_path, 'BPM.csv')
    gsr_filepath = os.path.join(inner_root_path, 'GSR.csv')
    images_path = os.path.join(inner_root_path, 'images.csv')

    images_data = pandas.read_csv(images_path, sep=',', header=None).values
    my_dtype = {'timestamp':np.uint64,'value': float}
    bmp_data = pandas.read_csv(bmp_filepath, sep=',',dtype=my_dtype).values
    gsr_data = pandas.read_csv(gsr_filepath, sep=',', dtype=my_dtype).values
    for index, image in enumerate(images_data):
        name = _get_filename(image[0])
        start_time = image[1]
        if index + 1 < len(images_data):
            next_start_time = images_data[index + 1][1]
        else:
            next_start_time = start_time + time_range*1000
        filtered_bpm = _find_data_in_range(bmp_data,start_time, time_range, next_start_time)
        filtered_gsr = _find_data_in_range(gsr_data,start_time, time_range, next_start_time)
        output[name] = (filtered_bpm, filtered_gsr)
    return output


def _get_filename(base_str:str) -> str:
    splited = base_str.split('\\')
    name = splited[-1]
    return name.split('.')[0]


def _find_data_in_range(raw_data: np.ndarray, start:int, range_: int, max_time:int) -> []:
    ns_range = range_ * 1000
    if start + ns_range > max_time:
        ns_range = max_time - start
        print('range too big, cutting to {}s'.format(ns_range/1000))
    found = [x for x in raw_data if 0 <= x[0] - start <= ns_range ]
    return found

