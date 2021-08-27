from django.urls import path

from .views             import CommentView, ProjectListView, ProjectView, SearchView, ProjectOptionView

urlpatterns = [
    path("", ProjectListView.as_view()),
    path("project/<int:project_id>", ProjectView.as_view()),
    path("project/<int:project_id>/option", ProjectOptionView.as_view()),
    path("/search",SearchView.as_view()),
    path("project/<int:project_id>/comment",CommentView.as_view()),
    path("project/<int:project_id>/comments",CommentView.as_view()),
]