import GOL
import torch
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import random
import matplotlib.patches as mpatches
import imageio
import os
import sys
from itertools import repeat

n_means = 19
n_stds = 3
means = list(np.linspace(0.1, 1, n_means)) * n_means
standard_deviations = list(np.linspace(0.1, 0.3, n_stds))
stds = [x for item in standard_deviations for x in repeat(item, n_means)]
size = 500
figsize = 30
time = 500

mean = round(means[int(sys.argv[1]) - 1], 2)
std = round(stds[int(sys.argv[1]) - 1], 2)

savepath = 'Animation/' + str(round(mean, 2)) + '_' + str(round(std, 2))

conway = GOL.Conway(mean = mean, std = std, size = size, figsize = figsize, time = time, wrap = True)
conway.simulate()