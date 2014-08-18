
$ ->
    forms = $ "form.new_item_form"
    forms.each ->
        form = $ @
        bind_form_btn form, (newitem_url) ->
            console.log newitem_url
            console.log 'success!'
