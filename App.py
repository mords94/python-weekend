import json
from typing import Any, List
from JourneyRepository import JourneyRepository
from Models import Journey
from Options import Options
from Redis import RedisClient
from Route import Route
from Routes import Routes, RoutesFactory
from Scraper import Scraper
from slugify import slugify


class App:
    locations: dict[str, Any] = {}
    rates: dict[str, float] = {}
    toLocationId: int
    fromLocationId: int
    redis: RedisClient
    journeyRepository: JourneyRepository

    def __init__(self, journeyRepository: JourneyRepository, redis: RedisClient):
        self.redis = redis
        self.journeyRepository = journeyRepository

    def get_journey_key(self):
        return 'dravai:journey:'+"_".join([slugify(self.options.source), slugify(self.options.destination), slugify(self.options.departure_date), slugify(self.options.currency)])

    def persist(self, routes: Routes):
        for route in routes.routes:
            journey = self.journeyRepository.find_by_route(route)
            if(journey is None):
                self.journeyRepository.create(route)

    def set_options(self, options: Options):
        self.options = options
        self.scraper = Scraper(self.journeyRepository, self.redis, options)

    def get_routes(self):
        routes = self.redis.get(self.get_journey_key())

        if(routes is not None):
            print("From redis")
            routes = Routes(Route.schema().loads(
                json.loads(routes), many=True))

            return routes

        journeys: List[Journey] = self.journeyRepository.find_all_by_options(
            self.options)

        if(len(journeys) > 0):
            print("FROM DATABASE....")
            routes = RoutesFactory.from_journeys(journeys)
        else:
            print("Scraping...")
            routes = self.scraper.scrape()
            self.persist(routes)

        self.redis.set(self.get_journey_key(), str(routes))

        return routes

    def search(self):
        routes: Routes = self.get_routes()
        return routes
        # for route in routes:
