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



################################################################################
# Generate Day Plot
################################################################################
to_range_limit=len(open_time)
min_close_time=60*5

print("Generate Day Plot data")
sum_open_plot=np.linspace(0,0,num=60*60*24)
sum_open_plot_x=np.linspace(60*60*24,0,num=60*60*24)
sum_open_plot_label=[]

print("Generate Day Plot labels")
for timestamp in sum_open_plot_x:
    sum_open_plot_label.append( datetime.fromtimestamp(int(round(timestamp))) )

def set_range(start, stop, state, space_width):
    for i in range(start, stop):
        second=i%space_width
        sum_open_plot[second]+=1

x_open_start=None
x_open_stop=None
print("Generate plot")
for i in range(0,to_range_limit-2):
    if (open_time[i+1]-open_time[i]) < min_close_time and x_open_start == None:
        x_open_start=open_time[i]
    elif x_open_start != None and (open_time[i+1]-open_time[i]) >=min_close_time and (open_time[i+2]-open_time[i]) >= min_close_time*1.49:
        x_open_stop=open_time[i]
        set_range(x_open_start, x_open_stop, 1, (60*60*24))
        x_open_start=None

print("Filter data")
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

sum_open_plot2=smooth(sum_open_plot,1200)
plt.plot_date(sum_open_plot_label,sum_open_plot,'r-')
plt.plot_date(sum_open_plot_label,sum_open_plot2,'b-')
plt.show()
