# helloworld.py
import json
from nameko.rpc import RpcProxy
from nameko.web.handlers import http

class GreetingService(object):
    name = "http_greeting_service"

    greeting_service = RpcProxy("greeting_service")

    @http('GET','/<string:toGreet>')
    def helloHttp(self, request, toGreet):
        return self.greeting_service.hello(toGreet)
