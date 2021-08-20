from django.urls import path, include

urlpatterns = [
    path("", include("projects.urls")),
    path('users', include('users.urls')),
    path("project", include("projects.urls")),
]
