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