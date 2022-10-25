import pandas as pd

def mesh_chu(path):
    df = pd.read_csv(path)
    mesh_list = list(df["meshcode"])
    mesh_list = [str(i)[0:8]+"00" for i in mesh_list] #8桁のメッシュ飲み抜き出す
    mesh_list = list(dict.fromkeys(mesh_list)) #重複排除
    return mesh_list

def mesh_with_kyosaku(henipath, mesh_list):
    df_heni = pd.read_csv(henipath)
    dic = []
    for mesh in mesh_list:
        try:
            meshcode = list(df_heni["meshcode"])
            meshcode = [int(i) for i in meshcode]
            index = meshcode.index(int(mesh))
            print(index)
            heni09, heni10,heni11, heni12, heni01 = list(df_heni["202109"]), list(df_heni["202110"]),list(df_heni["202111"]), list(df_heni["202112"]), list(df_heni["202201"])
            dic.append([mesh, heni09[index], heni10[index],heni11[index], heni12[index], heni01[index]])
        except Exception as e:
            print("Error!",e)
    print(dic)
    return pd.DataFrame(dic, columns=["meshcode", "202109", "202110","202111",  "202112", "202201"])

savedir="C:\\Users\hysir\Desktop\研究室\matching\distance_data_all/"
all_distance = "C:\\Users\hysir\Desktop\研究室\matching\distance_data_all\\all_distance.csv"

for i in range(5):
    kukan_path = "C:\\Users\hysir\Desktop\研究室\kyosaku_work\koutei_kukan"+str(i)+".csv"
    mesh_list = mesh_chu(kukan_path)
    df = mesh_with_kyosaku(all_distance, mesh_list)
    df.to_excel(savedir+"distance_kukan"+str(i)+".xlsx")
