import json, jwt, unittest

from django.test      import TestCase, Client

from unittest.mock    import patch, MagicMock
from my_settings      import SECRET_KEY

from users.models     import User

# Create your tests here.

class KakaoSigninTest(TestCase):
    def setUp(self):
        User.objects.create(
            kakao     = 10041004,
            nickname      = "한효주",
        )
        
    def tearDown(self):
        User.objects.all().delete()
        
    @patch("users.views.requests")
    
    def test_kakao_signin_user_success(self, mocked_requests) :
        class MockedResponse :
            def json(self) :
                return {
                    "id"            : 10041004,
                    "kakao_account" : {
                    "profile_nickname_needs_agreement": True,
                    "profile"                   : {
                    "nickname"            : "한효주",
                    },
                    "has_email": True,
                    "email_needs_agreement"     : False,
                    "is_email_valid"            : True,
                    "is_email_verified"         : True,
                    "email"                     : "angel@gmail.com",}
                }
        
        mocked_requests.get = MagicMock(return_value = MockedResponse())

        client   = Client()
        headers  = {"HTTP_Authorization" : "1234"}
        response = client.get("/users/signin", content_type='applications/json', **headers)
        self.assertEqual(response.status_code, 200)
        
        user       = User.objects.get(kakao=10041004)
        fake_token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = "HS256")
        self.assertEqual(response.json()["acess_token"], fake_token)
        
    @patch("users.views.requests")
    def test_kakao_signin_user_fail_needtoken(self, mocked_requests) :
        class MockedResponse :
            def json(self) :
                return {
                        "id"            : 10041004,
                        "kakao_account" : {
                        "profile_nickname_needs_agreement": True,
                        "profile"                   : {
                        "nickname"            : "한효주",
                        },
                        "has_email": True,
                        "email_needs_agreement"     : False,
                        "is_email_valid"            : True,
                        "is_email_verified"         : True,
                        "email"                     : "angel@gmail.com",}
                        }
        mocked_requests.get = MagicMock(return_value = MockedResponse())

        client = Client()
        headers = {}
        response = client.get("/users/signin", content_type = 'applications/json', **headers)
        self.assertEqual(response.status_code, 400)
