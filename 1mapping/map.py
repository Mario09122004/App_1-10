import folium
import pandas
import json
with open("./world.json", encoding="utf-8-sig") as f:
    world_data = json.load(f)
    
def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

file = pandas.read_csv("./Volcanoes.txt", sep=",")

name = list(file["NAME"])
longitude = list(file["LON"])
latitude = list(file["LAT"])
elev = list(file["ELEV"])
type = list(file["TYPE"])
status = list(file["STATUS"])
location = list(file["LOCATION"])
timeframe = list(file["TIMEFRAME"])

html = "<h4>Volcanoes information</h4>"

map = folium.Map(location=[45.5236, -122.6750], zoom_start=6, tiles="OpenStreetMap")

fg = folium.FeatureGroup(name="Population")
fgv = folium.FeatureGroup(name="Volcanoes")

for x,y,z,a,b,c,d,e in zip(name, longitude, latitude, elev, type, status, location, timeframe):
    iframe = folium.IFrame(
        html=html + f"{x}<br>Longitude: {y}<br>Latitude: {z}<br>Elevation: {a} m<br>Type: {b}<br>Status: {c}<br>Location: {d}<br>Timeframe: {e}",
        width=200,
        height=100
    )

    border_color = color_producer(a)

    icon_html = f"""
    <div style="
        background-color: #ffffff00;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 5px solid {border_color};
    ">
        <img src="volcan.png" style="width:30px;height:30px;border-radius:50%;" />
    </div>
    """

    fgv.add_child(folium.Marker(
        location=[z, y],
        popup=folium.Popup(iframe),
        icon=folium.DivIcon(html=icon_html)
    ))

fg.add_child(
    folium.GeoJson(
        data=world_data,
        style_function=lambda x: {
            'fillColor': 'green' if x['properties']['POP2005'] < 10000000
            else 'yellow' if 10000000 <= x['properties']['POP2005'] < 20000000
            else 'red'
        }
    )
)

map.add_child(fg)
map.add_child(fgv)
map.add_child(folium.LayerControl())

map.save("map.html")