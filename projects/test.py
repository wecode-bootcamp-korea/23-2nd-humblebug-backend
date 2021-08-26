from django.test       import TestCase

from projects.models   import Project, Category, Tag, Option, Patron, Comment
from users.models      import User

import unittest, json

from django.test import TestCase
from django.test import Client

class MainListViewTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            nickname="유영",
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
        self.assertEqual(response.json(), {
            'project': [{ 
            "id"         : 1,
            "category_id": 1,
            "user_id"    : 1,
            "user_name"  : "유영",
            "name"       : "탱고플레이트",
            "image" : "https://humblebug.s3.us-east-2.amazonaws.com/image1.png",            
            "aim_amount" : 500000,
            "created_at" : "2021-08-19T11:03:10.216Z",
            "description": "맛집 별점 어플 망고플레이트 클론코딩",
            "end_date": "2021-11-06T00:00:00Z",
        }]})

    def tearDown(self):
        User.objects.all().delete(),
        Project.objects.all().delete()
        Category.objects.all().delete(),

class ProjectTest(TestCase):

    def setUp(self):
        User.objects.create(
            id=2,
            email='hyerimc858@gmail.com',
            nickname='리미',
            password='abc1234')

        Category.objects.create(
            id=2,
            name='커머스'
        )
        
        Project.objects.create(
            id=2,
            name='혜림이 프로젝트',
            aim_amount=500000,
            description='혜림이 프로젝트!!!',
            end_date='2021-12-30',
            main_image_url='asdfasdf',
            category_id=2,
            user_id=2,
            )
        
        Tag.objects.bulk_create([
            Tag(id=1, tag='쇼핑몰'),
            Tag(id=2, tag='구독'),
            Tag(id=3, tag='약'),
            Tag(id=4, tag='23기'),
            Tag(id=5, tag='음식'),
            Tag(id=6, tag='패션')
        ])

        Option.objects.bulk_create([
            Option(id=1, name='껌', amount=500, project_id=2),
            Option(id=2, name='복숭아요거트스무디', amount=5000, project_id=2),
            Option(id=3, name='노트북', amount=1000000, project_id=2)
        ])

        Project.objects.get(id=2).tag.add(Tag.objects.get(id=2))

        Patron.objects.create(
            option_id=1,
            project_id=2,
            user_id=2,
            total_amount=100000
            )
	
    def test_success_project_view_get_handler_method(self):
        client   = Client()
        response = client.get('/project/2')

        self.assertEqual(response.json(), 
            {
            "project_information": {
                "tag": [
                    {
                        "id": 2,
                        "name": "구독"
                    }
                ],
                "name": "혜림이 프로젝트",
                "user": "리미",
                "remaining_time": 126,
                "number_of_sponsors": 1,
                "main_image_url": "asdfasdf",
                "aim_amount": 500000,
                "payment_date": "2021년 12월 30일",
                "collected_amount": 100000,
                "percentage": "20%"
                }
            }
        )
        self.assertEqual(response.status_code, 200)

class SearchViewTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            nickname="유영",
            kakao    = 1234,

        )
        Category.objects.create(
            id = 1,
            name = '리뷰'
        )
        project = Project.objects.create(
            id             = 1,
            category_id    = 1,
            name           = '탱고플레이트',
            user_name      = '1',
            user_id        = 1,
            aim_amount     = '500000',
            description    = '맛집 별점 어플 망고플레이트 클론코딩',
            end_date       = '2021-11-06 00:00',
            main_image_url = 'https://humblebug.s3.us-east-2.amazonaws.com/image1.png'
        )
        project.created_at = '2021-08-19T11:03:10.216Z'
        project.save()

    def test_search_success(self):
        client=Client()
        response = self.client.get('/projects/search?search=1')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), {
            'project': [
            { 
            "id"         : 4,
            "category_id": 3,
            'user_id'   : 1,
            "user_name"    : 1,
            "name"       : "탱고플레이트",
            "image" : "https://user-images.githubusercontent.com/8315252/130033730-65f628fc-9cfa-4167-a2a1-2de44e7be1d8.png",            
            "aim_amount" : 500000,
            "created_at" : "2021-08-19T11:03:10.216Z",
            "description": "맛집 별점 어플 망고플레이트 클론코딩",
            "end_date": "2021-11-06T00:00:00Z"
            }]})
        

    def tearDown(self):
        User.objects.all().delete(),
        Project.objects.all().delete()
        Category.objects.all().delete(),

class ProjectCommentTest(TestCase):
    def setUp(self):
        
        User.objects.create(
            id       = 2,
            nickname= "최혜림",
            kakao    = 1234,
        )

        Project.objects.create(
            id=2,
            name='혜림이 프로젝트',
            aim_amount=500000,
            description='혜림이 프로젝트!!!',
            end_date='2021-12-30',
            main_image_url='asdfasdf',
            category_id=2,
            user_id=2,
            )
        
        Comment.objects.create(
            id = 1,
            description = '짱짱',
            project_id = 2,
            user_id = 2
        )

    def test_success_comment_view_get_handler_method(self):
        client   = Client()
        response = client.get('/project/2/comments')

        self.assertEqual(response.json(), 
            {
            "comments": [
                {
                    "user_id": 2,
                    "nickname": "최혜림",
                    "description": "짱짱"
                }
            ]
        }
        )
        self.assertEqual(response.status_code, 200)