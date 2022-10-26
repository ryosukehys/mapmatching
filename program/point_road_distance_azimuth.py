import mesh_latlon_return

import os
import pandas as pd
import numpy as np
from geopy.distance import geodesic
import statistics

dayss =  [[str(i) for i in range(20210901, 20210931)],[str(i) for i in range(20211001, 20211031)] ,[str(i) for i in range(20211101, 20211131)], [str(i) for i in range(20211201, 20211231)],[str(i) for i in range(20220101, 20220131)]]
#dayss = [str(i) for i in range(20211101, 20211131)]
which_going = "Wakkanai"
bus_type = "bus_B"
mesh_srt = 6542402100
mesh_end = 6542402199
min_m = 20
mesh = pd.read_csv("C:\\Users\hysir\Desktop\研究室\kyosaku_work\mesh_all.csv")
mesh_list = list(mesh["meshcode"])
for mesh in [66412522]:
    try:
        mesh = str(mesh)[0:8]

        mesh_srt = int(mesh + "00")
        mesh_end = int(mesh + "99")
        min_m = 20
        for days in dayss:
            month = days[1][0:6]
            for day in days:

                try:
                    matched = pd.read_csv("C:/Users/hysir/Desktop/研究室/matching/matched_data/"+month+"_"+bus_type+"_"+which_going+"/"+day+"_"+bus_type+"_.csv")
                    pre = pd.read_csv("C:/Users/hysir/Desktop/研究室/matching/matched_data/"+month+"_"+bus_type+"_"+which_going+"/premesh"+day+"_"+bus_type+"_mesh.csv")

                    distance = []

                    for i in range(len(pre)):
                        if pre["meshcode"].iloc[i] <= mesh_end and pre["meshcode"].iloc[i] >= mesh_srt:
                            prelat, prelon = pre["latitude"].iloc[i], pre["longitude"].iloc[i]
                            prelat_next, prelon_next = pre["latitude"].iloc[i+1], pre["longitude"].iloc[i+1]
                            where_going = mesh_latlon_return.vincenty_inverse(prelat, prelon, prelat_next, prelon_next)
                            azimuth_going = where_going["azimuth1"]
                            x = 20
                            for t in range(len(matched)):
                                try:
                                    matlat, matlon = matched["latitude"].iloc[t], matched["longitude"].iloc[t]
                                    calc = mesh_latlon_return.vincenty_inverse(prelat, prelon, matlat, matlon)
                                    if 0 <= azimuth_going < 180.0:
                                        if calc["distance"] < x and azimuth_going < calc["azimuth1"] < azimuth_going+180 :#azimuth1は始点(pre)から終点(mat)の方位角
                                            x = calc["distance"]
                                            print("small azimuth", azimuth_going)
                                            continue

                                        #elif calc["distance"] < x:
                                         #   x = 0 * calc["distance"]
                                    elif 180.0 <= azimuth_going:
                                        if calc["distance"] < x and (0 < calc["azimuth1"] <azimuth_going -180 or azimuth_going < calc[azimuth_going] < 360):
                                            x = calc["distance"]
                                            print("big azimuth", azimuth_going)
                                            continue

                                       # elif calc["distance"] < x:
                                         #   x = 0 * calc["distance"]
                                    else:
                                        print(azimuth_going)



                                except Exception as e:
                                    print(e)
                            print(x,"m")
                            if x < min_m:
                                print([x, prelat, prelon, calc["azimuth1"]])
                                distance.append([x, prelat, prelon])
                    #mean = statistics.mean(distance[:][0])
                    #print(mean)
                    os.makedirs("C:/Users/hysir/Desktop/研究室/matching/distance_data/" + str(
                        mesh_srt) + "_" + bus_type + "_" + which_going, exist_ok=True)

                    df = pd.DataFrame(distance, columns=["distance", "latitude", "longitude"])
                    df.to_csv("C:/Users/hysir/Desktop/研究室/matching/distance_data/"+str(mesh_srt)+"_"+bus_type+"_"+which_going+"/distance"+day+"_"+str(mesh_srt)+"_"+bus_type+"_"+which_going+".csv")
                    print("finish")
                except Exception as e:
                    print(e)
    except Exception as e: print("not file", e)


print("finish")