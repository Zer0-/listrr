from bricks.render import mako_response
from common_components.static_renderers import Sass, SassLib

class Homepage:
    requires_configured = ['static_manager']
    depends_on = [
        Sass('homepage_style', asset='listrr:static/scss/home.scss'),
        SassLib('common_scss', asset='listrr:static/scss/common')
    ]

    def __init__(self, static_manager, *static):
        self.static_manager = static_manager

    @mako_response('listrr:templates/home.mako')
    def GET(self, request, response):
        return {}
