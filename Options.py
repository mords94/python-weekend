import argparse
from typing import Optional
from pendulum import datetime
from pydantic import BaseModel
from datetime import datetime


class OptionParser:

    def parse(self):
        parser = argparse.ArgumentParser(
            description='Blah blah')
        parser.add_argument('source', metavar='from', type=str,
                            help='From city')
        parser.add_argument('destination', metavar='to', type=str,
                            help='To City')

        parser.add_argument('date', metavar='date', type=str,
                            help='Date of travel')

        parser.add_argument('--currency', type=str,
                            help='Curency',  default='EUR')

        try:
            return Options.from_dict(parser.parse_args().__dict__)
        except Exception as e:
            print("Argparser:", e)


class Options(BaseModel):
    source: str
    destination: str
    departure_date: str
    currency: Optional[str] = 'EUR'

    def departure(self):
        return datetime.fromisoformat(self.departure_date)
