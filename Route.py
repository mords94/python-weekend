from ast import List
from calendar import c
from dataclasses import dataclass, field
from datetime import datetime
from Models import Journey
from Options import Options
from marshmallow import fields

from Rate import Rate
from dataclasses_json import config, dataclass_json


class RouteFactory:

    @staticmethod
    def create(route: dict, options: Options, rates: dict[str, int]):
        amount = route['priceFrom']/rates[options.currency]
        return Route(
            source=options.source,
            destination=options.destination,
            arrival_datetime=datetime.fromisoformat(route['arrivalTime']),
            departure_datetime=datetime.fromisoformat(route['departureTime']),
            type=route['vehicleTypes'][0].lower(),
            fare=Rate(amount=amount, currency=options.currency),
            carrier="REGIOJET"
        )

    @staticmethod
    def create_from_journey(journey: Journey):
        fare = Rate(amount=journey.price, currency=journey.currency)

        return Route(
            source=journey.source,
            destination=journey.destination,
            arrival_datetime=journey.arrival_datetime,
            departure_datetime=journey.departure_datetime,
            type=journey.vehicle_type,
            fare=fare,
            carrier=journey.carrier
        )


@dataclass_json
@dataclass
class Route:
    source: str
    destination: str
    arrival_datetime: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )
    departure_datetime: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )
    type: str
    fare: Rate
    carrier: str
