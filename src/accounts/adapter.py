# adapter.py
from allauth.account.adapter import DefaultAccountAdapter
from .models import MelimitUser, MelimitStore

class MelimitAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        # ログイン後のリダイレクト先をユーザーモデルによって変更する
        if isinstance(request.user, MelimitUser):
            return "/path/for/melimituser"
        elif isinstance(request.user, MelimitStore):
            return "/path/for/melimitstore"