from django.db import models

class Category(models.Model):
    category = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'

class Tag(models.Model):
    tag = models.CharField(max_length=45)

    class Meta:
        db_table = 'tags'

class Project(models.Model):
    name           = models.CharField(max_length=45)
    user           = models.ForeignKey('users.user', on_delete=models.CASCADE)
    aim_amount     = models.CharField(max_length=45)
    descrption     = models.CharField(max_length=20000)
    tag            = models.ForeignKey('tag', on_delete=models.SET_NULL, null=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    end_date       = models.DateTimeField()
    category       = models.ForeignKey('category', on_delete=models.SET_NULL, null=True)
    main_image_url = models.CharField(max_length=1000)
    ispublic       = models.BooleanField(default=False)

    class Meta:
        db_table = 'projects'

class Comment(models.Model):
    user        = models.ForeignKey('users.user', on_delete=models.CASCADE)
    project     = models.ForeignKey('project', on_delete=models.CASCADE)
    description = models.CharField(max_length=500)

    class Meta:
        db_table = 'comments'

class Patron(models.Model):
    user    = models.ForeignKey('users.user', on_delete=models.CASCADE)
    project = models.ForeignKey('project', on_delete=models.CASCADE)
    option  = models.ForeignKey('option', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'patrons'

class Option(models.Model):
    name    = models.CharField(max_length=45)
    amount  = models.CharField(max_length=45)
    project = models.ForeignKey('project', on_delete=models.CASCADE)

    class Meta:
        db_table = 'options'