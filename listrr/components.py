import logging
from bricks.render import mako_response, json_response
from bricks.staticfiles import StaticJs
from bricks.httpexceptions import HTTPBadRequest, HTTPNotFound
from common_components.static_renderers import Sass, SassLib, Coffee
from listrr.crud_api import ListApi, ItemNotFound

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
        self.status_fn_map = {
            'true': self.listapi.mark_done,
            'false': self.listapi.mark_undone
        }

    @json_response
    def POST(self, request, response):
        title = request.POST.get('title')
        if not title:
            raise HTTPBadRequest('No title data!')
        vars = request.route.vars
        if not vars:
            parent_id = self.root_id
        else:
            parent_id = vars[0]
        new_id, unmarked = self.listapi.add_list_item(parent_id, title)
        return (
            new_id,
            request.route.find('list', (new_id,)),
            request.route.find('api', (new_id,)),
            unmarked
        )

    def PUT(self, request, response):
        vars = request.route.vars
        title = request.POST.get('title')
        if not title or not vars:
            raise HTTPBadRequest('No title data!')
        self.listapi.update_list_item_title(vars[0], title)
        response.text = "OK"

    @json_response
    def DELETE(self, request, response):
        vars = request.route.vars
        if not vars:
            return HTTPNotFound()
        list_id = vars[0]
        try:
            return self.listapi.remove_list_item(list_id)
        except ItemNotFound:
            return HTTPNotFound()

    @json_response
    def PATCH(self, request, response):
        vars = request.route.vars
        if not vars:
            raise HTTPNotFound()
        list_id = vars[0]
        status_request = request.POST.get('status')#Yes POST is correct
        if status_request not in self.status_fn_map:
            raise HTTPBadRequest('status must be one of true, false')
        try:
            return self.status_fn_map[status_request](list_id)
        except ValueError:
            raise HTTPBadRequest('List item depends on children')
