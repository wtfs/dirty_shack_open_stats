from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pickle

f=open("data.bin",'rb')
data=pickle.load(f)
f.close()
open_time=data[0]
plot_list_open_x=data[1]
plot_list_open_x_label=data[2]

print("Create Output arrays")
time_diff = np.diff(open_time)

plot_y_zero = np.linspace(0,0,num=int(round((open_time[-1] - open_time[0]))))


print("Generate plot data")
to_range_limit=len(open_time)
#to_range_limit=10000
plt.plot_date(plot_list_open_x_label[0:1],plot_y_zero[0:1],'-')

x_open_start=None
x_open_stop=None
door_changes=0
min_close_time=60*5
for i in range(0,to_range_limit-2):
    if (open_time[i+1]-open_time[i]) < min_close_time and x_open_start == None:
        x_open_start=open_time[i]
    elif x_open_start != None and (open_time[i+1]-open_time[i]) >=min_close_time and (open_time[i+2]-open_time[i]) >= min_close_time*1.49:
        x_open_stop=open_time[i]
        plt.axvspan(
                datetime.fromtimestamp(int(round(x_open_start))),
                datetime.fromtimestamp(int(round(x_open_stop))),
                facecolor='#2ca02c', alpha=0.5)
        x_open_start=None
        door_changes += 1

print("The door changed {} times its state".format(door_changes))
plt.show()
