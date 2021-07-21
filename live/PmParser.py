import xml.etree.ElementTree as ET
import utm

SERVICE_DEFAULT = 0


def utm2latlon(x, y):
    return utm.to_latlon(x, y, 30, 'T')


class TrafficMeasurement:
    def __init__(self, description, x, y, serv_level):
        self.description = description
        self.y, self.x = utm2latlon(float(x.replace(",", ".")), float(y.replace(",", ".")))
        self.serv_level = int(serv_level) if serv_level is not None and serv_level != "Error" else SERVICE_DEFAULT

    def __str__(self):
        return "%s (%f, %f): %d" % (self.description, self.x, self.y, self.serv_level)

    def isvalid(self):
        if self.description is None or self.x is None or self.y is None or self.serv_level is None:
            return False
        else:
            return True


def parse_traffic_data(filename, debug=False):
    root_node = ET.parse(filename).getroot()
    tmList = []
    for tag in root_node.findall('pm'):
        tag_desc = tag.find('descripcion').text if tag.find('descripcion') != None else None
        tag_x = tag.find('st_x').text if tag.find('st_x') != None else None
        tag_y = tag.find('st_y').text if tag.find('st_y') != None else None
        tag_serv = tag.find('nivelServicio').text if tag.find('nivelServicio') != None else None
        tm = TrafficMeasurement(tag_desc, tag_x, tag_y, tag_serv)
        if tm.isvalid():
            tmList.append(tm)
            if debug:
                print(tm)
    return tmList

parse_traffic_data('pm.xml', debug=True)
