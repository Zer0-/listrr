bind_initial_btn_submit = (elems, jx_ok_callback, submit_callback) ->
    elems.btn_submit.removeAttr 'disabled'
    elems.btn_submit.click (e) ->
        e.preventDefault()
        form_setup elems, jx_ok_callback, submit_callback
        elems.btn_submit.unbind()
        elems.btn_submit.attr 'type', 'submit'

reset_form = (elems, jx_ok_callback, submit_callback) ->
    #recreated animated elements
    play = $ '.js_animated', elems.form
    play.removeClass 'play'
    play.each ->
        elem = $ @
        clone = elem.clone()
        for name, value of elems
            if value[0] == elem[0]
                elems[name] = clone
                break
        elem.replaceWith clone
    bind_initial_btn_submit elems, jx_ok_callback, submit_callback

bind_btn_reset = (elems, jx_ok_callback, submit_callback) ->
    elems.btn_reset.click ->
        form_teardown elems
        reset_form elems, jx_ok_callback, submit_callback

form_setup = (elems, jx_ok_callback, submit_callback) ->
    disable = ->
        elems.btn_submit.attr 'disabled', 'disabled'
    enable = ->
        elems.btn_submit.removeAttr 'disabled'
    disable()
    elems.txt_input.show()
    elems.btn_reset.show()
    play = $ '.js_animated', elems.form
    play.addClass 'play'
    bind_btn_reset elems, jx_ok_callback, submit_callback
    bind_form_submit elems, jx_ok_callback, submit_callback
    validator = ->
        title = elems.txt_input.val()
        return title.length
    watch_changes elems.form, validator, enable, disable

form_teardown = (elems) ->
    elems.txt_input.unbind()
    elems.btn_reset.unbind()
    elems.btn_submit.removeAttr 'disabled'
    elems.btn_submit.removeAttr 'type'
    elems.form.unbind()
    elems.txt_input.hide()
    elems.btn_reset.hide()

bind_form_submit = (elems, jx_ok_callback, submit_callback) ->
    response_handlers =
        load: (evt) ->
            xhr = @
            status = xhr.status
            response = xhr.response
            if status == 200
                jx_ok_callback xhr.response
            else
                console.log "Server Replied with an error (#{status}):"
                console.log response
        error: (evt) ->
            console.log "an error has occurred while uploading form:"
            console.log response
    form = elems.form
    form.submit (e) ->
        e.preventDefault()
        send_form form, response_handlers
        if submit_callback?
            submit_callback elems.txt_input.val()
        form_teardown elems
        reset_form elems, jx_ok_callback, submit_callback
        elems.txt_input.val ''

init_miniform = (form, jx_ok_callback, submit_callback) ->
    elems =
        form: form
        btn_submit: $ 'button[disabled]', form
        txt_input: $ 'input[type=text]', form
        btn_reset: $ 'button[type=reset]', form

    bind_initial_btn_submit elems, jx_ok_callback, submit_callback
    return elems

window.init_miniform = init_miniform
