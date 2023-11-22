from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import MelimitStore, MelimitUser

class MelimitModelMixin:
    def get_melimitmodel_user(self):
        user = self.request.user
        # userのidを取得
        melimit_id = user.id
        user_type = user.user_type
        try:
            if user_type == 'melimit_user':
                user = MelimitUser.objects.get(id=melimit_id)
            elif user_type == 'melimit_store':
                user = MelimitStore.objects.get(id=melimit_id)
        except ObjectDoesNotExist:
            raise Http404("User does not exist")

        if user.__class__.__name__ == 'MelimitUser':
            if isinstance(user, MelimitUser):
                return user
        elif user.__class__.__name__ == 'MelimitStore':
            if isinstance(user, MelimitStore):
                return user
        else:
            raise Http404("User is not a MelimitModel")