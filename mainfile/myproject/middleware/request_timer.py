import time
import logging
logger = logging.getLogger("api")

class RequestTimerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logger.info("Run server")

    def __call__(self, request):
        logger.info('Got request')
        start_time = time.time()
        response  = self.get_response(request)
        logger.info('Sending response')
        delay = time.time() - start_time
        logger.info(f'Delay {delay}')
        return response