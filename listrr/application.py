from bricks import Bricks, Settings, wsgi, Route, BaseMC
from bricks.static_manager import StaticManager
from ceramic_forms import And
from common_components.db import PostgresThreadPool, DatabaseComponent
from listrr.logger import setup_logger
from listrr.components import Homepage, ListView, Api

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

api_route = Route('api', handler=Api)
routemap = Route('home', handler=Homepage) + {
    uuid_length: Route('list', handler=ListView),
    'api': api_route + {
        uuid_length: api_route
    }
}

class Main(BaseMC):
    depends_on = [routemap]

bricks = Bricks()

for c in components:
    bricks.add(c)

main = bricks.add(Main)
application = wsgi(main)
