from django.contrib.auth.backends import ModelBackend
from .models import MelimitUser, MelimitStore

class MelimitUserModelBackend(ModelBackend):
    print('aaaaa')
    def authenticate(self, request, email=None, password=None, **kwargs):
        print('MelimitUser_______')
        try:
            user = MelimitUser.objects.get(email=email)
            print(user)
            if user.check_password(password):
                # userを出力してみる
                # print(f'Username: {user.email}')
                print(f'Email: {user.email}')
                return user
        except MelimitUser.DoesNotExist:
            print('none!!!!')
            # print(user.user_type)
            return None

class MelimitStoreModelBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        print('MelimitStore_______')
        try:
            store = MelimitStore.objects.get(email=email)
            if store.check_password(password):
                print('passcheck')
                # storeのmodel名を出力してみる
                model_name = store.__class__.__name__
                print(f'model: {model_name}')
                # storeのインスタンス名を出力してみる
                instance_name = type(store).__name__
                print(f'instance: {instance_name}')
                # セッションにモデル名とインスタンス名を保存
                request.session['model_name'] = model_name
                request.session['instance_name'] = instance_name
                return store
        except MelimitStore.DoesNotExist:
            print('none')
            return None