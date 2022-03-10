from datetime import datetime, timedelta
from sqlalchemy import cast, Date
from sqlalchemy.orm.session import Session
from Database import Database
from Models import Journey
from Options import Options
from Route import Route
from sqlalchemy.orm import aliased


class JourneyRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    def truncate(self):
        with Session(self.database.engine) as session:
            session.execute('TRUNCATE TABLE journeys_dravaib')
            session.commit()

    def create(self, route: Route):
        with Session(self.database.engine) as session:
            session.add(Journey(
                source=route.source, destination=route.destination,
                departure_datetime=route.departure_datetime,
                arrival_datetime=route.arrival_datetime,
                carrier=route.carrier, vehicle_type=route.type,
                price=route.fare.amount, currency=route.fare.currency
            )
            )
            session.commit()

    def all(self):
        with Session(self.database.engine) as session:
            return session.query(Journey).all()

    def find_by_route(self, journey: Route):
        with Session(self.database.engine) as session:
            return session.query(Journey).filter(
                Journey.arrival_datetime == journey.arrival_datetime and
                Journey.departure_datetime == journey.departure_datetime and
                Journey.source == journey.source and
                Journey.destination == journey.destination and
                Journey.currency == journey.fare.currency and
                Journey.price == journey.fare.amount
            ).first()

    def find_by_options(self, options: Options):
        with Session(self.database.engine) as session:
            return session.query(Journey).filter(
                Journey.source == options.source,
                Journey.destination == options.destination,
                cast(Journey.departure_datetime, Date) == options.departure()
            ).first()

    def find_all_by_options(self, options: Options):
        after_day = options.departure() + timedelta(days=1)

        with Session(self.database.engine) as session:
            return session.query(Journey).filter(
                Journey.source == options.source,
                Journey.destination == options.destination,
                cast(Journey.departure_datetime, Date) == options.departure()
            ).all()

    def find_all_combinations(self, options: Options):
        leg1 = aliased(Journey, name="leg1")
        leg2 = aliased(Journey, name="leg2")
        with Session(self.database.engine) as session:
            return session.query(
                leg1, leg2
            ).join(
                leg2,
                leg1.destination == leg2.source
            ).filter(leg1.source == options.source and leg2.desination == options.destination).all()
