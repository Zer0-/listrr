initialize_form = (form) ->
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
        initialize_form new_form
    submit_callback = (title) ->
        new_li_title = title
    init_miniform form, ajax_callback, submit_callback

$ ->
    forms = $ "form.new_item_form"
    forms.each ->
        form = $ @
        initialize_form form
