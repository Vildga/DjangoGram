import os
import django
from django.core.management.base import BaseCommand
from faker import Faker
import requests
from djangoProject.settings import BASE_DIR
import uuid
import shutil
from storages.backends.s3boto3 import S3Boto3Storage

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
django.setup()

from DjangoGramm.models import Post  # Предполагая, что у вас есть модель Post в DjangoGramm.models
from django.contrib.auth.models import User

fake = Faker()


class Command(BaseCommand):
    help = 'Generate fake data for testing purposes'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating fake data...'))

        for _ in range(10):
            user = self.create_fake_user()
            post = self.create_fake_post(user)

        self.stdout.write(self.style.SUCCESS('Fake data created successfully!'))

    def create_fake_user(self):
        return User.objects.create_user(
            username=fake.user_name(),
            password=fake.password(),
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )

    def download_and_save_image(self):
        category = 'nature'
        api_url = f'https://api.api-ninjas.com/v1/randomimage?category={category}'
        headers = {'X-Api-Key': 'itZqABDWbLLInV2jpQGklA==inK7dq7RseraS75h', 'Accept': 'image/jpg'}

        response = requests.get(api_url, headers=headers, stream=True)
        if response.status_code == requests.codes.ok:
            generated_uuid = str(uuid.uuid4())
            file_name = generated_uuid[:8] + '.jpg'

            with open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)

            return file_name
        else:
            print("Error:", response.status_code, response.text)

    def create_fake_post(self, author):
        file_name = self.download_and_save_image()
        s3_file_path = f"images/posts/{file_name}"
        storage = S3Boto3Storage()

        with open(file_name, 'rb') as image_file:
            storage.save(s3_file_path, image_file)

        os.remove(file_name)

        return Post.objects.create(
            count_likes=fake.random_int(min=0, max=100),
            count_dislikes=fake.random_int(min=0, max=100),
            description=fake.text(),
            publication_date=fake.date_time(),
            images=s3_file_path,
            author_id=author
        )
