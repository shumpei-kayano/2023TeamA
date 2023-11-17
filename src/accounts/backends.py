from django.contrib.auth.backends import ModelBackend
from .models import MelimitUser, MelimitStore

class MelimitUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print('MelimitUser_______')
        try:
            user = MelimitUser.objects.get(username=username)
            print(user)
            if user.check_password(password):
                # userを出力してみる
                print(f'Username: {user.username}')
                print(f'Email: {user.email}')
                return user
        except MelimitUser.DoesNotExist:
            print('none!!!!')
            return None

class MelimitStoreModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print('MelimitStore_______')
        try:
            store = MelimitStore.objects.get(email=username)
            if store.check_password(password):
                print('passcheck')
                return store
        except MelimitStore.DoesNotExist:
            print('none')
            return None