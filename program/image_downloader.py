import pandas as pd
import os
import pprint
import time
import urllib.error
import urllib.request

def download_file(url, dst_path):
    try:
        with urllib.request.urlopen(url) as web_file:
            data = web_file.read()
            with open(dst_path, mode='wb') as local_file:
                local_file.write(data)
    except urllib.error.URLError as e:
        print(e)

def download_file_to_dir(url, dst_dir, date):
    download_file(url, os.path.join(dst_dir, date+".jpg"))

days = [str(i) for i in range(20210901, 20210931)] + [str(i) for i in range(20211001, 20211031)] + [str(i) for i in range(20211201, 20211231)] + [str(i) for i in range(20220101, 20220131)]
#days = ["20211201"]
path = "C:/Users/hysir/Desktop/研究室/matching/original_data/"
which_going = "toWakkanai"
bus_type = "bus_B"




mesh = pd.read_csv("C:\\Users\hysir\Desktop\研究室\kyosaku_work\mesh_all.csv")
mesh_list = list(mesh["meshcode"])
mesh_list = [str(i)[0:8] for i in mesh_list]
mesh_list = list(set(mesh_list))
for mesh in mesh_list:
    try:
        meshcode = str(mesh)
        dst_dir = "C:/Users/hysir/Desktop/研究室/matching/区間前方画像_ALL/" + meshcode + "_" + bus_type + "_" + which_going + "/"



        for day in days:
            try:
                month = day[0:6]
                os.makedirs("C:/Users/hysir/Desktop/研究室/matching/区間前方画像_ALL/"+meshcode+"_"+bus_type+"_"+which_going , exist_ok=True)
                #os.makedirs("C:/Users/hysir/Desktop/研究室/matching/区間_前方画像/" + meshcode + "_" + bus_type+"/"+day, exist_ok=True)
                dr_dir = dst_dir + "/" + day + "/"
                folder_path = path + month + "_" + bus_type +"/"
                file_path = folder_path + "newmeshwitharea_nostep"+day+"_"+bus_type+"_"+which_going+".csv"
                df = pd.read_csv(file_path)
                image_name_list = list(df["image_name"])
                meshcode_list = list(df["meshcode"])
                meshcode_list = [str(i)[0:len(meshcode)] for i in meshcode_list]
                print([i for i in range(len(meshcode_list)) if meshcode_list[i]==meshcode])
                mesh_index_list = [i for i in range(len(meshcode_list)) if meshcode_list[i] == meshcode]
                if mesh_index_list:
                    for i in mesh_index_list:
                        image_name = image_name_list[i]
                        save_name = meshcode + "_" + which_going +"_"+ image_name[:-4]
                        os.makedirs("C:/Users/hysir/Desktop/研究室/matching/区間前方画像_ALL/" + meshcode + "_" + bus_type +"_"+which_going +"/" + day,
                                    exist_ok=True)
                        imagefile = "http://stakahashi.ddns.net/webdav2021LAMTp8st/soyaBUS/" + month + '/' + day + '/' + image_name
                        download_file_to_dir(imagefile, dr_dir, save_name)
            except Exception as e:
                print(e)
    except Exception as e: print(e, "wow")