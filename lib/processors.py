import csv
import pandas
import os
import numpy as np

sample_root='2018-afcai-spring'
output_root='2018-asia-winter'

def gather_info():
    cleanOutput()
    dirs = next(os.walk(sample_root))[1]
    for directory in dirs:
        current_dir = os.path.join(sample_root, directory)
        data =extract_data_for_single_image(current_dir)
        for image in data:
            handle_image(os.path.join(image,directory),data.get(image),image)
        break


def handle_image(path:str,data:tuple,im):
    image_file=os.path.join(output_root,path)+'.csv'
    image_dir=os.path.join(output_root,im)
    os.mkdir(image_dir)

    # Trzeba wyciagnac z daty wartosci i wpisac je do pliku

    with open(image_file,'a+',) as image_csv:
        writer=csv.writer(image_csv,delimiter=';', escapechar=' ', quotechar='', quoting=csv.QUOTE_NONE)

        image_csv.close()



def cleanOutput():
    for root, dirs, files in os.walk(output_root, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))









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
    bmp_data = pandas.read_csv(bmp_filepath, sep=',',dtype=my_dtype).values if os.path.isfile(bmp_filepath) else []
    gsr_data = pandas.read_csv(gsr_filepath, sep=',', dtype=my_dtype).values if os.path.isfile(gsr_filepath) else []
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

