#TODO FIX DELETING CLEANUP
initialize_del_form = (form) ->
    jx_ok_callback = ->
        li_elem = form.closest 'li'
        remelem = li_elem

        #determine if entire list needs to be removed too
        ul = li_elem.closest 'ul'
        children = ul.children 'li'
        if children.length <= 2 and ul[0] != $('body>ul')[0]
            remelem = ul
        remelem.fadeOut 'normal', ->
            remelem.remove()
    response_handlers =
        load: (evt) ->
            xhr = @
            status = xhr.status
            response = xhr.response
            if status == 200
                jx_ok_callback()
            else
                console.log "Server Replied with an error (#{status}):"
                console.log response
        error: (evt) ->
            console.log "an error has occurred while deleting an item"
            console.log @
            console.log evt
    form.submit (e) ->
        e.preventDefault()
        send_form form, response_handlers
        $("button[type=submit]", form).attr "disabled", "disabled"

initialize_li_form = (form) ->
    console.log 'initting form'
    form_action = form.attr 'action'
    new_li_title = undefined
    ajax_callback = (newitem_url) ->
        data =
            content: new_li_title
        li = form.parent()
        form.replaceWith from_template 'list_item', data
        data =
            action: form_action
        new_elem = from_template 'li_form', data
        li.after new_elem
        new_form = $ 'form', new_elem
        initialize_li_form new_form
    submit_callback = (title) ->
        new_li_title = title
    init_miniform form, ajax_callback, submit_callback

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

initialize_menu = (menu) ->
    toggle_elems = $ ".menu_item", menu
    btn_menu = $(".menu_icon", menu)
    enable = false
    window_click = (e) ->
        if not enable
            enable = true
            return
        if not many_hit toggle_elems, e
            toggle_elems.stop()
            toggle_elems.fadeToggle 'fast'
            btn_menu.toggleClass 'selected'
            $(window).unbind 'click', window_click
            initialize_menu menu

    btn_menu.click (e) ->
        btn_menu.toggleClass 'selected'
        toggle_elems.stop()
        toggle_elems.fadeToggle()
        $(window).click window_click
        btn_menu.unbind()

$ ->
    forms = $ "ul form.new_item_form"
    forms.each ->
        form = $ @
        initialize_li_form form

    forms = $ "form.del_item_form"
    forms.each ->
        form = $ @
        initialize_del_form form

    $("li .menu").each ->
        menu = $ @
        initialize_menu menu
