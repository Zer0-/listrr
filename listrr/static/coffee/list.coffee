$ ->
    forms = $ "form.new_item_form"
    forms.each ->
        form = $ @
        form_action = form.attr 'action'
        new_li_title = undefined
        ajax_callback = (newitem_url) ->
            data =
                content: new_li_title
            form.replaceWith from_template 'list_item', data
        submit_callback = (title) ->
            new_li_title = title
        init_miniform form, ajax_callback, submit_callback
