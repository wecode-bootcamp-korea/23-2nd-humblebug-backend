from django.urls import path
from users.views import KakaologinView, LikeView

urlpatterns = [ 
	path ('/signin', KakaologinView.as_view()),
	path ('/like', LikeView.as_view())
] 
