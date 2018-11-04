from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import sys

f=open("states.tsv")
lines=f.readlines()
f.close()

open_time=[]

print("Read data")
for line in lines:
    line = line.split("\t")
    open_date = datetime.strptime(line[0], "%d/%b/%Y:%H:%M:%S %z")
    open_time.append(int(round(open_date.timestamp())))

open_time=np.array(open_time)

print("Create Output arrays")
time_diff = np.diff(open_time)

plot_list_open_y = np.linspace(5,5,num=int(round((open_time[-1] - open_time[0])/60)))
plot_list_lit_dt = np.linspace(4,4,num=int(round((open_time[-1] - open_time[0])/60)))
plot_list_lit_dt.fill(None)
plot_list_open_x = np.linspace(open_time[0],open_time[-1],num=int(round((open_time[-1] - open_time[0])/60)))
plot_list_open_x_label = []

print("Create X Labels")
for timestamp in plot_list_open_x:
    plot_list_open_x_label.append( datetime.fromtimestamp(int(round(timestamp))) )

def find_nearest_above(my_array, target):
    diff = my_array - target
    mask = np.ma.less_equal(diff, 0)
    # We need to mask the negative differences and zero
    # since we are looking for values above
    if np.all(mask):
        return None # returns None if target is greater than any value
    masked_diff = np.ma.masked_array(diff, mask)
    return masked_diff.argmin()

def set_array_space(from_timestamp, to_timestamp, set_to, array):
    i_from = find_nearest_above(plot_list_open_x, from_timestamp)
    i_to   = find_nearest_above(plot_list_open_x, to_timestamp)
    for i in range(i_from, i_to):
        array[i] = set_to

#to_range_limit=len(open_time)
to_range_limit=10000
print("Fill open array")
for i in range(0,to_range_limit-1):
    if (open_time[i+1]-open_time[i]) <= 40:
        set_array_space(open_time[i],open_time[i+1],4,plot_list_lit_dt)
    if (open_time[i+1]-open_time[i]) < 180:
        pass
    else:
        set_array_space(open_time[i],open_time[i+1],None,plot_list_open_y)
    sys.stdout.write("\r{}/{}".format(i,to_range_limit))

print("")

print("Create Plots")
plt.hold(False)
plt.plot_date(plot_list_open_x_label[0:to_range_limit],plot_list_lit_dt[0:to_range_limit],'x')
plt.hold(True)
plt.plot_date(plot_list_open_x_label[0:to_range_limit],plot_list_open_y[0:to_range_limit],'b-')
plt.show()
