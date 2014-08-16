from listrr.application import application
import logging

def main():
    from wsgiref.simple_server import make_server
    from bricks import Settings
    settings = Settings()
    app = application
    debug = settings['debug']
    if debug:
        from werkzeug.debug import DebuggedApplication
        app = DebuggedApplication(application, evalex=True)
    port = settings['port']
    logging.info("Serving on port %s" % port)
    make_server('', port, app).serve_forever()

if __name__ == "__main__":
    main()

