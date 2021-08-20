from django.urls import path
from users.views import KakaologinView

urlpatterns = [ 
	path ('/signin', KakaologinView.as_view()),
] 
