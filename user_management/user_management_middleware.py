import time
from django.utils.deprecation import MiddlewareMixin


class TimeStats(MiddlewareMixin):
    """
    middleware to record request to response time duration for each api call
    """
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        time_duration = time.time() - request.start_time

        response['X-Page-Generation-Duration-ms'] = int(time_duration * 1000)
        return response



