from django.db import models

class User(models.Model):
    email        = models.CharField(max_length=45, unique=True, null=True)
    nickname     = models.CharField(max_length=45, null=True)
    password     = models.CharField(max_length=300)
    kakao        = models.CharField(max_length=100, unique=True, null=True)
    google       = models.CharField(max_length=100, unique=True, null=True)
    auth_level   = models.CharField(max_length=45, null=True)
    isdeleted    = models.BooleanField(default=False) 

    class Meta:
        db_table = 'users'

class Like(models.Model):
    project = models.ForeignKey('projects.project', on_delete=models.CASCADE)
    user    = models.ForeignKey('user', on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'

class Follow(models.Model):
    follower = models.ForeignKey('user', on_delete=models.CASCADE, db_column="follower", related_name='followers')
    followed = models.ForeignKey('user', on_delete=models.CASCADE, db_column="followed")

    class Meta:
        db_table = 'follows'
