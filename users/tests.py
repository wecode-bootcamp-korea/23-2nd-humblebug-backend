import json, jwt

from users.models import User

from django.test     import TestCase, Client
from unittest.mock   import patch, MagicMock
from my_settings  import SECRET_KEY
# Create your tests here.

class KakaoLoginTest(TestCase):
    def setUp(self):
        pass

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
        
        response = client.get("/users/kakaologin", **{"AUTHORIZATION":"1234","content_type" : "application/json"})
        self.assertEqual(response.status_code, 201)