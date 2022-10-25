import os

import pandas as pd
import plot

dayss = [[str(i) for i in range(20210901, 20210931)],[str(i) for i in range(20211001, 20211031)], [str(i) for i in range(20211201, 20211231)], [str(i) for i in range(20220101, 20220131)]]
which_going = "Wakkanai"
bus_type = "bus_B"

for days in dayss:
    month = days[1][0:6]
    for day in days:
        try:
            psb = plot.PlotSoyaBus(date=day)
            folium_map = psb.generate()
            df = pd.read_csv("C:/Users/hysir/Desktop/研究室/matching/original_data/"+month+"_"+bus_type+"/newmeshwitharea_nostep"+day+"_"+bus_type+"_to"+which_going+".csv")
            folium_map = psb.plot_point_with_roadcondition(folium_map, df, month, day)
            os.makedirs("C:/Users/hysir/Desktop/研究室/matching/roadcondition_map/"+month+"_"+bus_type+"_"+which_going, exist_ok=True)
            psb.save_map(folium_map, "C:/Users/hysir/Desktop/研究室/matching/roadcondition_map/"+month+"_"+bus_type+"_"+which_going+"/"+day+"_"+bus_type+"_"+which_going)

        except Exception as e:
            print(e)

