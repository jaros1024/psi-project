import os
from shutil import copyfile
from lib.converters import *
import lib.image_processing

# processing of single person
def processPerson(path):
    print(path)

    sensors = next(os.walk(path))[1]
    if not os.path.exists(path + "/output"):
        os.makedirs(path + "/output")

    lib.image_processing.process_image_file(path)

    if "BITalino" in sensors:
        microvolt_to_beats(__get_file_name(path + "/BITalino", "BPM"), path + "/output/BPM.csv")
        copyfile(path + "/BITalino/GSR.csv", path + "/output/GSR.csv")
    else:
        if "Empatica" in sensors and "eHealth" in sensors:
            nanowatt_to_beats(__get_file_name(path + "/Empatica", "BVP"), path + "/output/BPM.csv")
            ohm_to_microsiemens(__get_file_name(path + "/eHealth", "GSR"), path + "/output/GSR.csv")
        elif "Empatica" in sensors:
            nanowatt_to_beats(__get_file_name(path + "/Empatica", "BVP"), path + "/output/BPM.csv")
            sec_to_millisec(__get_file_name(path + "/Empatica", "GSR"), path + "/output/GSR.csv", sep=";")
        elif "eHealth" in sensors:
            copyfile(__get_file_name(path + "/eHealth", "BPM"), path + "/output/BPM.csv")
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



#assuming that data is in same folder
rootPath = '2018-afcai-spring'

dirs = next(os.walk(rootPath))[1]

for directory in dirs:
    processPerson(rootPath+"/"+directory)

