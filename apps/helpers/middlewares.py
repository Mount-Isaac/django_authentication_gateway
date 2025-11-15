from django.db import models
from json import dumps
from uuid import uuid4
from .responses import log_request_response

class GenerateRequestsId:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request, **kwargs):
        '''A middleware that generates and appends a unique request id on every request made to the server'''
        
        # if request.path.startswith("/api/"):
        # Code to be executed for each request before
        request_id = str(uuid4())
        request.id = request_id

        request_body = request.body

        response = self.get_response(request) # return updated response object : with request_id
        
        # code to be executed for each requests/response after
        log_request_response(request_id, request_body, response)
        return response
        
        # return self.get_response(request)