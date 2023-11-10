from django.contrib.auth.backends import ModelBackend
from .models import MelimitUser, MelimitStore

class MelimitUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = MelimitUser.objects.get(username=username)
            if user.check_password(password):
                return user
        except MelimitUser.DoesNotExist:
            return None

class MelimitStoreModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            store = MelimitStore.objects.get(username=username)
            if store.check_password(password):
                return store
        except MelimitStore.DoesNotExist:
            return None