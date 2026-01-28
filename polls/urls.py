from django.urls import path
from . import views
from . import practice_views

app_name = "polls"

urlpatterns = [
    # FBV (주석 처리됨)
    # path("", views.index, name="index"),
    # path("<int:question_id>/", views.detail, name="detail"),
    # path("<int:question_id>/results/", views.results, name="results"),
    # path("<int:question_id>/vote/", views.vote, name="vote"),
    
    # CBV
    path("", views.IndexView.as_view(), name="index"), 
    path("<int:pk>/", views.DetailView.as_view(), name="detail"), 
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),

    # CRUD
    path("create/", views.QuestionCreateView.as_view(), name="question_create"), 
    path("<int:pk>/update/", views.QuestionUpdateView.as_view(), name="question_updata"),
    path("<int:pk>/delete/", views.QuestionDeleteView.as_view(), name="question_delete"), 

     path("practice/1/", practice_views.practice_1, name="practice_1"),
     path("practice/2/", practice_views.practice_2, name="practice_2"),
     path("practice/3/", practice_views.practice_3, name="practice_3"),
     path("practice/5/", practice_views.practice_5, name="practice_5"),
     path("practice/6/", practice_views.practice_6, name="practice_6"),


    path("practice/api/1/", practice_views.practice_api_1, name="practice_api_1"),
    path("practice/api/2/", practice_views.practice_api_2, name="practice_api_2"),
    path("practice/api/3/", practice_views.practice_api_3, name="practice_api_3"),
    path("practice/api/5/", practice_views.practice_api_5, name="practice_api_5"),
    path("practice/api/6/", practice_views.practice_api_6, name="practice_api_6"),
]






