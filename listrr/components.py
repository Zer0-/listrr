import logging
from bricks.render import mako_response, json_response
from bricks.staticfiles import StaticJs
from bricks.httpexceptions import HTTPBadRequest, HTTPNotFound
from common_components.static_renderers import Sass, SassLib, Coffee
from listrr.crud_api import ListApi

class FormBtn:
    depends_on = [
        StaticJs('jquery',     asset='listrr:static/js/jquery.js'),
        Coffee('form_watcher', asset='listrr:static/coffee/form_watcher.coffee'),
        Coffee('ajax_forms',   asset='listrr:static/coffee/ajax_forms.coffee'),
        Coffee('form_btn',  asset='listrr:static/coffee/form_btn.coffee'),
    ]
    def __init__(self, *args):
        pass

class Homepage:
    requires_configured = ['static_manager']
    depends_on = [
        SassLib('common_scss', asset='listrr:static/scss/common'),
        Sass('homepage_style', asset='listrr:static/scss/home.scss'),
        FormBtn,
    ]

    def __init__(self, static_manager, *static):
        self.static_manager = static_manager

    @mako_response('listrr:templates/home.mako')
    def GET(self, request, response):
        return {}

class ListView:
    requires_configured = ['static_manager']
    depends_on = [
        ListApi,
        SassLib('common_scss', asset='listrr:static/scss/common'),
        Sass('list_style', asset='listrr:static/scss/list.scss'),
        FormBtn,
        Coffee('skelly_js', asset='listrr:static/skelly.js/src/templates.coffee'),
        Coffee('list_coffee',  asset='listrr:static/coffee/list.coffee'),
    ]

    def __init__(self, static_manager, listapi, *static):
        self.static_manager = static_manager
        self.listapi = listapi

    @mako_response('listrr:templates/list.mako')
    def GET(self, request, response):
        list_id = request.route.vars[0]
        list_items = self.listapi.get_list_tree(list_id)
        if list_items is None:
            raise HTTPNotFound()
        head = list_items[0]
        tree = head.replies
        return {
            'head': head,
            'tree': tree
        }

class Api:
    depends_on = [ListApi]

    def __init__(self, listapi):
        self.listapi = listapi
        self.root_id = listapi.get_root_node()

    def POST(self, request, response):
        title = request.POST.get('title')
        if not title:
            raise HTTPBadRequest('No title data!')
        vars = request.route.vars
        if not vars:
            parent_id = self.root_id
        else:
            parent_id = vars[0]
        new_id = self.listapi.add_list_item(parent_id, title)
        response.text = request.route.find('list', (new_id,))

    def DELETE(self, request, response):
        list_id = request.route.vars[0]
        del_result = self.listapi.remove_list_item(list_id)
        if not del_result:
            return HTTPNotFound()
