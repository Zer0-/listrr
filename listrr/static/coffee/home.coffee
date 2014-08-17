create_validator = (title_input) ->
    return ->
        title = title_input.val()
        return title.length

rebind_button = (btn, title_input) ->
    btn.unbind()
    title_input.show()
    form = $ 'form'
    validator = create_validator title_input
    enable = ->
        btn.removeAttr 'disabled'
    disable = ->
        btn.attr 'disabled', 'disabled'
    disable()
    watch_changes form, validator, enable, disable

$ ->
    main_button = $ '#main_button'
    main_button.removeAttr 'disabled'
    title_input = $ 'form input[name=title]'
    main_button.click ->
        rebind_button main_button, title_input
        return false
