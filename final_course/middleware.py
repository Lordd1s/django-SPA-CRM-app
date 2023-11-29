import logging
import time


class CustomCORSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"
        return response


logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()

        # Логируем информацию о запросе
        logger.info(
            f"\n\nMethod: {request.method}, \n"
            f"Path: {request.path}, \n"
            f"Status Code: {response.status_code}, \n"
            f"Time taken: {end_time - start_time:.2f}s\n"
            f"IP: {request.META['REMOTE_ADDR']}\n"
            f"when: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        )

        return response
