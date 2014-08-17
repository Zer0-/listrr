create_validator = (title_input) ->
    return ->
        title = title_input.val()
        return title.length

bind_form_submit = (form, disable) ->
    response_handlers =
        load: (evt) ->
            xhr = @
            status = xhr.status
            response = xhr.response
            if status == 200
                window.location = response
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

disable_watcher = (form) ->
    $("input", form).unbind()

rebind_button = (btn, title_input) ->
    disable = ->
        btn.attr 'disabled', 'disabled'
        btn.unbind()
    disable()
    form = $ 'form'
    disable_all = ->
        disable_watcher form
        disable()
    bind_form_submit form, disable_all
    enable = ->
        btn.removeAttr 'disabled'
    title_input.show()
    validator = create_validator title_input
    watch_changes form, validator, enable, disable

$ ->
    main_button = $ '#main_button'
    main_button.removeAttr 'disabled'
    title_input = $ 'form input[name=title]'
    main_button.click ->
        rebind_button main_button, title_input
        return false
