from .bottle import ServerAdapter
import logging

logger = logging.getLogger('server')

FORMAT = '%(asctime)-15s - %(message)s'
logger = logging.getLogger('server')
logger.setLevel(logging.DEBUG)
formater = logging.Formatter(FORMAT)
ch = logging.StreamHandler()
ch.setFormatter(formater)
logger.addHandler(ch)

class TulipServer(ServerAdapter):
    def run(self, handler):
        import tulip
        from tulip.http import WSGIServerHttpProtocol
        def wsgi_app(env, start):
            def start_response(status_line, headerlist):
                status_code = status_line.split(' ', 1)[0]
                length = dict(headerlist).get('Content-Length', 0)
                logger.info('{} {} {} {}'.format(env['REQUEST_METHOD'], env['RAW_URI'], status_code, length))
                return start(status_line, headerlist)
            return handler(env, start_response)
        loop = tulip.get_event_loop()
        f = loop.start_serving(
                lambda: WSGIServerHttpProtocol(wsgi_app, loop = loop, readpayload=True),
                self.host, self.port)
        socks = loop.run_until_complete(f)
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
