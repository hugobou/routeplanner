import Application as app


app = app.application_creator("/home/hugo/PycharmProjects/routeplanner/proto/madrid.gml",
                              "/home/hugo/PycharmProjects/routeplanner/test/model_params")

origin_point = (-3.6121729, 40.4224813)
destination_point = (-3.7090030, 40.4538682)

route, valid = app.get_route(origin_point, destination_point)

print(route)
print(valid)

