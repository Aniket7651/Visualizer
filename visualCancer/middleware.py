

class CacheControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith('/static/'):
            response['Cache-Control'] = 'public, max-age=3600, must-revalidate'
            # response['Pragma'] = 'no-cache'
            # response['Expires'] = '0'
        return response 