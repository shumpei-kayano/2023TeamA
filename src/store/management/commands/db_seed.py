from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django_seed import Seed
from faker import Faker
from django.contrib.auth import get_user_model
from accounts.models import MelimitStore, MelimitUser

class Command(BaseCommand):
    help = 'Seeds the database with data for myapp'
    fake = Faker('ja_JP')  # ロケールを 'ja_JP' として直接指定

    def handle(self, *args, **options):
        seeder = Seed.seeder(locale='ja_JP')
        User = get_user_model()

        # Melimitstore
        seeder.add_entity(MelimitStore, 3, {
            'email': lambda x: self.fake.email(),
            'password': make_password('P123456789'),
            'username': lambda x: self.fake.company(),
            'postal_code': lambda x: self.fake.postcode().replace('-', ''),
            'prefecture': lambda x: self.fake.prefecture(),
            'city': lambda x: self.fake.city(),
            'address': lambda x: self.fake.town(),
            'phone_number': lambda x: self.fake.phone_number().replace('-', ''),
            'site_url': lambda x: self.fake.url(),
            'user_type': 'melimit_store',
            'is_active': True,
            'is_staff': True,
            'is_superuser': False,
            'date_joined': lambda x: self.fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None),
        })
        
        # Melimituser
        seeder.add_entity(MelimitUser, 3, {
            'email': lambda x: self.fake.email(),
            'password': make_password('P123456789'),
            'username': lambda x: self.fake.name(),
            'postal_code': lambda x: self.fake.postcode().replace('-', ''),
            'prefecture': lambda x: self.fake.prefecture(),
            'city': lambda x: self.fake.city(),
            'address': lambda x: self.fake.town(),
            'phone_number': lambda x: self.fake.phone_number().replace('-', ''),
            'user_type': 'melimit_user',
            'is_active': True,
            'is_staff': True,
            'is_superuser': False,
            'taste': lambda x: self.fake.random_element(elements=('meat', 'vegetables', 'fruit', 'fish')),
            'date_joined': lambda x: self.fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None),
        })

        seeder.execute()
        self.stdout.write(self.style.SUCCESS('できたよ！'))
