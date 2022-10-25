import  pandas as pd
import folium

df = pd.read_csv("C:\\Users\hysir\Desktop\研究室\matching\matched_data\\202201_bus_B_Wakkanai\\20220105_bus_B_.csv")

x = folium.Map(tiles="OpenStreetMap")
folium.PolyLine(df[["latitude", "longitude"]].values, color="blue",weight=5 ).add_to(x)
x.fit_bounds([[df["latitude"].min(), df["longitude"].min()],
                       [df["latitude"].max(), df["longitude"].max()]])
x.save("map.html")