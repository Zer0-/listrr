#tools for dealing with form clientside.
#send_form lets you submit a form via xhr, file et all and handle any events
#
#form_watch_changes tells you as soon as form has changed so
#it's safe to validate/submit
#
#needs not jquery

#method to convert bytes to a human readable string
pretty_bytes = (bytes) ->
    s = ["bytes", "kB", "MB", "GB", "TB", "PB"]
    e = Math.floor Math.log(bytes) / Math.log(1024)
    return Math.round(bytes / Math.pow(1024, e)) + " " + s[e]

window.pretty_bytes = pretty_bytes

xhr_from_form = (form_elem) ->
    url = form_elem.attr 'action'
    url = url or ''
    method = form_elem.attr 'method'
    method = method or 'GET'
    xhr = new XMLHttpRequest()
    xhr.open method, url
    return xhr

attach_xhr_handlers = (xhr, handler_map) ->
    #supported: progress, load, error, abort, loadend
    for event_name, handler of handler_map
        xhr.addEventListener event_name, handler, false

attach_xhr_upload_handlers = (xhr, handler_map) ->
    attach_xhr_handlers xhr.upload, handler_map

stats_clojure = (event_handler) ->
#wraps given event_handler function in something that passes it:
#   completion [0, 1] , rate (bytes/s)
#wrapped fn accpets a progress event
    last_time = new Date().getTime() #in ms
    dt = 1 #in ms
    lastloaded = 0
    dloaded = 0 #bytes loaded since last called
    rate = 0 #bytes / second
    return (evt) ->
        dloaded = event.loaded - lastloaded
        lastloaded = event.loaded
        now = new Date().getTime()
        dt = now - last_time
        last_time = now
        rate = dloaded / (dt / 1000)
        event_handler (event.loaded / event.total), rate

window.stats_clojure = stats_clojure

send_form = (form_elem, load_handlers, upload_handlers) ->
    xhr = xhr_from_form form_elem
    attach_xhr_handlers xhr, load_handlers
    attach_xhr_upload_handlers xhr, upload_handlers
    xhr.send new FormData form_elem[0]#array thing because form_elem is assumed to be a jquery elem

window.send_form = send_form
