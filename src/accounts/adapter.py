from allauth.account.adapter import DefaultAccountAdapter
from .models import *

class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        this is called when saving user via allauth registraction.
        we override this to set additional data on user object.
        """
        # do # Do not persist the user yet so we pass commit=False
        # (last argument)
        # super(AccountAdapter, self)
        user = super().save_user(request, user, form, commit=False)
        #user.userType = form.cleaned_data.get('userType')
        try:
            user.is_typename = request.POST['is_typename'] == 'True'
        except KeyError:
            user.is_typename = False
        # if not user.usertype:
        #     user.usertype = False # デフォルトのユーザ種別を設定

        # ユーザIDを取得するために一旦保存する
        user.save()

        # if user.usertype == True:
        #     # サプライヤーユーザ
        #     supplier = MelimitStoreDetail()
        #     supplier.user_id = user.id
        #     supplier.username = request.POST['username']
        #     supplier.save()
        # else:
        #     # それ以外は一般ユーザ
        #     user.usertype = False
        #     buyer = MelimitUserDetail()
        #     buyer.user_id = user.id
        #     buyer.username = request.POST.get('username', False)
        #     buyer.save()