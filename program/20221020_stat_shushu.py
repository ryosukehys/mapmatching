import pandas as pd

def shushu(data, lis_all):
    lis = []
    day, mean, stdev, numofdata = list(data["day"]), list(data["mean"]), list(data["stdev"]), list(data["num of data"])
    for i in range(len(day)):
        lis.append([day[i], mean[i], stdev[i], numofdata[i]])
        lis_all.append([day[i], mean[i], stdev[i], numofdata[i]])


def data_load(meshcode, month):
    meshcode = str(meshcode)
    month = str(month)
    df = pd.read_csv("C:/Users/hysir/Desktop/研究室/matching/distance_data_all/"+meshcode+"00_bus_B_Wakkanai/statistics_"+month+"_"+meshcode+"00_bus_B.csv")
    return df

months = [202109, 202110, 202111, 202112, 202201]
lis_all = []
mesh = 66412522
savedir = "C:/Users/hysir/Desktop/研究室/matching/distance_data_all/"+mesh+"00_bus_B_Wakkanai/"

for month in months:
    data = data_load(mesh, month)
    lis, lis_all = shushu(data, lis_all)
    lis = pd.DataFrame(lis, columns=["day", "mean", "stdev", "numofdata"])
    lis.to_excel()