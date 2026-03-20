from django.shortcuts import redirect

ROTAS_LIVRES = ['/verificacao/', '/static/', '/media/', '/admin/']

class VerificacaoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get('verificado'):
            for rota in ROTAS_LIVRES:
                if request.path.startswith(rota):
                    return self.get_response(request)
            return redirect('verificacao')
        return self.get_response(request)