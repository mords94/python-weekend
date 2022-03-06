import json
from typing import List, Tuple
from Models import Journey
from Route import Route, RouteFactory


class RoutesFactory:

    @staticmethod
    def from_journeys(journeys: List[Journey]):
        return Routes(list(map(RouteFactory.create_from_journey, journeys)))


class Routes:
    def __init__(self, routes: List[Route]):
        self.routes = routes

    def __str__(self):
        return json.dumps(self.dump())

    def print(self):
        print(str(self))

    def dump(self):
        return Route.schema().dump(self.routes, many=True)

    def json(self):
        return json.dumps(Route.schema().dump(self.routes, many=True))
