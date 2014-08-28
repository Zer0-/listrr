mark = (elem) ->
    elem.addClass 'done'

unmark = (elem) ->
    elem.removeClass 'done'

hit_detection = (x, y, tx, ty, width, height) ->
    if tx <= x <= (tx + width)
        if ty <= y <= (ty + height)
            return true
    return false

many_hit = (elems, e) ->
    x = e.pageX
    y = e.pageY
    for elem in elems
        elem = $ elem
        target = elem.offset()
        if hit_detection x, y, target.left, target.top, elem.width(), elem.height()
            return true
    return false

attach_toggle = (btn_elem, fn_on, fn_off) ->
    #fn_on must return things that will be displayed, we need to do
    #hit detection on them!
    enable = false
    toggle_elems = undefined
    window_click = (e) ->
        if not enable
            enable = true
            toggle_elems = fn_on()
            return
        if not many_hit toggle_elems, e
            enable = false
            $(window).unbind 'click', window_click
            fn_off()

    btn_elem.click (e) ->
        if enable
            return
        $(window).click window_click

hit_api = (url, method, payload, callback) ->
    jx_callback = ->
        xhr = @
        if xhr.status != 200
            console.log 'an error has occurred: '
            console.log xhr.response
            return
        callback xhr.response

    data = new FormData
    for key, value of payload
        data.append key, value

    xhr = new XMLHttpRequest()
    xhr.open method, url
    xhr.addEventListener 'load', jx_callback, false
    xhr.addEventListener 'error', jx_callback, false
    xhr.send data

get_list_children = (li) ->
    return $ 'li[id]', $ 'ul', li

list_children_all_complete = (li) ->
    done = true
    get_list_children(li).each ->
        child = $ @
        done = done and child.hasClass 'done'
    return done

mark_many = (id_list, status) ->
    if status
        fn = mark
    else
        fn = unmark
    for id in id_list
        fn $ '#' + id

bind_unmark = (li, menu, api_url) ->
    callback = (data) ->
        mark_many $.parseJSON(data), false
    $('.unmark', menu).click ->
        unmark li
        hit_api api_url, 'PATCH', {status: false}, callback

bind_mark = (li, api_url) ->
    callback = (data) ->
        mark_many $.parseJSON(data), true
    $('.btn_mark:eq(0)', li).click ->
        mark li
        hit_api api_url, 'PATCH', {status: true}, callback

bind_del = (li, menu, api_url) ->
    callback = (data) ->
        mark_many $.parseJSON(data), true
        list_container = li.closest 'ul'
        children = $ 'li[id]', list_container
        if children.length == 1
            list_container.fadeOut 'fast', ->
                list_container.remove()
            list_container.parent().addClass 'leaf'
        li.fadeOut 'fast', ->
            li.remove()
    $('.delete', menu).click ->
        hit_api api_url, 'DELETE', {}, callback
        $(@).unbind()

bind_sublist_miniform_cancel = (li, sublist, form_elems) ->
    form_elems.btn_reset.click ->
        sublist.fadeOut 'fast', ->
            sublist.remove()
            li.addClass 'leaf'

bind_add_sublist = (li, menu, api_url) ->
    $('.sublist', menu).click ->
        template_data =
            action: api_url
        sublist = from_template 'list', template_data
        li.append sublist
        li.removeClass 'leaf'
        form_container = $ '.new_form_container', sublist
        form_elems = init_new_li_form form_container
        bind_sublist_miniform_cancel li, sublist, form_elems

create_item_menu = (li, api_url) ->
    item_url = li.data 'item_url'
    is_leaf = li.hasClass 'leaf'
    data =
        href: item_url
        unmark: is_leaf and li.hasClass('done')
        sublist: is_leaf
    menu = from_template 'menu_buttons', data
    bind_unmark li, menu, api_url
    bind_del li, menu, api_url
    bind_add_sublist li, menu, api_url
    return menu

init_menu_btn = (li, api_url) ->
    btn_elem = $ '.menu .menu_icon:eq(0)', li
    menu = undefined
    fn_on = ->
        menu = create_item_menu li, api_url
        menu.hide()
        btn_elem.after menu
        menu.fadeIn 'fast'
        btn_elem.addClass 'show'
        return menu

    fn_off = ->
        menu.fadeOut 'fast', ->
            menu.remove()
        btn_elem.removeClass 'show'

    attach_toggle btn_elem, fn_on, fn_off

init_new_li_form = (container) ->
    new_li_title = undefined
    jx_callback = (data) ->
        [item_id, item_url, item_api_url, items_unmarked] = $.parseJSON data
        template_data =
            id: item_id
            'data-item_url': item_url
            'data-api_url': item_api_url
            title: new_li_title
        new_li = from_template 'list_item', template_data
        init_list_item new_li
        container.before new_li
        mark_many items_unmarked, false
    submit_callback = (title) ->
        new_li_title = title

    form = $ 'form', container
    return init_miniform form, jx_callback, submit_callback

init_list_item = (li) ->
    api_url = li.data 'api_url'
    init_menu_btn li, api_url
    bind_mark li, api_url

$ ->
    $('li[id]').each ->
        init_list_item $ @

    $('main li.new_form_container').each ->
        init_new_li_form $ @
