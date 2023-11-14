from django.contrib.auth.backends import ModelBackend
from .models import MelimitUser, MelimitStore

class MelimitUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print('MelimitUser_______')
        try:
            user = MelimitUser.objects.get(username=username)
            if user.check_password(password):
                # userを出力してみる
                print(f'Username: {user.username}')
                print(f'Email: {user.email}')
                return user
        except MelimitUser.DoesNotExist:
            return None

class MelimitStoreModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print('MelimitStore_______')
        try:
            store = MelimitStore.objects.get(username=username)
            if store.check_password(password):
                return store
        except MelimitStore.DoesNotExist:
            return None