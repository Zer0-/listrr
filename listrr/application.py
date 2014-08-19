from bricks import Settings, app_from_routemap, Route
from bricks.staticfiles import StaticManager
from ceramic_forms import And
from common_components.db import PostgresThreadPool, DatabaseComponent
from listrr.logger import setup_logger

settings = Settings()
setup_logger(settings['logfile_path'])

components = (
    Settings,
    StaticManager,
    PostgresThreadPool,
    DatabaseComponent
)

def make_length_verifier():
    from listrr.listid import gen_list_uuid
    correct_length = len(gen_list_uuid(settings['list_uuid_size']))
    def lenverify(s):
        return len(s) == correct_length
    return lenverify

uuid_length = make_length_verifier()

from listrr.components import Homepage, ListView, Api
api_route = Route('api', handler=Api)
routemap = Route('home', handler=Homepage) + {
    uuid_length: Route('list', handler=ListView),
    'api': api_route + {
        uuid_length: api_route
    }
}

application = app_from_routemap(routemap, components=components)
