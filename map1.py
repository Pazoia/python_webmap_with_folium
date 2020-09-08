import folium
import pandas

data = pandas.read_csv("files/Volcanoes.txt")

lat = list(data["LAT"])
lon = list(data["LON"])
elevation = list(data["ELEV"])
name = list(data["NAME"])

html = """
Volcano name: <br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

def color_producer(elevation):
    if elevation < 1000:    
        return "green"  
    elif 1000 <= elevation < 3000:  
        return "orange"
    else:
        return "red"

map = folium.Map(location=[39.54, -119.79], zoom_start=6, tiles="Stamen Terrain")

feature_group_population = folium.FeatureGroup(name="Population")

feature_group_population.add_child(folium.GeoJson(data=open("files/world.json", "r", encoding="utf-8-sig").read(), 
style_function=lambda x: {
    "fillColor":"green" if x["properties"]["POP2005"] < 10000000
    else "orange" if 10000000 <= x["properties"]["POP2005"] < 20000000
    else "red"}
))

feature_group_volcanos = folium.FeatureGroup(name="Volcanoes")

for lt, ln, elv, name in zip(lat, lon, elevation, name):
    iframe = folium.IFrame(html=html % (name, name, elv), width=200, height=100)
    feature_group_volcanos.add_child(folium.CircleMarker(
        location=[lt, ln], 
        radius=7, 
        popup=folium.Popup(iframe), 
        fill_color=color_producer(elv), 
        color=color_producer(elv), 
        fill_opacity=0.8
        ))

map.add_child(feature_group_population)
map.add_child(feature_group_volcanos)
folium.LayerControl().add_to(map)

map.save("Map1.html")
