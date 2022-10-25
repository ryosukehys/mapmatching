import plotly .graph_objects as go
import pandas as pd

dayss = [str(i) for i in range(20210901, 20210931)] + [str(i) for i in range(20211001, 20211031)] + [str(i) for i in range(20211201, 20211231)]+ [str(i) for i in range(20220101, 20220131)]

for day in dayss:
    try:
        matched = pd.read_csv("C:/Users/hysir/Desktop/研究室/matching/matched_data/matching"+day+".csv")
        pre = pd.read_csv("C:/Users/hysir/Desktop/研究室/matching/matched_data/premesh"+day+"mesh.csv")

        latitude_match = matched.iloc[:,2]
        longitude_match = matched.iloc[:,1]
        latitude_pre = pre.iloc[:,2]
        longitude_pre = pre.iloc[:,1]

        fig = go.Figure()
        fig.add_trace(
            go.Scattermapbox(
            lat=latitude_pre,
            lon=longitude_pre,
            mode="markers",
            name="data",
            marker=dict(color="red")
        ))
        fig.add_trace(
            go.Scattermapbox(
            lat=latitude_match,
            lon=longitude_match,
            mode="markers",
            name="matched data",
            marker=dict(color="blue")
        ))


        fig.update_layout(
            hovermode='closest',
            mapbox=dict(
                bearing=0,
                center=go.layout.mapbox.Center(
                    lat=45,
                    lon=143
                ),
                pitch=0,
                zoom=5,
                style="open-street-map"
            )
        )
        fig.update_layout(mapbox_style="open-street-map")

        fig.write_html("C:/Users/hysir/Desktop/研究室/matching/matched_map/"+day+".html")
        print("finish")
    except Exception as e:
        print(e)