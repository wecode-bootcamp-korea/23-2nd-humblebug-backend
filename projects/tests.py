import jwt

from django.test                    import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock                  import MagicMock, patch

from users.models      import User
from .models           import Project
from my_settings       import SECRET_KEY, ALGORITHM

class ProjectViewTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            kakao    = 1234,
            password = 'wecode12#',
        )
        Category.objects.create(
            id = 1,
            name = '리뷰'
        )
        project = Project.objects.create(
            id             = 1,
            category_id    = 1,
            name           = '탱고플레이트',
            user_id        = 1,
            aim_amount     = '500000',
            description    = '맛집 별점 어플 망고플레이트 클론코딩',
            end_date       = '2021-11-06 00:00',
            main_image_url = 'https://humblebug.s3.us-east-2.amazonaws.com/image1.png'
        )
        project.created_at = '2021-08-19T11:03:10.216Z'
        project.save()
    
    def tearDown(self):
        Project.objects.all().delete(),
        Category.objects.all().delete()
        User.objects.all().delete(),
