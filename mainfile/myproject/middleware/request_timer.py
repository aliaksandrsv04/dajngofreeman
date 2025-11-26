import time


class RequestTimerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("Run server")

    def __call__(self, request):
        print('Got request')
        start_time = time.time()
        response  = self.get_response(request)
        print('Sending response')
        delay = time.time() - start_time
        print(f'Delay {delay}')
        return response