from django.urls import path

from .views             import ProjectListView, ProjectView, SearchView

urlpatterns = [
    path("", ProjectListView.as_view()),
    path("/<int:project_id>", ProjectView.as_view()),
    path('/search',SearchView.as_view()),
]
