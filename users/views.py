import json
import jwt
import requests
import bcrypt

from django.views          import View
from django.http           import JsonResponse, response

from users.models          import User
from humblebug.settings    import SECRET_KEY
from my_settings           import ALGORITHM

class KakaologinView(View):
    def get(self, request):
        try:
            access_token = request.headers.get("Authorization")
            
            if not access_token:
                return JsonResponse({"message" : "INVALID_TOKEN"}, status = 400)
                
            response = requests.get(
                    "https://kapi.kakao.com/v2/user/me", 
                    headers = {"Authorization" : f"Bearer {access_token}"}
                    )
                    
            if not response:
                    return JsonResponse({"message" : "NOT_FOUND_IN_KAKAO"}, status = 404)
                    
            profile_json  = response.json()
                
            kakao_id      = profile_json.get("id")
            kakao_account = profile_json.get("kakao_account")
            name          = kakao_account["profile"]["nickname"]
                
            user, created = User.objects.get_or_create(
			kakao     = kakao_id,
			defaults  = {"nickname" : name,}
			)
            user.name     = name
            user.save()
			
            token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = "HS256")
                
            return JsonResponse({"message" : "SUCCESS", "access_token" : token}, status = 200)
        except KeyError:
                return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
