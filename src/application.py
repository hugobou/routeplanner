import routeplanner as rp
import traffic as tf
import routeformatter as rf


class Application:
    def __init__(self, graph, pm_dict, model, feature_encoder):
        self.graph = graph
        self.pm_dict = pm_dict
        self.route_planner = rp.RoutePlanner(model, feature_encoder)

    def get_route(self, origin, destination):
        return self.route_planner.get_route_gps(self.graph, origin, destination)

    def get_formatted_route(self, origin, destination):
        route, valid = self.get_route(origin, destination)
        return rf.RouteFormatter().format(self.graph, route)

    def update_traffic_info(self, tm_list):
        tf.update_traffic_info(self.graph, tm_list, self.pm_dict)
