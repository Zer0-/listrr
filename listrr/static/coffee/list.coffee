$ ->
    forms = $ "form.new_item_form"
    forms.each ->
        form = $ @
        bind_form_btn form, ->
            console.log 'success!'
