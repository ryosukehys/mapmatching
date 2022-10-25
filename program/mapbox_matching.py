import glob
import pandas as pd
import numpy as np
from mapbox import MapMatcher
import mesh_latlon_return
import os

days = [str(i) for i in range(20211101, 20211131)]
month = days[1][0:6]
which_going = "Wakkanai"
bus_type = "bus_B"
os.makedirs("C:/Users/hysir/Desktop/研究室/matching/matched_data/"+month+"_"+bus_type+"_"+which_going, exist_ok=True)
for day in days:
    try:
        df = pd.read_csv("C:/Users/hysir/Desktop/研究室/matching/original_data/"+month+"_"+bus_type+"/newmeshwitharea_nostep"+day+"_"+bus_type+"_to"+which_going+".csv")
        latlon = []

        for lat, lon in zip(df["latitude_exchange"], df["longitude_exchange"]):
            latlon.append([lon,lat])

        imgnamex = list(df["image_name"])
        imglist = []
        for imgname in imgnamex:
            img = "20"+imgname[6:8]+"-"+imgname[8:10]+"-"+imgname[10:12]+"T"+imgname[13:15]+":"+imgname[15:17]+":"+imgname[17:19]+"Z"
            imglist.append(img)


        service = MapMatcher(access_token="pk.eyJ1IjoicnlvMTFoeXMiLCJhIjoiY2w3OGZ5a3F4MDk4YjN2czlzbGFwMGd1aCJ9.ebDE0Nqg_VaPzTF57ou66A")

        # map matching api は一度に100件までしか処理できないため分割処理
        corrected = []
        dist = 0
        for i in range(len(latlon) // 100 + 1):
            # apiの入力形式に合わせる
            line = {}
            line["type"] = "Feature"
            line["properties"] = {"coordTimes": imglist[i * 100:(i + 1) * 100]}
            line["geometry"] = {"type": "LineString", "coordinates": latlon[i * 100:(i + 1) * 100]}

            response = service.match(line, profile='mapbox.driving')
            print(i, response)
            # 結果を統合
            try:
                for i in response.geojson()['features']:
                    corrected.extend(i["properties"]["matchedPoints"])
                    dist += i["properties"]["distance"]
            except KeyError:
                pass



        correct = pd.DataFrame(corrected, columns=["longitude", "latitude"])

        correct.to_csv("C:/Users/hysir/Desktop/研究室/matching/matched_data/"+month+"_"+bus_type+"_"+which_going+"/"+day+"_"+bus_type+"_.csv")
        prematch = pd.DataFrame(latlon, columns=["longitude", "latitude"])
        mesh_latlon_return.mesh_contact_match("C:/Users/hysir/Desktop/研究室/matching/matched_data/"+month+"_"+bus_type+"_"+which_going+"/", prematch, bus_type,day)
    except Exception as e:
        print(e)