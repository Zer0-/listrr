
$ ->
    forms = $ "form.new_item_form"
    forms.each ->
        form = $ @
        init_miniform form, (newitem_url) ->
            console.log newitem_url
            console.log 'success!'
