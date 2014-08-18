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

rebind_button = (disable, enable, disable_all, form_elem, title_input, success_callback) ->
    disable()
    bind_form_submit form_elem, disable_all, success_callback
    validator = create_validator title_input
    watch_changes form_elem, validator, enable, disable

bind_form_btn = (form_elem, success_callback) ->
    main_button = $ 'button[type=submit]', form_elem
    main_button.removeAttr 'disabled'
    title_input = $ 'input[name=title]', form_elem
    reset_button = $ 'button[type=reset]', form_elem
    disable = ->
        main_button.attr 'disabled', 'disabled'
    disable_all = ->
        title_input.unbind()
        disable()
    enable = ->
        main_button.removeAttr 'disabled'
    main_button.click ->
        main_button.unbind()
        rebind_button disable, enable, disable_all, form_elem, title_input, success_callback
        title_input.show()
        reset_button.show()
        return false
    reset_button.click ->
        title_input.unbind()
        title_input.hide()
        enable()
        reset_button.hide()
        bind_form_btn form_elem, success_callback

window.bind_form_btn = bind_form_btn
