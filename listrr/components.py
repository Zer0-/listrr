import logging
from bricks.render import mako_response
from bricks.staticfiles import StaticJs
from bricks.httpexceptions import HTTPBadRequest, HTTPNotFound
from common_components.static_renderers import Sass, SassLib, Coffee
from listrr.crud_api import ListApi

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

class ListView:
    depends_on = [ListApi]

    def __init__(self, listapi):
        self.listapi = listapi

    @mako_response('listrr:templates/list.mako')
    def GET(self, request, response):
        #WARNING TODO: make sure list_id is not root_id!
        list_id = request.route.vars[0]
        list = self.listapi.get_list_tree(list_id)
        if list is None:
            raise HTTPNotFound()
        return {}

class ApiNewItem:
    depends_on = [ListApi]

    def __init__(self, listapi):
        self.listapi = listapi
        rootnode = listapi.get_root_node()
        if rootnode is None:
            logging.info("Creating root list node www")
            self.root_id = listapi.create_root_node()
        else:
            self.root_id = rootnode[0]

    def POST(self, request, response):
        url = '/' + '/'.join(request.route.find('list', (self.root_id,)))
        response.text = url
        return
        title = request.POST.get('title')
        if not title:
            raise HTTPBadRequest('No title data!')
        vars = request.route.vars
        if not vars:
            parent_id = self.root_id
        else:
            parent_id = vars[0]
        new_id = self.listapi.add_list_item(parent_id, title)
        response.text = new_id
