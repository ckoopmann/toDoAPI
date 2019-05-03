# helloworld.py
import json
from nameko.rpc import rpc
from nameko.web.handlers import http

class GreetingService(object):
    name = "greeting_service"

    @http('GET','/<string:toGreet>')
    def hello(self, request, toGreet):
        return json.dumps({'greeting': "Hello, {}!".format(toGreet)})
