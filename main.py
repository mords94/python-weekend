from fastapi import Depends, FastAPI
from Database import Database
from JourneyRepository import JourneyRepository
from Options import Options
from Redis import RedisClient
from Routes import Routes
from Scraper import Scraper

# options = OptionParser().parse()
journeyRepository = JourneyRepository(database=Database())
redis = RedisClient("localhost")
app = FastAPI()


@app.get("/search")
def search(options: Options = Depends()):
    routes: Routes = Scraper(journeyRepository, redis, options).get_routes()

    return routes.dump()
