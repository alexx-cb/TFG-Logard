class JWTAuthCookieMiddleware:
    """
    Middleware para extraer el token JWT de la cookie 'access_token'
    y ponerlo en el header Authorization para que lo reconozca DRF.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('access_token')  # nombre de la cookie que usas
        if token and 'HTTP_AUTHORIZATION' not in request.META:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        response = self.get_response(request)
        return response