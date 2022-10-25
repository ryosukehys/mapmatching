import os
import csv
import json
import datetime
import time
import configparser
import requests

# 入力CSVファイル指定
input_csvfile = "C:/Users/hysir/Desktop/20220109_do_mapbox.csv"

# 出力CSVファイル指定
output_csvfile = "C:/Users/hysir/Desktop/20220109_did_mapbox.csv"

# Map Matching API URL※変更しないでください。
api_url = "https://api.mapbox.com/matching/v5/mapbox/driving/"

# Mapbox Access token
api_token = "Apk.eyJ1IjoicnlvMTFoeXMiLCJhIjoiY2w3OGZ5a3F4MDk4YjN2czlzbGFwMGd1aCJ9.ebDE0Nqg_VaPzTF57ou66A"

# 作業用リスト
data = []
wklst = []

# 入力CSVファイルを作業用リストへセット
with open(input_csvfile, encoding="utf-8") as f:
    #ヘッダー行をスキップ
    h = next(csv.reader(f))
    for v in csv.reader(f):
        data.append(v)
print(data)
for i in range(len(data) -1):
    wklst.append([data[i][0],data[i][1],data[i+1][0],data[i+1][1]])

print(wklst)

# 出力CSVファイルの存在チェック(ヘッダー有無の判断)
if(os.path.exists(output_csvfile)):
    header_flg = 0
else:
    header_flg = 1

# 作業用リストよりMap Matching APIへリクエストし、結果を出力CSVファイルに書き込む
with open(output_csvfile, 'a', encoding='utf-8') as output_csvfile_fp:

    fieldnames = ['bef_lat','bef_lng','aft_lat','aft_lng']
    csvfile_writer = csv.DictWriter(output_csvfile_fp, fieldnames=fieldnames,lineterminator='\n')

    # 出力CSVファイル新規作成時、ヘッダー出力
    if header_flg == 1:
        csvfile_writer.writeheader()
        header_flg == 0

    print(len(wklst))
    for i in range(len(wklst)):
        # print(wklst[i])
        # Map Matching APIのパラメータ生成
        origins = wklst[i][1] + ','+ wklst[i][0]
        destinations = wklst[i][3] + ','+ wklst[i][2]
        params = {
            'radiuses':'50;50',
            'access_token': api_token
            }
        # Map Matching APIにリクエスト
        raw_response = requests.get(api_url + origins + ';' + destinations+".json?"+ "access_token="+"pk.eyJ1IjoicnlvMTFoeXMiLCJhIjoiY2w3OGZ5a3F4MDk4YjN2czlzbGFwMGd1aCJ9.ebDE0Nqg_VaPzTF57ou66A")
        parsed_response = json.loads(raw_response.text)
        parsed_response_json = json.dumps(parsed_response, indent=4)
        # print(parsed_response_json)
        breakpoint
        print(parsed_response)
        # JSONから要素を取り出す
        if parsed_response['code'] == 'Ok':
            lng1 = parsed_response['tracepoints'][0]['location'][0]
            lat1 = parsed_response['tracepoints'][0]['location'][1]
            lng2 = parsed_response['tracepoints'][1]['location'][0]
            lat2 = parsed_response['tracepoints'][1]['location'][1]
        else:
            lng1 = None
            lat1 = None
            lng2 = None
            lat2 = None

        # 出力CSVファイルに書き込み
        csvfile_writer.writerow({
            'bef_lat': wklst[i][0],
            'bef_lng': wklst[i][1],
            'aft_lat': lat1,
            'aft_lng': lng1
            })

        print(wklst[i][0],wklst[i][1],lat1,lng1)

print(u'処理終了')