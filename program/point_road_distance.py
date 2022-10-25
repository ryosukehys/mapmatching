import os

import pandas as pd
import numpy as np
from geopy.distance import geodesic
import statistics

dayss =  [[str(i) for i in range(20210901, 20210931)],[str(i) for i in range(20211001, 20211031)] , [str(i) for i in range(20211201, 20211231)],[str(i) for i in range(20220101, 20220131)]]

which_going = "Wakkanai"
bus_type = "bus_A"
mesh_srt = 6641660100
mesh_end = 6641660199
min_m = 5
os.makedirs("C:/Users/hysir/Desktop/研究室/matching/distance_data/"+str(mesh_srt)+"_"+bus_type, exist_ok=True)
for days in dayss:
    month = days[1][0:6]
    for day in days:
        try:
            matched = pd.read_csv("C:/Users/hysir/Desktop/研究室/matching/matched_data/"+month+"_"+bus_type+"_"+which_going+"/"+day+"_"+bus_type+"_.csv")
            pre = pd.read_csv("C:/Users/hysir/Desktop/研究室/matching/matched_data/"+month+"_"+bus_type+"_"+which_going+"/premesh"+day+"_"+bus_type+"_mesh.csv")

            distance = []
            print(pre)
            print(matched)
            print([pre.iat[1,1], pre.iat[1,2]])
            print([matched.iat[1, 1], matched.iat[1, 2]])

            for i in range(len(pre)):
                if pre["meshcode"].iloc[i] < mesh_end and pre["meshcode"].iloc[i] > mesh_srt:
                    preplace = [pre["latitude"].iloc[i], pre["longitude"].iloc[i]]
                    x = 20
                    for t in range(len(matched)):
                        try:
                            matplace = [matched["latitude"].iloc[t], matched["longitude"].iloc[t]]
                            dis = geodesic(preplace, matplace).m
                            if dis < x :
                                x = dis
                        except Exception as e:
                            print(e)
                    print(x,"m")
                    if x < min_m:
                        print([x, preplace[0], preplace[1]])
                        distance.append([x, preplace[0], preplace[1]])
            #mean = statistics.mean(distance[:][0])
            #print(mean)
            df = pd.DataFrame(distance, columns=["distance", "latitude", "longitude"])
            df.to_csv("C:/Users/hysir/Desktop/研究室/matching/distance_data/"+str(mesh_srt)+"_"+bus_type+"/distance"+day+"_"+str(mesh_srt)+"_"+bus_type+".csv")
            print("finish")
        except Exception as e:
            print(e)

print("finish")