import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

filename = ""

def clicked_btnquit():
    root.destroy

def dataimporter(filename,header=65):
    data = pd.read_csv(filename, header=header)
    nummer = data.to_numpy()
    nummerdata = np.asarray(nummer[:-1,:], dtype="float")
    return nummerdata

def plotter(ax,data,zo,colour,label):
    ax.plot(data[:,0],data[:,1],zorder=zo, lw = 4, color = colour, label =label)
    ax.fill_between(data[:,0],data[:,1],zorder=zo, color = colour)
   
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def data_integration(data,under=2.2,over=2.6,avgunder=2.65,avgover=2.8 ):
    array = np.array([])
    for i in (data):
        intunder = np.where(i[:,0]==find_nearest(i[:,0],under))
        intover = np.where(i[:,0]==find_nearest(i[:,0],over))
        placeunder = np.where(i[:,0]==find_nearest(i[:,0],avgunder))
        placeover = np.where(i[:,0]==find_nearest(i[:,0],avgover))
        
        intunder = np.reshape(intunder,-1)
        intover = np.reshape(intover,-1)
        placeunder = np.reshape(placeunder, -1)
        placeover = np.reshape(placeover, -1)

        i[:,1] = i[:,1]-np.average(i[placeunder[0]:placeover[0],1])

        top1 = np.sum(i[intunder[0]:intover[0],1])
        array = np.append(array,top1)
    return array

def predict(signal,c):
    return c[0]*signal + c[1]

def UploadAction(event=None):
    global filename
    filename = filedialog.askopenfilename()
    lbl.config(text=('Selected:'+filename))
    global data
    data = dataimporter(filename)
    thick = predict(data_integration([data]),np.array([0.0059018,1.92601479]))
    thickness.config(text=("Thickness: " + f"{thick[0]:.2f}" + "nm"))
    
Molines = [2.29316, 2.28985, 2.39481, 2.5183]
Silines = [1.73998,1.73938, 1.83594]
Slines = [2.30784,2.30664,2.46404]
Olines =[0.5249] 
Nticks = 20
xmax = 3
xmin = 0
ymax = 1000

fig, ax = plt.subplots()
fig.set_size_inches(12,6)
fmt = lambda x, pos: '{}'.format(x).rstrip('0')

plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right',fontsize=14)
plt.setp(ax.get_yticklabels(),fontsize=14)
ax.xaxis.set_major_locator(ticker.MaxNLocator(Nticks))
# ax.yaxis.set_major_locator(ticker.MaxNLocator(7))
#ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: str(x).rstrip('0')))
ax.grid(zorder = 1)
ax.set_xlim([xmin,xmax])
ax.set_ylim([0,ymax])
ax.set_facecolor((0.1, 0.5, 0.8))
ax.spines['bottom'].set_color('black')
ax.spines['top'].set_color('black')
ax.xaxis.label.set_color('black')
ax.tick_params(colors=(0.2, 0.2, 0.2), which ='both')
ax.set_xlabel("Energy (keV)",fontsize=14)
ax.set_ylabel("Count (cps/eV)",fontsize=14)
ax.set_title("EDS spectrum",fontsize=16)

ax.vlines(Silines,-1000,ymax, colors="red",linestyles="dashed", alpha = 0.7, label="Si K tops",zorder = 10)#Silicon K tops
ax.vlines(Molines,-1000,ymax, colors="black",linestyles="dashed",alpha = 0.7,label= "Mo L tops",zorder = 10)#Mo L tops
ax.vlines(Slines,-1000,ymax, colors=(0,0,1),linestyles="dashed",alpha = 0.7,label= "S L tops",zorder = 10)#S K tops
ax.vlines(Olines,-1000,ymax, colors=(0,0,1),linestyles="dashed",alpha = 0.7,label= "O L tops",zorder = 10)#S K tops
ax.legend(fontsize=14)



root = tk.Tk()



root.geometry("1000x1000")
root.title("Thickness calculator")
root.tk.call("tk","scaling",3.0)

lbl = tk.Label(root,text="Test")
lbl.pack()

thickness = tk.Label(root,text="Thickness")
thickness.pack()

# quitbutton = tk.Button(root, text="Quit", command = clicked_btnquit())
# quitbutton.pack()

# Create an "Import File" button
button = tk.Button(root, text='Open', command=UploadAction)
button.pack()

scatter = FigureCanvasTkAgg(fig, root)
scatter.get_tk_widget().pack() #fill='both', expand=True)

test = tk.Button(root,text="testbutton",command=print("test"))
test.pack()

#Figure test
def plottbutton():
    ax.cla()
    ax.xaxis.set_major_locator(ticker.MaxNLocator(Nticks))
    ax.grid(zorder = 1)
    ax.set_xlim([xmin,xmax])
    ax.set_ylim([0,ymax])
    ax.set_facecolor((0.1, 0.5, 0.8))
    ax.spines['bottom'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.xaxis.label.set_color('black')
    ax.tick_params(colors=(0.2, 0.2, 0.2), which ='both')
    ax.set_xlabel("Energy (keV)",fontsize=14)
    ax.set_ylabel("Count (cps/eV)",fontsize=14)
    ax.set_title("EDS spectrum",fontsize=16)

    ax.vlines(Silines,-1000,ymax, colors="red",linestyles="dashed", alpha = 0.7, label="Si K tops",zorder = 10)#Silicon K tops
    ax.vlines(Molines,-1000,ymax, colors="black",linestyles="dashed",alpha = 0.7,label= "Mo L tops",zorder = 10)#Mo L tops
    ax.vlines(Slines,-1000,ymax, colors=(0,0,1),linestyles="dashed",alpha = 0.7,label= "S L tops",zorder = 10)#S K tops
    ax.vlines(Olines,-1000,ymax, colors=(0,0,1),linestyles="dashed",alpha = 0.7,label= "O L tops",zorder = 10)#S K tops
    ax.legend(fontsize=14)
    plotter(ax,data,7,"yellow","")
    scatter.draw()
    
    
plott = tk.Button(root, text='Plott', command=plottbutton)
plott.pack()


root.mainloop() #Creates root and repsonds to input


