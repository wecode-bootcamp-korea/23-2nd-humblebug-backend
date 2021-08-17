from django.db import models

class TimeStampModel(models.Model): 
    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True) 
    
    class Meta: 
        abstract = True
        
class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name
        
class Tag(models.Model):
    tag = models.CharField(max_length=45)

    class Meta:
        db_table = 'tags'

    def __str__(self):
        return self.tag

class Project(TimeStampModel):
    name           = models.CharField(max_length=45)
    user           = models.ForeignKey('users.User', on_delete=models.CASCADE)
    aim_amount     = models.PositiveIntegerField(null=True)
    description    = models.TextField(null=True)
    tag            = models.ManyToManyField('Tag')
    end_date       = models.DateTimeField(null=True)
    category       = models.ForeignKey('category', on_delete=models.SET_NULL, null=True)
    main_image_url = models.CharField(max_length=1000)
    isvisible      = models.BooleanField(default=False)
    isdeleted      = models.BooleanField(default=False)  

    class Meta:
        db_table = 'projects'

    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.name

