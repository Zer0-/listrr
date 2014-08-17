from bricks.render import mako_response
from bricks.staticfiles import StaticJs
from common_components.static_renderers import Sass, SassLib, Coffee

class Homepage:
    requires_configured = ['static_manager']
    depends_on = [
        Sass('homepage_style', asset='listrr:static/scss/home.scss'),
        SassLib('common_scss', asset='listrr:static/scss/common'),
        StaticJs('jquery',     asset='listrr:static/js/jquery.js'),
        Coffee('form_watcher', asset='listrr:static/coffee/form_watcher.coffee'),
        Coffee('ajax_forms',   asset='listrr:static/coffee/ajax_forms.coffee'),
        Coffee('home_coffee',  asset='listrr:static/coffee/home.coffee'),
    ]

    def __init__(self, static_manager, *static):
        self.static_manager = static_manager

    @mako_response('listrr:templates/home.mako')
    def GET(self, request, response):
        return {}
