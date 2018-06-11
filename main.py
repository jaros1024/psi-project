import os

import numpy as np

from lib.converters import *
import lib.image_processing
import lib.processors as proc
import lib.plotters as plot
import os.path as op
import pandas


sample_root='2018-afcai-spring'
output_root='2018-asia-winter'

NAPS_VALIDATION_DATA = pandas.read_csv('NAPS_valence_arousal_2014.csv',sep=';', names=['ID', 'Category','Nr', 'V_H',
                                                                              'Description', 'Valence' ,'Arousal'])

# processing of single person
def process_person(path):
    print(path)

    sensors = next(os.walk(path))[1]
    if not os.path.exists(path + "/output"):
        os.makedirs(path + "/output")

    lib.image_processing.process_image_file(path)

    if "BITalino" in sensors:
        microvolt_to_beats(__get_file_name(path + "/BITalino", "BPM"), path + "/output/BPM.csv")
        diff_values(__get_file_name(path + "/BITalino","GSR"), path + "/output/GSR.csv")
    else:
        if "Empatica" in sensors and "eHealth" in sensors:
            nanowatt_to_beats(__get_file_name(path + "/Empatica", "BVP"), path + "/output/BPM.csv")
            ohm_to_microsiemens(__get_file_name(path + "/eHealth", "GSR"), path + "/output/GSR.csv")
        elif "Empatica" in sensors:
            nanowatt_to_beats(__get_file_name(path + "/Empatica", "BVP"), path + "/output/BPM.csv")
            sec_to_millisec(__get_file_name(path + "/Empatica", "GSR"), path + "/output/GSR.csv", sep=";")
        elif "eHealth" in sensors:
            diff_values(__get_file_name(path + "/eHealth", "BPM"), path + "/output/BPM.csv")
            ohm_to_microsiemens(__get_file_name(path + "/eHealth", "GSR"), path + "/output/GSR.csv")
    print()


# returns correct file name: BPM.csv or BPM_p.csv (or GSR)
def __get_file_name(path, sensor):
    if sensor == "BPM":
        if os.path.isfile(path + "/BPM.csv"):
            return path + "/BPM.csv"
        elif os.path.isfile(path + "/BPM_p.csv"):
            return path + "/BPM_p.csv"
    elif sensor == "GSR":
        if os.path.isfile(path + "/GSR.csv"):
            return path + "/GSR.csv"
        elif os.path.isfile(path + "/GSR_p.csv"):
            return path + "/GSR_p.csv"
    elif sensor == "BVP":
        if os.path.isfile(path + "/BVP.csv"):
            return path + "/BVP.csv"
        elif os.path.isfile(path + "/BVP_p.csv"):
            return path + "/BVP_p.csv"


def convert_data(root_path):
    dirs = next(os.walk(root_path))[1]
    for directory in dirs:
        process_person(op.join(root_path, directory))
        break


if __name__ == '__main__':
    #assuming that data is in same folder
    convert_data(sample_root)
    proc.gather_info()
    # data = proc.extract_data_for_single_image(sample_root + '/B303')
    # plot.plot_all_in_dict(data)