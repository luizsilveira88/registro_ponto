from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Admin
        if request.path.startswith("/admin/"):
            return None

        match = request.resolver_match
        url_name = match.view_name if match else None

        # Páginas públicas
        if url_name in settings.PUBLIC_URL_NAMES:
            return None

        # Usuário não autenticado
        if not request.user.is_authenticated:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(
                    {"result": "error", "msg": "Sessão expirada"}, status=401
                )
            return redirect(settings.LOGIN_URL)

        # Usuário autenticado tentando acessar login
        if request.path == settings.LOGIN_URL:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return None
