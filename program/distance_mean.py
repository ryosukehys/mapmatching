import os

import scipy.stats
import numpy as np
import pandas as pd
import statistics

dayss = [[str(i) for i in range(20210901, 20210931)],[str(i) for i in range(20211001, 20211031)],[str(i) for i in range(20211101, 20211131)], [str(i) for i in range(20211201, 20211231)], [str(i) for i in range(20220101, 20220131)]]
#dayss = [[str(i) for i in range(20211101, 20211131)]]
which_going = "Wakkanai"
mesh_srt = 6542402100
#mesh_end = 6741169999
bus_type = "bus_B"
statistics_list_mon = []
os.makedirs("C:/Users/hysir/Desktop/研究室/matching/distance_data/"+str(mesh_srt)+"_"+bus_type, exist_ok=True)


which_going = "Wakkanai"
bus_type = "bus_B"
mesh_srt = 6542402100
mesh_end = 6542402199
min_m = 20
mesh = pd.read_csv("C:\\Users\hysir\Desktop\研究室\kyosaku_work\mesh_all.csv")
mesh_list = list(mesh["meshcode"])
for mesh in ["66412522"]:
    try:
        mesh = str(mesh)[0:8]

        mesh_srt = int(mesh + "00")
        mesh_end = int(mesh + "99")
        min_m = 20

        for days in dayss:
            statistics_list = []
            month = days[1][0:6]
            for day in days:
                try:
                    df = pd.read_csv("C:/Users/hysir/Desktop/研究室/matching/distance_data/"+str(mesh_srt)+"_"+bus_type+"_"+which_going+"/distance"+day+"_"+str(mesh_srt)+"_"+bus_type+"_"+which_going+".csv")
                    distance = df["distance"]
                    #mean = statistics.mean(distance)
                    #stdev = statistics.pstdev(distance)
                    distance = np.array(distance)
                    mean = scipy.stats.trim_mean(distance, 0.2) #トリム平均使う
                    stdev = statistics.pstdev(list(scipy.stats.trimboth(distance, 0.2)))
                    data_num = len(list(scipy.stats.trimboth(distance, 0.2)))
                    statistics_list.append([day, mean, stdev, data_num])
                    statistics_list_mon.append([day, mean, stdev, data_num])
                except Exception as e:
                    print(e)
            save = pd.DataFrame(statistics_list, columns=["day", "mean", "stdev", "num of data"])
            save.to_csv(
                "C:/Users/hysir/Desktop/研究室/matching/distance_data/"+str(mesh_srt)+"_"+bus_type+"_"+which_going+ "/statistics_" + month + "_" + str(
                    mesh_srt) + "_"+bus_type+".csv")
        save_month = pd.DataFrame(statistics_list_mon, columns=["day", "mean", "stdev", "num of data"])
        save_month.to_csv(
                "C:/Users/hysir/Desktop/研究室/matching/distance_data/"+str(mesh_srt)+"_"+bus_type+"_"+which_going+ "/statistics_" + str(
                    mesh_srt) + "_"+bus_type+".csv")
        print("finish", str(mesh_srt))
    except Exception as e: print(e, "final")