import re, os, sys
import pandas as pd
import folium

# 宗谷バスのデータをプロットするためのクラス
class PlotSoyaBus(object):
    # 初期値設定
    def __init__(self, date, tiles='OpenStreetMap'):
        self.date = str(date),
        self.path = "/Users/hayashi/Desktop/研究室_now/kyosaku/"
        self.tiles = tiles

    # foliumインスタンスを生成する関数
    def generate(self):
        return folium.Map(
            tiles=self.tiles
        )

    # 緯度経度の計算をする関数
    def exchange_dm(self, x):
        deg, minute = int(x / 100), x % 100
        return deg + (minute / 60)
    
    # 変換したデータを追加する関数
    def calculate_dm(self, data):
        exchange_ll_list = []
        for i in range(data.shape[0]):
            x, y = data['latitude'].iloc[i], data['longitude'].iloc[i]
            latitude, longitude = self.exchange_dm(x), self.exchange_dm(y)
            exchange_ll_list.append([latitude, longitude])
        # データフレームを作成
        exchange_ll_df = pd.DataFrame(exchange_ll_list, columns=['latitude_exchange', 'longitude_exchange'])
        # 元のデータフレームにデータを追加して返す
        return pd.concat([data, exchange_ll_df], axis=1)
    
    # 地図に点を追加する関数
    def plot_point(self, folium_map, data, color='red', interval=1):
        for i, (name, x, y) in enumerate(data[['image_name', 'latitude_exchange', 'longitude_exchange']].values):
            # すべてのデータではなくintervalごとにプロットする
            html = '<h4>'+name+'</h4> "<img src="http://stakahashi.ddns.net/webdav2021LAMTp8st/soyaBUS/202201/20220116/'+name+'" width="320" height="240"   >'
            if i % interval == 0:
                folium.Marker(
                    location=[x, y],
                    popup=name,
                    icon=folium.Icon(color=color),
                ).add_to(folium_map)
        # 地図の表示範囲を緯度経度の最低最大とする
        folium_map.fit_bounds([[data["latitude_exchange"].min(),data["longitude_exchange"].min()], [data["latitude_exchange"].max(),data["longitude_exchange"].max()]])
        return folium_map


    #狭窄を色で表す かつ、popupに画像はっつけ line版
    def plot_point_with(self, folium_map, data, color1="blue", color2="orange", color3="red"):
        for i, (name, x, y, kyosaku) in enumerate(data[["image_name", "latitude_exchange", "longitude_exchange", "kyosaku_line"]].values):
            #html = '<h4>'+name+':'+str(kyosaku)+'</h4> "<img src="./20220116jpg_forplot/'+name+'" width="320" height="240"   >'
            html = '<h4>'+name+':'+str(kyosaku)+'</h4> "<img src="http://stakahashi.ddns.net/webdav2021LAMTp8st/soyaBUS/202201/20220116/'+name+'" width="320" height="240"   >'

            if kyosaku < 240:
                folium.Marker(
                    location=[x, y],
                    popup= html,
                    icon=folium.Icon(color=color1)
                ).add_to(folium_map)
            elif 240 <= kyosaku < 360:
                folium.Marker(
                    location=[x, y],
                    popup=html,
                    icon=folium.Icon(color=color2)
                ).add_to(folium_map)
            elif kyosaku >=360:
                folium.Marker(
                    location=[x, y],
                    popup=html,
                    icon=folium.Icon(color=color3)
                ).add_to(folium_map)
        # 地図の表示範囲を緯度経度の最低最大とする
        folium_map.fit_bounds([[data["latitude_exchange"].min(), data["longitude_exchange"].min()],
                                       [data["latitude_exchange"].max(), data["longitude_exchange"].max()]])
        return folium_map

    #路面状態を可視化したマップを作ってみる
    def plot_point_with_roadcondition(self, folium_map, data, month, mon, interval=5, color1="blue", color2="red"):
        for i, (name, x, y, roadcondition, mesh) in enumerate(data[["image_name", "latitude_exchange", "longitude_exchange", "roadSurface", "meshcode"]].values):
            if i % interval == 0:
                #html = '<h4>'+name+':'+str(kyosaku)+'</h4> "<img src="./20220116jpg_forplot/'+name+'" width="320" height="240"   >'
                html = '<h4>'+name+":"+str(data.iloc[i, 0])+':'+roadcondition+":"+str(mesh)+'</h4> "<img src="http://stakahashi.ddns.net/webdav2021LAMTp8st/soyaBUS/'+month+'/'+mon+'/'+name+'" width="320" height="240"   >'

                if roadcondition == "dry" or roadcondition == "semi-wet" or roadcondition == "wet":
                    folium.Marker(
                        location=[x, y],
                        popup= html,
                        icon=folium.Icon(color=color1)
                    ).add_to(folium_map)
                elif roadcondition == "slush" or roadcondition == "ice" or roadcondition == "fresh":
                    folium.Marker(
                        location=[x, y],
                        popup=html,
                        icon=folium.Icon(color=color2)
                    ).add_to(folium_map)
            else:
                pass
        # 地図の表示範囲を緯度経度の最低最大とする
        folium_map.fit_bounds([[data["latitude_exchange"].min(), data["longitude_exchange"].min()],
                                       [data["latitude_exchange"].max(), data["longitude_exchange"].max()]])
        return folium_map

    #狭窄を色で表す+popupに画像はっつけ area版
    def plot_point_with_area(self, folium_map, data, month, mon, interval=1, color1="blue", color2="orange", color3="red"):
        for i, (name, x, y, kyosaku, mesh) in enumerate(data[["image_name", "latitude_exchange", "longitude_exchange", "kyosaku", "meshcode"]].values):
            if i % interval == 0:
                kyosaku = kyosaku/76800
                kyosaku = round(kyosaku, 3)
                #html = '<h4>'+name+':'+str(kyosaku)+'</h4> "<img src="./20220116jpg_forplot/'+name+'" width="320" height="240"   >'
                html = '<h4>'+name+":"+str(data.iloc[i, 0])+':'+str(kyosaku)+":"+str(mesh)+'</h4> "<img src="http://stakahashi.ddns.net/webdav2021LAMTp8st/soyaBUS/'+month+'/'+mon+'/'+name+'" width="320" height="240"   >'

                if kyosaku < 0.25:
                    folium.Marker(
                        location=[x, y],
                        popup= html,
                        icon=folium.Icon(color=color1)
                    ).add_to(folium_map)
                elif 0.25 <= kyosaku < 0.4:
                    folium.Marker(
                        location=[x, y],
                        popup=html,
                        icon=folium.Icon(color=color2)
                    ).add_to(folium_map)
                elif kyosaku > 0.4:
                    folium.Marker(
                        location=[x, y],
                        popup=html,
                        icon=folium.Icon(color=color3)
                    ).add_to(folium_map)
            else:
                pass
        # 地図の表示範囲を緯度経度の最低最大とする
        folium_map.fit_bounds([[data["latitude_exchange"].min(), data["longitude_exchange"].min()],
                                       [data["latitude_exchange"].max(), data["longitude_exchange"].max()]])
        return folium_map


    #狭窄を色で表す+popupに画像はっつけ area版
    def plot_point_with_area_minuswinter(self, folium_map, data, month, mon, interval=1, color1="blue", color2="orange", color3="red"):
        for i, (name, x, y, kyosaku, mesh) in enumerate(data[["image_name", "latitude", "longitude", "kyosaku", "meshcode"]].values):
            if i % interval == 0:
                kyosaku = kyosaku/76800
                kyosaku = round(kyosaku, 3)
                #html = '<h4>'+name+':'+str(kyosaku)+'</h4> "<img src="./20220116jpg_forplot/'+name+'" width="320" height="240"   >'
                html = '<h4>'+name+":"+str(kyosaku)+":"+str(mesh)+'</h4> "<img src="http://stakahashi.ddns.net/webdav2021LAMTp8st/soyaBUS/'+month+'/'+mon+'/'+name+'" width="320" height="240"   >'

                if kyosaku < 0.05:
                    folium.Marker(
                        location=[x, y],
                        popup= html,
                        icon=folium.Icon(color=color1)
                    ).add_to(folium_map)
                elif 0.05 <= kyosaku < 0.2:
                    folium.Marker(
                        location=[x, y],
                        popup=html,
                        icon=folium.Icon(color=color2)
                    ).add_to(folium_map)
                elif kyosaku > 0.2:
                    folium.Marker(
                        location=[x, y],
                        popup=html,
                        icon=folium.Icon(color=color3)
                    ).add_to(folium_map)
            else:
                3
                4
                5
                6
                2
                2
                0
                0
                pass
        # 地図の表示範囲を緯度経度の最低最大とする
        folium_map.fit_bounds([[data["latitude"].min(), data["longitude"].min()],
                                       [data["latitude"].max(), data["longitude"].max()]])
        return folium_map



    # 地図上に線を追加する関数
    def plot_line(self, folium_map, data, color='blue'):
        folium.PolyLine(
            data[['latitude_exchange', 'longitude_exchange']].values,
            color=color
        ).add_to(folium_map)
        folium_map.fit_bounds([[data["latitude_exchange"].min(),data["longitude_exchange"].min()], [data["latitude_exchange"].max(),data["longitude_exchange"].max()]])
        return folium_map
    
    # htmlファイルとして出力する関数
    def save_map(self, folium_map, file_name):
        folium_map.save(file_name+ ".html")