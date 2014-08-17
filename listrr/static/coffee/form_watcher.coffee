#jquery selectors
USER_MODIFIABLE_INPUTS = [
    'input:not([type=submit], [type=reset], [type=hidden])',
    'select',
    'textarea'
]

hamming_distance = (array1, array2) ->
    distance = 0
    for elem, i in array1
        if elem != array2[i]
            ++distance
    return distance

field_values = (fields) ->
    return ($(field).val() for field in fields)

#calls validator if all fields returned by required_fields selectors have been changed
#if the form has changed and the validator returns true call enable()
#if the form is reverted to its default state call disable()
#required_fields is one of 'any', 'all' or an array of jquery selectors
#fields := (undefined | 'any') ==> "any one fields is sufficient"
#fields := 'all' ==> all inputs must be changed to fire dirty callback
#fields := ['selector', ...] ==> each and every field in $('selector', form)
#   must have been changed to fire dirty callback
watch_changes = (form, validator, enable, disable, required_fields) ->
    if required_fields == 'all' or required_fields == 'any' or required_fields is undefined
        selectors = USER_MODIFIABLE_INPUTS
    else
        selectors = required_fields
    form_fields = $(selectors.join(', '), form)
    init_state = ($(field).prop('defaultValue') for field in form_fields)
    if required_fields == 'all'
        required_distance = form_fields.length
    else if required_fields == 'any' or required_fields is undefined
        required_distance = 1
    disabled = true
    check_and_fire = ->
        distance = hamming_distance init_state, field_values form_fields
        form_changed = distance >= required_distance
        if validator() and form_changed
            if disabled
                enable()
                disabled = false
        else if not disabled
            disable()
            disabled = true
    form_fields.bind 'input change', ->
        check_and_fire()
    check_and_fire()

window.watch_changes = watch_changes
