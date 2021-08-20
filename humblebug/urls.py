from django.urls import path, include

urlpatterns = [
    path("", include("projects.urls")),
    path("project", include("projects.urls")),
    path('users', include('users.urls')),
]
