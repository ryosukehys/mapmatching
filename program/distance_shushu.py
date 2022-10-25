import pandas as pd
import statistics

dayss = [[str(i) for i in range(20210901, 20210931)],[str(i) for i in range(20211001, 20211031)],[str(i) for i in range(20211101, 20211131)], [str(i) for i in range(20211201, 20211231)], [str(i) for i in range(20220101, 20220131)]]
month = ["202109", "202110","202111", "202112", "202201"]
which_going = "Wakkanai"
bus_type = "bus_B"
mesh = pd.read_csv("C:\\Users\hysir\Desktop\研究室\kyosaku_work\mesh_all.csv")
mesh_list = list(mesh["meshcode"])

stat_dic = dict()
dir = "C:/Users/hysir/Desktop/研究室/matching/distance_data_all/"

for mesh in mesh_list[5:]:
    try:
        mesh = str(mesh)[0:8]

        mesh_srt = int(mesh + "00")
        mesh_end = int(mesh + "99")

        stat_lis=[]

        for mon in month:
            try:
                df_stat_mon = pd.read_csv(dir+str(mesh_srt)+"_"+bus_type+"_"+which_going+"/statistics_"+mon+"_"+str(mesh_srt)+"_"+bus_type+".csv")
                mean_month = sorted(list(df_stat_mon["mean"]))
                mean_month_lis = mean_month[1:-1]
                mean_month = round(statistics.mean(mean_month_lis),3)
                std = round(statistics.pstdev(mean_month_lis), 3)
                stat_lis.append(str(mean_month)+"±"+str(std))

            except Exception as e: print("wow", e)

        stat_dic[str(mesh_srt)] = stat_lis

    except Exception as e: print(e)

save = pd.DataFrame.from_dict(stat_dic, orient="index", columns=month)
save = save.dropna(how="any")
save.to_csv(dir+"all_distance_ver3.csv", encoding="shift-jis")