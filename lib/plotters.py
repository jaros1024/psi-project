import matplotlib.pyplot as ppl
import numpy as np

def plot_all_in_dict(dc):
    for k in dc.keys():
        plot_picture_data(dc,k)


def plot_picture_data(dict_, key):
    ppl.figure(1)
    bpm, gsr = dict_[key]
    x = np.asarray(bpm)[:,0]
    y = np.asarray(bpm)[:,1]
    ppl.plot(x,y)
    ppl.title('bpm')
    ppl.figure(2)
    x = np.asarray(gsr)[:, 0]
    y = np.asarray(gsr)[:, 1]
    ppl.plot(x, y)
    ppl.title('gsr')
    ppl.show()