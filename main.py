from fastapi import Depends, FastAPI
from Database import Database
from JourneyRepository import JourneyRepository
from Options import Options
from Redis import RedisClient
from Routes import Routes
from App import App

# options = OptionParser().parse()
journeyRepository = JourneyRepository(database=Database())
redis = RedisClient("localhost")
app = FastAPI()

journeyApp = App(journeyRepository, redis)


@app.get("/search")
def search(options: Options = Depends()):
    journeyApp.set_options(options)
    routes: Routes = journeyApp.search()

    return routes.dump()
