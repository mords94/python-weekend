import json
from typing import Any, List
import requests
from JourneyRepository import JourneyRepository
from Models import Journey
from Options import Options
from Redis import RedisClient
from Route import Route, RouteFactory
from Routes import Routes, RoutesFactory
from slugify import slugify

from config import LOCATIONS_URL, RATES_URL, ROUTE_URL


class Scraper:
    locations: dict[str, Any] = {}
    rates: dict[str, float] = {}
    toLocationId: int
    fromLocationId: int
    redis: RedisClient
    journeyRepository: JourneyRepository

    def __init__(self, journeyRepository, redis, options: Options):
        self.options = options
        self.redis = redis
        self.journeyRepository = journeyRepository

    def fetch_locations(self):
        self.locations = requests.get(LOCATIONS_URL).json()

    def fetch_rates(self):
        rates = self.redis.get(self.get_rates_key())
        if(rates is not None):
            self.rates = json.loads(rates)
            return

        rates = requests.get(RATES_URL).json()

        self.redis.set(self.get_rates_key(), rates)
        self.rates = rates
        self.toLocationId = None
        self.fromLocationId = None

    def get_rates_key(self):
        return 'dravai:rates'

    def get_journey_key(self):
        return 'dravai:journey:'+"_".join([slugify(self.options.source), slugify(self.options.destination), slugify(self.options.departure_date)])

    def get_location_key(self, location):
        return 'dravai:location:' + slugify(location)

    def find_city_ids(self):
        self.fromLocationId = self.redis.get(
            self.get_location_key(self.options.source))

        self.toLocationId = self.redis.get(
            self.get_location_key(self.options.destination))

        for country in self.locations:
            if self.fromLocationId is not None and self.toLocationId is not None:
                break
            for city in country['cities']:
                if(city['name'] == self.options.source):
                    self.fromLocationId = city['id']

                if(city['name'] == self.options.destination):
                    self.toLocationId = city['id']

    def find_routes(self):
        routes = self.redis.get(self.get_journey_key())

        if(routes is not None):
            print("From redis")
            routes = Routes(Route.schema().loads(
                json.loads(routes), many=True))

            self.persist(routes)
            return routes

        # journeys: List[Journey] = self.journeyRepository.find_all_by_options(
        #     self.options)

        # if(journeys is not None):
        #     print("FROM DATABASE....")
        #     return RoutesFactory.from_journeys(journeys)

        params = {"tariffs": "REGULAR", "toLocationType": "CITY", 'toLocationId': self.toLocationId,
                  'fromLocationType': 'CITY', "fromLocationId": self.fromLocationId, "departureDate": self.options.departure_date}

        routes_result = requests.get(ROUTE_URL, params, headers={
            'X-Currency': 'EUR'}).json()['routes']

        routes_list = list(map(lambda r: RouteFactory.create(
            r, self.options, self.rates), routes_result))

        routes = Routes(routes_list)

        self.redis.set(self.get_journey_key(), str(routes))
        self.persist(routes)
        return routes

    def persist(self, routes: Routes):
        for route in routes.routes:
            journey = self.journeyRepository.find_by_route(route)
            if(journey is None):
                self.journeyRepository.create(route)

    def get_routes(self):
        self.fetch_locations()
        self.fetch_rates()

        self.find_city_ids()

        return self.find_routes()
