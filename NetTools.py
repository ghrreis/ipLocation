from icmplib import traceroute
import ipaddr
from urllib.request import urlopen
from json import load
import folium
from folium.features import DivIcon


class tracert():

    __last_distance = 0
    __hops = ""
    __listIPs = []

    def __init__(self, target):

        self.__hops = traceroute(target)

        for hop in self.__hops:
            if self.__last_distance + 1 != hop.distance:
                print('Some gateways are not responding')
            if not ipaddr.IPv4Address(hop.address).is_private:
                # print(f'{hop.distance}   {hop.address}   {hop.avg_rtt}')
                self.__listIPs.append(hop.address)
            self.__last_distance = hop.distance


    def getListIPs(self):

        return self.__listIPs


class iplocation():

    __listLocations = []

    def __init__(self, listTarget):

        for target in listTarget:
            url = 'https://ipinfo.io/' + target + '/json'
            response = urlopen(url)
            data = load(response)
            for attr in data.keys():
                if attr == 'loc':
                    self.__listLocations.append(data[attr])

    def getLocations(self):

        return self.__listLocations


class maplocation():

    __index = 1
    __latitude = 0
    __longitude = 0
    __latitudeAux = 0
    __longitudeAux = 0

    def __init__(self, listLocations):

        #listLocations = [[-21.2747, -43.1792], [-21.2732088, -43.0433725], [-21.7289999, -43.5226092]]
        self.__latitude = float(str(listLocations[0]).split(",")[0])
        self.__longitude = float(str(listLocations[0]).split(",")[1])
        m = folium.Map(location=[self.__latitude, self.__longitude], zoom_start=3)

        for point in range(0, len(listLocations)):
            self.__latitude = float(str(listLocations[point]).split(",")[0])
            self.__longitude = float(str(listLocations[point]).split(",")[1])
            folium.Marker(location=[self.__latitude, self.__longitude], icon=DivIcon(
                icon_size=(150, 36),
                icon_anchor=(7, 20),
                html='<br><div style="font-size: 14pt; color : black">' + str(self.__index) + '</div>',
            )).add_to(m)
            # m.add_child(folium.CircleMarker(listLocations[point], radius=10))
            if point + 1 < len(listLocations):
                self.__latitudeAux = float(str(listLocations[point + 1]).split(",")[0])
                self.__longitudeAux = float(str(listLocations[point + 1]).split(",")[1])
                coordinates = [(self.__latitude, self.__longitude), (self.__latitudeAux, self.__longitudeAux)]
                aline = folium.PolyLine(locations=coordinates, weight=2, color='purple')
            m.add_child(aline)
            self.__index += 1

        m.save("index.html")
