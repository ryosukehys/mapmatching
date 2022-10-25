import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import japanize_matplotlib
import plotly.express as px
import plotly.graph_objects as go

def mesh_chu(path):
    df = pd.read_csv(path)
    mesh_list = list(df["meshcode"])
    mesh_list = [str(i)[0:8]+"00" for i in mesh_list] #8桁のメッシュ飲み抜き出す
    mesh_list = list(dict.fromkeys(mesh_list)) #重複排除
    return mesh_list

def mesh_kotei(alldis, mesh_list):
    df_heni = pd.read_csv(alldis)
    meshcode_in_dis = list(df_heni["meshcode"])
    meshcode_in_dis = [int(i) for i in meshcode_in_dis]
    lis = []
    for mesh in mesh_list:
        try:
            index = meshcode_in_dis.index(int(mesh))
            heni09, heni10, heni12, heni01 = list(df_heni["202109"]), list(df_heni["202110"]), list(
                df_heni["202112"]), list(df_heni["202201"])
            lis.append([mesh, heni09[index], heni10[index], heni12[index], heni01[index]])
        except Exception as e:
            print("Error!", e)
    return pd.DataFrame(lis, columns=["meshcode", "202109", "202110", "202112", "202201"])

def graph(df, savetile, month1="202109", month2="202112", month3=False):
    meshcode_list = list(df["meshcode"])
    dis_1, dis_2 = list(df[month1]), list(df[month2])
    graphtitle = "走行位置変位:"+month1+"-"+month2
    heni = [dis2-dis1 for (dis1, dis2) in zip(dis_1, dis_2)]

    plt.figure(figsize=(15,5))
    plt.title(graphtitle)
    plt.grid()
    plt.ylim(-4, 4)
    sb.lineplot(meshcode_list, heni, alpha=0.6)
    if month3:
        dis_3 = list(df[month3])
        heni2 = [dis3-dis1 for (dis1, dis3) in zip(dis_1, dis_3)]
        sb.lineplot(meshcode_list, heni2, alpha=0.6)
        plt.legend(labels=["202112", "202201"])
    location = [ 6741657900, 6741369600, 6641451500, 6441439300]
    location = [str(t) for t in location]
    locaton_name = ["豊富北IC", "幌延IC", "羽幌町", "札幌JCT"]
    plt.xticks(location, locaton_name)
    plt.savefig("C:/Users/hysir/Desktop/研究室/matching/"+savetile+".png")

def heni(df, month1="202109", month2="202112"):
    dis_1, dis_2 = list(df[month1]), list(df[month2])
    return [dis2-dis1 for (dis1, dis2) in zip(dis_1, dis_2)]


savedir="C:\\Users\hysir\Desktop\研究室\matching\distance_data_all/"
all_distance = "C:\\Users\hysir\Desktop\研究室\matching\distance_data_all\\all_distance.csv"
mesh_all = "C:\\Users\hysir\Desktop\研究室\kyosaku_work\mesh_all.csv"


mesh_list = mesh_chu(mesh_all)
df = mesh_kotei(all_distance, mesh_list)
y_1 = heni(df, month1="202109", month2="202112")
y_2 = heni(df, month1="202109", month2="202201")
fig = go.Figure()
fig.add_trace(go.Scatter(x=mesh_list, y=y_1, name="202109-202112", line=dict(width=4)))
fig.add_trace(go.Scatter(x=mesh_list, y=y_2, name="202109-202201", line=dict(width=4)))
fig.update_layout(title="走行位置変位:202109-202112, 202109-202201")
fig.write_html("C:/Users/hysir/Desktop/研究室/matching/wow.html")


"""matplot での描画　インタラクティブではない
mesh_list = mesh_chu(mesh_all)
df = mesh_kotei(all_distance, mesh_list)
graph(df, month1="202109", month2="202112",month3="202201", savetile="走行位置変位091201")"""