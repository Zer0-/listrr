initialize_del_form = (form) ->
    jx_ok_callback = ->
        li_elem = form.closest 'li'
        li_elem.fadeOut 'normal', li_elem.remove
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

initialize_menu = (menu) ->
    toggle_elems = $ ".menu_item", menu
    bind_window = ->
        window_click = ->
            $(".menu_icon", menu).toggleClass "selected"
            toggle_elems.stop()
            toggle_elems.fadeToggle()
            $(window).unbind 'click', window_click
        $(window).click window_click

    $(".menu_icon", menu).click (e) ->
        toggle_elems.fadeToggle()
        $(@).toggleClass "selected"
        e.stopPropagation()
        bind_window()

$ ->
    forms = $ "form.new_item_form"
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
