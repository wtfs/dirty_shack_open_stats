from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pickle

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

print("Create X Labels")
plot_list_open_x = np.linspace(open_time[0],open_time[-1],num=int(round((open_time[-1] - open_time[0])/60)))
plot_list_open_x_label = []
for timestamp in plot_list_open_x:
    plot_list_open_x_label.append( datetime.fromtimestamp(int(round(timestamp))) )


print("Save data")
f=open("data.bin",'wb')
pickle.dump([open_time, plot_list_open_x, plot_list_open_x_label],f)

f.close()


