import json
import jwt
import requests
import bcrypt

from django.views          import View
from django.http           import JsonResponse

from users.models          import User
from humblebug.settings      import SECRET_KEY

class KakaologinView(View):
    def post(self, request):
        try:
            access_token   = request.headers.get("Authorization", None)   #프런트에서 토큰 받아오기

            token_info_url = 'https://kapi.kakao.com/v2/user/me'              
            headers        = {'Authorization' : f"Bearer {access_token}"}  
            user_info_response = requests.post(token_info_url, headers=headers) 
            user_info_json     = user_info_response.json() 
            print(user_info_json)               
            #받은 토큰으로 카카오한테 유저정보 요청하기
            kakao_account      = user_info_json.get('kakao_account')         
            kakao_id           = user_info_json.get('id')  
                
            user, first_login = User.objects.get_or_create( #유저정보 없으면 생성
                    kakao    = kakao_id,
                    #email    = kakao_account['email'],
                    #nickname = kakao_account['properties']['nickname'], 
                  # nickname = kakao_account['properties'].get['nickname']
                   #nickname = kakao_account['profile']['nickname']
                )

            token = jwt.encode({'email' : kakao_account['email']}, SECRET_KEY, algorithm = 'HS256')
            
            access_token = token

            return JsonResponse({"access_token" : access_token}, status = 200)

        except KeyError:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status = 400)
