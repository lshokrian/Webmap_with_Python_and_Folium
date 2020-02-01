import folium
import pandas
import json

def elev_color(elev):
    if elev > 3000:
        return "red"
    elif elev > 2000:
        return "orange"
    elif elev > 1000:
        return "beige"
    else:
        return "green"

valcanoes = pandas.read_csv("Volcanoes.txt")
capitals = pandas.read_csv("concap.csv")
nationalParks = json.load(open("nationalParks.json"))

#US Volcano Data
volcanoX = list(valcanoes["LAT"])
volcanoY = list(valcanoes["LON"])
volcanoElevation = list(valcanoes["ELEV"])
volcanoName = list(valcanoes["NAME"])

#Country Capitals Data
capitalX = list(capitals["CapitalLatitude"])
capitalY = list(capitals["CapitalLongitude"])
capitalName = list(capitals["CapitalName"])

#National Park Data
nationalParkX = []
nationalParkY = []
nationalParkNames = []
for park in nationalParks:
    nationalParkX.append(park["coordinates"]['latitude'])
    nationalParkY.append(park["coordinates"]['longitude'])
    nationalParkNames.append(park["title"])

#Create Map
map = folium.Map(location = [40.749, -73.575], zoom_start=1, tiles="Stamen Terrain")

#Volcano Information
html = """
<h4>Volcano information:</h4><br>
<a href = "https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Name: %s
Height: %s m """

#Volcano Feature Group
fgv = folium.FeatureGroup(name = "Volcanoes")

for x,y,name,elev in zip(volcanoX, volcanoY, volcanoName, volcanoElevation):
    iframe = folium.IFrame(html= html % (name, name, name, str(elev)), width=200, height=100)
#Option 1: CircleMarkers
    fgv.add_child(folium.CircleMarker(location=[x,y], radius=5, popup=folium.Popup(iframe), weight=1, opacity=10.0, color="black",
                fill=True, fill_color=elev_color(elev), fill_opacity = .7))
#Option 2: Markers
#    map.add_child(folium.Marker(location=[x,y], popup=folium.Popup(iframe),
#    icon=folium.Icon(color=elev_color(elev), icon_color='white', icon='flag')))


#Population Feature Group
fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=(open("world.json", 'r', encoding='utf-8-sig').read()),
style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))


#Country Capitals Feature Group
fgc = folium.FeatureGroup(name="Country Capitals")
for x, y, name in zip(capitalX, capitalY, capitalName):
    fgc.add_child(folium.Marker(location=[x,y], popup=name, icon=folium.Icon(color='blue')))


#US National Parks
fgnp = folium.FeatureGroup(name="US National Parks")
for x, y, name in zip(nationalParkX, nationalParkY, nationalParkNames):
    fgnp.add_child(folium.Marker(location=[x,y], popup=name, icon=folium.Icon(color='green')))

#Add Feature Groups
map.add_child(fgp)
map.add_child(fgc)
map.add_child(fgv)
map.add_child(fgnp)
map.add_child(folium.LayerControl())
map.save("Map1.html")
