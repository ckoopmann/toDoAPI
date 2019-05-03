# helloworld.py
import json
from nameko.rpc import rpc
from nameko.web.handlers import http

class GreetingService(object):
    name = "greeting_service"


    @rpc
    def hello(self,toGreet):
        return json.dumps({'greeting': "Hello, {}!".format(toGreet)})

    @http('GET','/<string:toGreet>')
    def helloHttp(self, request, toGreet):
        return json.dumps({'greeting': "Hello, {}!".format(toGreet)})   
