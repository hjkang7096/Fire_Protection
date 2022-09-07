from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("<int:pk>/", views.post_detail, name="post_detail"),
    path("post_new/", views.post_new, name="post_new"),
    path("post_update/<int:pk>/", views.post_update, name="post_update"),
    path("post_delete/<int:pk>/", views.post_delete, name="post_delete"),
]
