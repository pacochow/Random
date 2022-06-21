import torch
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import random
import matplotlib.patches as mpatches
import imageio
import os
from itertools import repeat

class Conway(object):
    def __init__(self, mean, std, size, figsize, time, wrap):
        self.mean = mean
        self.std = std
        self.size = size
        self.figsize = figsize
        self.time = time
        self.wrap = wrap
        
    def init_box(self):
        self.box = torch.round(torch.normal(self.mean, self.std, size = (self.size, self.size)))
        for i in range(self.size):
            for j in range(self.size):
                self.box[i][j] = self.classify_life(self.box[i][j])
        
    def find_neighbor_index(self, index1, index2, box):
        
        limit = self.size - 1
        neighbors = []
        
        if self.wrap == False:


            if index1 == 0 and index2 == 0:
                neighbors.extend([(index1+1, index2), (index1+1, index2+1), (index1, index2+1)])
            elif index1 == 0 and index2 != 0 and index2!= limit:
                neighbors.extend([
                    (index1, index2 - 1), (index1+1, index2-1), (index1+1, index2), (index1+1, index2+1), (index1, index2+1)])
            elif index1 == 0 and index2 == limit:
                neighbors.extend([(index1, index2-1), (index1+1, index2-1), (index1+1, index2)])
            elif index1 != 0 and index1!= limit and index2 == 0:
                neighbors.extend([
                    (index1-1, index2), (index1-1, index2+1), (index1, index2+1), (index1+1, index2+1), (index1+1, index2)])
            elif index1 != 0 and index1!= limit and index2 == limit:
                neighbors.extend([
                    (index1-1, index2), (index1-1, index2-1), (index1, index2-1), (index1+1, index2-1), (index1+1, index2)])
            elif index1 == limit and index2 == 0:
                neighbors.extend([(index1-1, index2), (index1-1, index2+1), (index1, index2+1)])
            elif index1 == limit and index2 != 0 and index2!= limit:
                neighbors.extend([(index1, index2-1), (index1-1, index2-1), (index1-1, index2), (index1-1, index2+1), (index1, index2+1)])
            elif index1 == limit and index2 == limit:
                neighbors.extend([(index1, index2-1), (index1-1, index2-1), (index1-1, index2)])
            else:
                neighbors.extend([
                    (index1-1, index2-1), (index1-1, index2), (index1-1, index2+1), (index1, index2+1), 
                    (index1+1, index2+1), (index1+1, index2), (index1+1, index2-1), (index1, index2-1)])
        
        else:
            wrap = np.linspace(0, limit, self.size)
            neighbors.extend([
                (int(wrap[(index1-1)%self.size]), int(wrap[(index2-1)%self.size])), 
                (int(wrap[(index1-1)%self.size]), index2), 
                (int(wrap[(index1-1)%self.size]), int(wrap[(index2+1)%self.size])),
                (index1, int(wrap[(index2+1)%self.size])), 
                (int(wrap[(index1+1)%self.size]), int(wrap[(index2+1)%self.size])), 
                (int(wrap[(index1+1)%self.size]), index2), 
                (int(wrap[(index1+1)%self.size]), int(wrap[(index2-1)%self.size])), 
                (index1, int(wrap[(index2-1)%self.size]))
            ])
            

        return neighbors

    def classify_life(self, x):
        values = [0, 1]
        if np.abs(x - values[0]) >= np.abs(x - values[1]):
            return values[1]
        else:
            return values[0]
    
    def calculate_life(self, index1, index2, box):
        neighbors = self.find_neighbor_index(index1, index2, box)
        counter = 0
        for n in neighbors:
            if box[n[0], n[1]] == 1:
                counter += 1
        return counter

    def compute(self, box):
        initial = box.clone()
        self.movement = 0
        for i in range(self.size):
            for j in range(self.size):
                life = self.calculate_life(i, j, initial)
                if initial[i, j] == 0 and life == 3: 
                    box[i, j] = 1
                    self.movement += 1
                elif initial[i, j] == 1 and life < 2 or initial[i, j] == 1 and life > 3:
                    box[i, j] = 0
                    self.movement += 1
                    

    def run(self, box):
        for t in range(self.time):
            self.compute(box)


    def build(self, box):
        savepath = str(round(self.mean, 2)) + '_' + str(round(self.std, 2))
        for t in tqdm(range(self.time)):
            plt.figure(figsize = [self.figsize, self.figsize])
            plt.axis('off')
            im = plt.imshow(box, cmap = 'Greens')
            plt.savefig('Animation/' + savepath + '/time_' + str(t) + '.png')
            plt.close()
            self.compute(box)


        files = ['Animation/' + savepath + '/time_' + str(t) + '.png' for t in range(self.time)]
        
        # Build gif
        
        
        with imageio.get_writer('Animation/' + savepath + '/' + savepath + '.gif', mode='I', fps = 8) as writer:
            for filename in files:
                image = imageio.imread(filename)
                writer.append_data(image)

#         Remove files
        for filename in set(files):
            os.remove(filename)

    def simulate(self):
        self.init_box()
        self.build(self.box)
            


