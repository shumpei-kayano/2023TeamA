from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django_seed import Seed
from faker import Faker
from django.contrib.auth import get_user_model
from accounts.models import MelimitStore, MelimitUser

class Command(BaseCommand):
    help = 'Seeds the database with data for myapp'
    fake = Faker('ja_JP')

    def handle(self, *args, **options):
        seeder = Seed.seeder(locale='ja_JP')
        User = get_user_model()

        # 顧客ユーザー
        user_usernames = ['ATTS様_1', 'ATTS様_2', 'トリアナ様_1', 'トリアナ様_2', '大分シーイーシー様_1', '中島校長先生', 'テスト_1']

        for i, username in enumerate(user_usernames, start=1):
            seeder.add_entity(MelimitUser, 1, {
                'email': f'user{i}@mail.com',
                'password': make_password('P123456789'),
                'username': username,
                'postal_code': self.fake.postcode().replace('-', ''),
                'prefecture': self.fake.prefecture(),
                'city': self.fake.city(),
                'address': self.fake.town() + self.fake.building_number(),
                'phone_number': self.fake.phone_number().replace('-', ''),
                'user_type': 'melimit_user',
                'is_active': True,
                'is_staff': True,
                'is_superuser': False,
                'taste': self.fake.random_element(elements=('meat', 'vegetables', 'fruit', 'fish')),
                'date_joined': self.fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None),
            })

        # 店舗ユーザー
        store_usernames = ['ATTS様_1', 'ATTS様_2', 'トリアナ様_1', 'トリアナ様_2', '大分シーイーシー様_1', '中島校長先生', 'テスト_1']

        for i, username in enumerate(store_usernames, start=1):
            seeder.add_entity(MelimitStore, 1, {
                'email': f'store{i}@mail.com',
                'password': make_password('P123456789'),
                'username': username,
                'postal_code': self.fake.postcode().replace('-', ''),
                'prefecture': self.fake.prefecture(),
                'city': self.fake.city(),
                'address': self.fake.town() + self.fake.building_number(),
                'phone_number': self.fake.phone_number().replace('-', ''),
                'site_url': self.fake.url(),
                'user_type': 'melimit_store',
                'is_active': True,
                'is_staff': True,
                'is_superuser': False,
                'date_joined': self.fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None),
            })

        seeder.execute()
        self.stdout.write(self.style.SUCCESS('できたよ！'))
