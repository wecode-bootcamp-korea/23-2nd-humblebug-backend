import json
import jwt
import requests
import bcrypt

from django.views          import View
from django.http           import JsonResponse

from users.models          import Like, User
from humblebug.settings    import SECRET_KEY
from my_settings		   import AlGORITHM
from users.utils           import login_required

class KakaologinView(View):
	def get(self, request):
		try:
			access_token = request.headers.get("Authorization")

			if not access_token:
				return JsonResponse({"message" : "NEED_TOKEN"}, status = 400)

			profile_request = requests.get(
				"https://kapi.kakao.com/v2/user/me", headers = {"Authorization" : f"Bearer {access_token}"}
			)

			if not profile_request:
				return JsonResponse({"message" : "NOT_FOUND_IN_KAKAO"}, status = 404)

			profile_json  = profile_request.json()
       
			kakao_id      = profile_json.get("id")
			kakao_account = profile_json.get("kakao_account")
			name          = kakao_account["profile"]["nickname"]
    
			if not User.objects.filter(kakao = kakao_id).exists():
				User.objects.create(
							kakao     = kakao_id,
							name      = name,
				)

			user           = User.objects.get(kakao = kakao_id)
			user.name      = name
			user.save()

			token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = "HS256")
			
			return JsonResponse({"message" : "SUCCESS", "acess_token" : token}, status = 200)

		except KeyError:
			return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

class LikeView(View):
    @login_required
    def get(self, request):
        try:
            user=User.objects.get(id=request.user.id)
           # like_list      = user.wishlist_set.all().annotate(price=Min("product__option__price"))
            
            like_items = [{
                'product_id'   : like.product.id,
                'name'         : like.product.name,
                'image'        : like.product.thumbnail_image_url,
                'price'        : like.price} for like in like_list]
            return JsonResponse({'Like_Items' : like_items}, status = 200)
        except KeyError:
            return JsonResponse({'Message' : 'KEY_ERROR'}, status = 400)
    
    @login_required
    def post(self,request):
        try:
            data           = json.loads(request.body)
            product_id     = data.get('product_id')
            user_id        = request.user.id

            if Like.objects.filter(Q(product_id=product_id) & Q(user_id=user_id)).exists():
               Like.objects.filter(product_id=product_id).delete()
               return JsonResponse({'Message' : 'SUCCESS_DELETE'}, status = 200)
            else:
                Like.objects.create(
                product_id    = data['product_id'],
                user_id       = user_id
                )
            return JsonResponse({'Message' : 'SUCCESS_CREATE'}, status = 200)
        except KeyError:
            return JsonResponse({'Message' : 'KEY_ERROR'}, status = 400)