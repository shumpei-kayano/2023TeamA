# adapter.py
from allauth.account.adapter import DefaultAccountAdapter
from .models import CustomUser, MelimitUser, MelimitStore

class MelimitAccountAdapter(DefaultAccountAdapter):
    # def login(self, request, user):
    #     print('nextnextnext')
    #     # `next`パラメータを無視する
    #     request.session.pop('next', None)
    #     super().login(request, user)

    def get_login_redirect_url(self, request):
        # # ログイン後のリダイレクト先をユーザーモデルによって変更する
        # if isinstance(request.user, MelimitUser):
        #     # userアプリ内のtemplates/account/login.htmlにリダイレクトする
        #     return "/user/"
        # elif isinstance(request.user, MelimitStore):
        #     return "/user/anai/"
        # # else:
        # #     # userアプリ内のtemplates/account/login.htmlにリダイレクトする
        # #     return "/user/"

        user = request.user
        if user.is_authenticated:
            print(f'request.user type: {type(user)}')
            print(f'user type: {user.user_type}')
            if user.user_type == 'melimit_user':
                print('___melimit_user')
                return '/ana_ana/'
            elif user.user_type == 'melimit_store':
                print('___melimit_store')
                return '/yoshi_yoshi/'
            # else:
            #     return super().get_login_redirect_url(request)
        return super().get_login_redirect_url(request)