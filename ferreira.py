%matplotlib notebook
import traceback
import math
import scipy.stats as s
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])

class Ferreira(object):
    def __init__(self, df, y = 0):
        self.df = df
        y=int(y)
        index = [1992,1993,1994,1995]
        labels = ['1992','1993','1994','1995']
        std=df.std(axis=1)
        avg=df.mean(axis=1)
        yerr=std/np.sqrt(df.shape[1]*s.t.ppf(0.95,df.shape[1])-1)
        cmap = cm.coolwarm
        cpick = cm.ScalarMappable(cmap=cmap)
        cpick.set_array([])
        perconversion = []
        for a, b in zip(avg, std):
            h = a + b
            l = a - b
            per = (h - y) / (h - l)
            per = 1 if per > 1 else 0
            perconversion.append(per)
        colors = cpick.to_rgba(perconversion)
        self.fig = plt.figure('Feirreira Functional',figsize=(8,8))
        self.ax = self.fig.add_subplot(111)
        self.bars = self.ax.bar(
            index, avg, yerr=yerr,capsize=20, picker = 5, color=colors, tick_label=labels)
        plt.title('Ferreira et al, 2014')
        plt.xlabel('Year')
        plt.ylabel('Y-Values')
        self.text = self.ax.text(1995.5, y, 'y = %d' %y, bbox=dict(fc='white',ec='k'), position = (1995.5,y), wrap = False)
        self.text.set_text('y = %d' %y);
        self.text.set_position((1995.5, y));
        self.line = self.line = self.ax.axhline(y=y, color='k', linestyle='--')
        self.line.set_ydata(y)
        self.fig.canvas.mpl_connect('pick_event', self.onpick)
    
    def onpick(self, event):
        y = event.mouseevent.ydata

        try:
            self.line.set_ydata(y)
            self.text.set_text('y = %d' %y);
            self.text.set_position((1995.5, y));
        except:
            print('something went wrong :(')
            plt.close()

        recalc = s.ttest_1samp(df.transpose(), y)
        cw = cm.coolwarm
        cchng = cw(1 / (1 +  np.exp(recalc.statistic)))
        
        for bar, col in zip(self.bars, cchng):
            bar.set_color(col)
            
        self.fig.canvas.draw()
while True:    
    try:
        num = input("Enter Initial y (between 0 and 48000): ")
        f = Ferreira(df, y = num)
        if 0 <= int(num) <= 48000:
            break
        raise ValueError()
    except ValueError:
        print("Input must be an integer between 0 and 48000.")
        plt.close()