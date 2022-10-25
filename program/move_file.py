import glob
import shutil
import os

months = [str(i) for i in range(20211101, 20211131)]
month = months[1][0:6]
bus_type = "bus_B"
path = "C:/Users/hysir/Desktop/研究室/kyosaku_work/depth_fig/"
filelist = []
os.makedirs("C:/Users/hysir/Desktop/研究室/matching/original_data/"+month+"_"+bus_type, exist_ok=True)
for day in months:
    for t in glob.glob(path+day+"_"+bus_type+"/newmeshwitharea_nostep"+day+"_"+bus_type+"_*.csv"):
        shutil.move(t,"C:/Users/hysir/Desktop/研究室/matching/original_data/"+month+"_"+bus_type+"/")

print(filelist)