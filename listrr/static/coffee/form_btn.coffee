create_validator = (title_input) ->
    return ->
        title = title_input.val()
        return title.length

bind_form_submit = (form, disable, success_callback) ->
    response_handlers =
        load: (evt) ->
            xhr = @
            status = xhr.status
            response = xhr.response
            if status == 200
                success_callback xhr.response
            else
                console.log "Server Replied with an error (#{status}):"
                console.log response
        error: (evt) ->
            console.log "an error has occurred while uploading form:"
            console.log response
    form.submit (e) ->
        e.preventDefault()
        send_form form, response_handlers
        disable()

rebind_button = (btn, title_input, success_callback) ->
    disable = ->
        btn.attr 'disabled', 'disabled'
        btn.unbind()
    disable()
    form = $ 'form'
    disable_all = ->
        title_input.unbind()
        disable()
    bind_form_submit form, disable_all, success_callback
    enable = ->
        btn.removeAttr 'disabled'
    title_input.show()
    validator = create_validator title_input
    watch_changes form, validator, enable, disable

bind_form_btn = (formelem, success_callback) ->
    main_button = $ 'button[type=submit]', formelem
    main_button.removeAttr 'disabled'
    title_input = $ 'input[name=title]', formelem
    main_button.click ->
        rebind_button main_button, title_input, success_callback
        return false

window.bind_form_btn = bind_form_btn
