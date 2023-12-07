from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import MelimitStore, MelimitUser

# 画面遷移時ユーザーがCustomUserに戻ってしまうため、MelimitStore/MelimitUserどちらのオブジェクトか振り分ける処理
# 各viewで使用する
class MelimitModelMixin:
    def get_melimitmodel_user(self):
        print('mixins:get_melimitmodel_user')
        user = self.request.user
        print(f"mixin_user：{user}")
        if not user.is_authenticated:
            print("ログインしてない")
            # ログインしていない場合の処理を記述

        # userのidを取得
        melimit_id = user.id
        user_type = user.user_type
        try:
            if user_type == 'melimit_user':
                user = MelimitUser.objects.get(id=melimit_id)
            elif user_type == 'melimit_store':
                user = MelimitStore.objects.get(id=melimit_id)
        except ObjectDoesNotExist:
            # print("User does not exist")
            raise Http404("User does not exist")

        if user.__class__.__name__ == 'MelimitUser':
            if isinstance(user, MelimitUser):
                return user
        elif user.__class__.__name__ == 'MelimitStore':
            if isinstance(user, MelimitStore):
                return user
        else:
            # print("User is not a MelimitModel")
            raise Http404("User is not a MelimitModel")