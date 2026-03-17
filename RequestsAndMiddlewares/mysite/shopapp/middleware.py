import time
from django.core.cache import cache
from django.http import HttpResponseForbidden


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_ip(request)
        key = f"throttling{ip}"

        requests = cache.get(key, [])
        current_time = time.time()
        last_time = [t for t in requests if current_time -t < 60]

        if len(last_time) == 5:
            return HttpResponseForbidden('You have been throttled')

        requests.append(current_time)
        cache.set(key, requests, 100)

        response = self.get_response(request)
        return response


    def get_ip(self,request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')