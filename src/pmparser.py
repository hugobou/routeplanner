import xml.etree.ElementTree as ET

from traffic import TrafficMeasurement


def parse_traffic_data(xml_string, debug=False):
    root_node = ET.ElementTree(ET.fromstring(xml_string)).getroot()

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


