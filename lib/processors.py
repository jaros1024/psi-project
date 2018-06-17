import pandas
import os
import numpy as np

SAMPLE_ROOT = '2018-afcai-spring'
NAPS_VALIDATION_DATA = pandas.read_csv('NAPS_valence_arousal_2014.csv', sep=';', names=['ID', 'Category', 'Nr', 'V_H',
                                                                                        'Description', 'Valence',
                                                                                        'Arousal'])
def merge_bpm_and_csr(d_root):
    """"
    loads all processed data to pandas.DataFrame
    :returns pandas DataFrame with  columns [bpm. gsr ,valence ,arousal]
    """
    final_list = pandas.DataFrame(columns=['bpm', 'gsr', 'valence', 'arousal'])
    dirs = next(os.walk(d_root))[1]
    for directory in dirs:
        current_dir = os.path.join(d_root, directory)
        data = extract_data_for_single_image(current_dir, keep_timestamp=False)
        for name in data.keys():
            bpm, gsr = data[name]
            valence, arousal = _find_v_a(NAPS_VALIDATION_DATA, name)
            final_list = final_list.append({'bpm': bpm, 'gsr': gsr, 'valence': valence, 'arousal': arousal},
                                           ignore_index=True)
    return final_list


def extract_data_for_single_image(path, time_range=10, keep_timestamp=True):
    """"
    functions assumes that data is converted and 'output' folder in given path exists
    :param path: path to single person folder
    :param time_range: time range which will be extracted in seconds
    :param keep_timestamp: optional swtich to return data lists with or without timestamp
    :returns dictionary with picture names as keys and tuple of data arrays as data ([bpm],[gsr])"""
    output = {}
    inner_root_path = os.path.join(path, 'output')
    bmp_filepath = os.path.join(inner_root_path, 'BPM.csv')
    gsr_filepath = os.path.join(inner_root_path, 'GSR.csv')
    images_path = os.path.join(inner_root_path, 'images.csv')

    images_data = pandas.read_csv(images_path, sep=',', header=None).values
    my_dtype = {'timestamp': np.uint64, 'value': float}
    bmp_data = pandas.read_csv(bmp_filepath, sep=',', dtype=my_dtype).values if os.path.isfile(bmp_filepath) else []
    gsr_data = pandas.read_csv(gsr_filepath, sep=',', dtype=my_dtype).values if os.path.isfile(gsr_filepath) else []
    for index, image in enumerate(images_data):
        name = _get_filename(image[0])
        start_time = image[1] + 5000 # timeshift 500 ms
        if index + 1 < len(images_data):
            next_start_time = images_data[index + 1][1]
        else:
            next_start_time = start_time + time_range * 1000
        filtered_bpm = _find_data_in_range(bmp_data, start_time, time_range, next_start_time, not keep_timestamp)
        filtered_gsr = _find_data_in_range(gsr_data, start_time, time_range, next_start_time, not keep_timestamp)
        output[name] = (filtered_bpm, filtered_gsr)
    return output


def _get_filename(base_str: str) -> str:
    """
    parses out filename from path
    :param base_str: string with unix like path and filename at the end
    :return: name of the file
    """
    splited = base_str.split('\\')
    name = splited[-1]
    return name.split('.')[0]


def _find_data_in_range(raw_data: np.ndarray, start: int, range_: int, max_time: int, skip_timestamp=False) -> []:
    """
    finds bpm or gsr data from given time renge, startgin from cleset following record  from when picture was shown
    through given range or to start of new timestamp when  next picture was shown
    :param raw_data: raw data to search
    :param start: picture show time
    :param range_: range to exctract
    :param max_time: max possible range
    :param skip_timestamp: optional if given data without timestamp is returned
    :return:  list of exctracred data with timstamps
    """
    ns_range = range_ * 1000
    if start + ns_range > max_time:
        ns_range = max_time - start
        print('range too big, cutting to {}s'.format(ns_range / 1000))
    found = [x[1] for x in raw_data if 0 <= x[0] - start <= ns_range] if skip_timestamp else \
        [x for x in raw_data if 0 <= x[0] - start <= ns_range]
    return found



def _find_v_a(pandas_df, name):
    """"
    finds valence and arousal by name of picture
    :param pandas_df: pandas DataFrame created from NAPS file
    :param name: name of the picture
    :returns two flaots representing found valnce and arousal
    """
    row = pandas_df.loc[pandas_df['ID'] == name]
    return _str_with_comma_to_float(row['Valence'].values[0]), \
           _str_with_comma_to_float(row['Arousal'].values[0])


def _str_with_comma_to_float(data: str) -> float:
    return float(data.replace(',', '.'))
