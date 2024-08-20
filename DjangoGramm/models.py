from django.db import models
from django.contrib.auth.models import User


# class Registration(models.Model):
#     id = models.AutoField(primary_key=True)
#     login = models.CharField(max_length=30, unique=True)
#     password = models.CharField(max_length=30)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     avatar = models.ImageField(upload_to='images/avatars', blank=True)
#     date_of_birth = models.DateTimeField(blank=True, null=True)
#     about = models.TextField(blank=True)
#     is_active = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.login


class Following(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    count_likes = models.IntegerField()
    count_dislikes = models.IntegerField()
    description = models.TextField()
    publication_date = models.DateTimeField()
    images = models.ImageField(upload_to='images/posts')
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Tags(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    link = models.TextField()
    count_users = models.IntegerField()


class PostHasTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)

