import json, bcrypt

from django.test     import TestCase, Client
from unittest.mock   import patch, MagicMock
from .models    import User
# Create your tests here.

class KakaoLoginTest(TestCase):
    def setUp(self):
        User.objects.create(
            social_login = '67890',
            name         = "한효주",
            email        = "abcd@gmail.com",
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch("user.views.requests")
    def test_kakaosignupview_get_success(self, mocked_requests):
        client   = Client()
        
        class MockedResponse:
            def json(self):
                return {
                    "id" : "12345",
                    "properties" : {
                        "nickname" : "한상웅"
                    },
                    "kakao_account":{
                        "email":"abcd@gmail.com"
                    }
                }
        
        mocked_requests.post = MagicMock(return_value = MockedResponse())
        
        response = client.get("/user/kakaologin", **{"HTTP_AUTHORIZATION":"1234","content_type" : "application/json"})
        self.assertEqual(response.status_code, 201)
    
    @patch("user.views.requests")
    def test_kakaologinview_get_success(self, mocked_requests):
        client   = Client()
        
        class MockedResponse:
            def json(self):
                return {
                    "id" : "67890",
                    "properties" : {
                        "nickname" : "한효주"
                    },
                    "kakao_account":{
                        "email":"abcd@gmail.com"
                    }
                }

        mocked_requests.post = MagicMock(return_value = MockedResponse())
        
        response = client.get("/user/kakaologin", **{"HTTP_AUTHORIZATION":"1234","content_type" : "application/json"})
        self.assertEqual(response.status_code, 200)

    @patch("user.views.requests")
    def test_kakaologinview_get_fail(self, mocked_requests):
        client   = Client()

        class MockedResponse:
            def json(self):
                return {
                    'msg': 'this access token does not exist', 'code': -401
                }

        mocked_requests.post = MagicMock(return_value = MockedResponse())

        response = client.get("/user/kakaologin", **{"HTTP_AUTHORIZATION":"1234","content_type" : "application/json"})
        self.assertEqual(response.json(),{'message':'INVALID_TOKEN'})
        self.assertEqual(response.status_code, 400)
    
    def test_kakaologinview_get_not_found(self):
        client   = Client()
        response = client.get('/user/a')
        self.assertEqual(response.status_code, 404)