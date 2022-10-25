import pandas as pd
import statistics

dayss = [str(i) for i in range(20210901, 20210931)] + [str(i) for i in range(20211001, 20211031)] + [str(i) for i in range(20211201, 20211231)] + [str(t) for t in range(20220101, 20220131)]
which_going = "Wakkanai"
bus_type = "bus_B"
mesh_srt = 64414380
dir = "C:/Users/hysir/Desktop/研究室/kyosaku_work/original_data/"
df_med = pd.read_csv("C:\\Users\hysir\Desktop\研究室\kyosaku_work\Sapporo_mesh_to"+which_going+".csv")

mesh_sum = [str(i) for i in list(df_med.columns)]
med_sum = list(df_med.median())
results = {}
for day in dayss:

    month = day[0:6]
    lis = []
    try:
        csv_path = dir + month + "_" + bus_type + "/newmeshwitharea_nostep" + day + "_" + bus_type + "_to" + which_going + ".csv"
        data = pd.read_csv(csv_path)

        for i in range(0, len(data)):
            try:
                mesh = str(data["meshcode"].iloc[i])
                if mesh[0:8] == str(mesh_srt):
                    kyosaku = data["kyosaku"].iloc[i]
                    lis.append(kyosaku)
                    #print(kyosaku)


            except Exception as e:
                print(e)
        kyosaku = statistics.mean(lis)
        results.setdefault(day, [])
        results[day].append(kyosaku)
        print(results)



    except Exception as e:
        print(e)

df = pd.DataFrame.from_dict(results, orient="index",
                                    columns=["kyosaku"])
df.to_csv("C:/Users/hysir/Desktop/研究室/matching/kyosaku_mesh/result" + str(mesh_srt) + "_" + which_going + ".csv")
