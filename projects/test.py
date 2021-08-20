from django.test       import TestCase
from projects.models   import Project, Category
from users.models      import User

import unittest, json

from django.test import TestCase
from django.test import Client

from .models      import Project

class MainListViewTest(TestCase):
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

    def test_mainlist_success(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'project': [{ 
            "id"         : 1,
            "category_id": 1,
            "user_id"    : 1,
            "name"       : "탱고플레이트",
            "image" : "https://humblebug.s3.us-east-2.amazonaws.com/image1.png",            
            "aim_amount" : 500000,
            "created_at" : "2021-08-19T11:03:10.216Z",
            "description": "맛집 별점 어플 망고플레이트 클론코딩",
            "end_date": "2021-11-06T00:00:00Z"
        }]})

    def tearDown(self):
        User.objects.all().delete(),
        Project.objects.all().delete()
        Category.objects.all().delete(),
