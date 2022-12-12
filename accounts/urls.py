from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = "accounts"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("profile_edit/", views.profile_edit, name="profile_edit"),
    path("profile_delete/", views.profile_delete, name="profile_delete"),
    path("password_change/", views.password_change, name="password_change"),
    path("recovery/id/", views.RecoveryIdView.as_view(), name="recovery_id"),
    path("recovery/id/find/", views.ajax_find_id_view, name="ajax_id"),
    # 비밀번호 초기화
    path(
        "password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
]
