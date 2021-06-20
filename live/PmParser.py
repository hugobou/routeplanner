import xml.etree.ElementTree as ET
import utm

def to_latlon(x, y):
    return utm.to_latlon(x, y, 30, 'T')

class TrafficMeasurement:
    def __init__(self, description, x, y, serv_level):
        self.desc = description
        self.y, self.x = to_latlon(float(x.replace(",",".")), float(y.replace(",",".")))
        self.serv_level = int(serv_level)

    def __str__(self):
        return "%s (%f, %f): %d" % (self.desc, self.x, self.y, self.serv_level)

    def isValid(self):
        if self.description == None or self.x == None or self.y == None or self.serv_level == None:
            return False
        else:
            return True
 
# We're at the root node (<page>)
root_node = ET.parse('pm.xml').getroot()
 
# We need to go one level below to get <header>
# and then one more level from that to go to <type>

tmList = []

for tag in root_node.findall('pm'):
    tag_desc = tag.find('descripcion').text if tag.find('descripcion') != None else None
    tag_x = tag.find('st_x').text if tag.find('st_x') != None else None
    tag_y = tag.find('st_y').text if tag.find('st_y') != None else None
    tag_serv = tag.find('nivelServicio').text if tag.find('nivelServicio') != None else None
    tm = TrafficMeasurement(tag_desc, tag_x, tag_y, tag_serv)
    if tm.isValid():
        tmList.append(tm)
        print(tm)