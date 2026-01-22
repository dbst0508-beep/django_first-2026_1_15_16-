from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("polls/", include("polls.urls")),
    #http://127.0.0.1:8000/polls/
    path('admin/', admin.site.urls),
    #http://127.0.0.1:8000/admin/
]
