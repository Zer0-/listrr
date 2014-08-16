from bricks import Settings, app_from_routemap, Route
from bricks.staticfiles import StaticManager
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

from listrr.components import Homepage
routemap = Route('home', handler=Homepage)

application = app_from_routemap(routemap, components=components)
