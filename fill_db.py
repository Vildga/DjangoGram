import os
import django
from faker import Faker

import glob

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
django.setup()

from DjangoGramm.models import Registration, Post, Like, Dislike
from django.contrib.auth.models import User

fake = Faker()


def create_fake_user():
    return User.objects.create_user(
        username=fake.user_name(),
        password=fake.password(),
        email=fake.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )


def create_fake_post(author):
    image_folder = 'test_images'

    image_files = glob.glob(os.path.join(image_folder, 'img_*'))

    if not image_files:
        raise Exception("No image files found in the specified folder.")

    selected_image = fake.random_element(elements=image_files)

    return Post.objects.create(
        count_likes=fake.random_int(min=0, max=100),
        count_dislikes=fake.random_int(min=0, max=100),
        description=fake.text(),
        publication_date=fake.date_time(),
        images=selected_image,
        author_id=author
    )


def main():
    for _ in range(10):
        user = create_fake_user()
        post = create_fake_post(user)


if __name__ == '__main__':
    main()
