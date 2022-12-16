from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, logout_then_login
from django.contrib.auth import login as auth_login, update_session_auth_hash
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from .forms import (
    SignupForm,
    ProfileForm,
    PasswordChangeForm,
    CheckPasswordForm,
    RecoveryIdForm,
)
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.urls import reverse_lazy
from django.views.generic import View
from .decorators import logout_message_required
import json
from .models import User
from django.contrib.auth import views as auth_views
from mysite.decorators import logout_message_required


class Login(LoginView):
    template_name = "accounts/login_form.html"


login = logout_message_required(Login.as_view())


@login_required
def logout(request):
    messages.success(request, "로그아웃 되었습니다.")
    return logout_then_login(request)  # global settings login url로 이동


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            signed_user = form.save()
            messages.success(request, "회원가입을 축하드립니다.")
            auth_login(request, signed_user)
            # urls.py에서 login_required()로 감싸는 경우 next인자 생성
            return redirect("/")
    else:
        form = SignupForm()
    return render(
        request,
        "accounts/signup_form.html",
        {
            "form": form,
        },
    )


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "회원정보를 성공적으로 변경하였습니다.")
            return redirect("accounts:profile_edit")
    else:
        form = ProfileForm(instance=request.user)

    return render(
        request,
        "accounts/profile_edit_form.html",
        {
            "form": form,
        },
    )


def profile_delete(request):
    if request.method == "POST":
        form = CheckPasswordForm(request.POST)
        if form.is_valid():
            password = request.POST["password"]
            user = request.user
            if check_password(password, user.password):
                user.delete()
                logout(request)
                messages.success(request, "회원탈퇴가 완료되었습니다.")
                return redirect("/")
            else:
                form.add_error("password", "비밀번호가 일치하지 않습니다.")
    else:
        form = CheckPasswordForm()

    return render(
        request,
        "accounts/profile_delete.html",
        {
            "form": form,
        },
    )


# class PasswordChangeView(
#     LoginRequiredMixin, AuthPasswordChangeView, SuccessMessageMixin
# ):
#     form_class = PasswordChangeForm
#     success_url = reverse_lazy("accounts:password_change")
#     template_name = "accounts/password_change_form.html"
#     success_message = "비밀번호를 변경했습니다!"
#
#
# password_change = PasswordChangeView.as_view()


@login_required
def password_change(request):
    if request.method == "POST":
        password_change_form = PasswordChangeForm(
            request.user, request.POST, request.FILES
        )
        if password_change_form.is_valid():
            new_password = password_change_form.save()
            update_session_auth_hash(request, new_password)
            messages.success(request, "비밀번호를 성공적으로 변경하였습니다.")
            return redirect("accounts:profile_edit")
    else:
        password_change_form = PasswordChangeForm(request.user)
    return render(
        request,
        "accounts/password_change_form.html",
        {
            "form": password_change_form,
        },
    )


@method_decorator(logout_message_required, name="dispatch")
class RecoveryIdView(View):
    template_name = "accounts/recovery_id.html"
    recovery_id = RecoveryIdForm

    def get(self, request):
        if request.method == "GET":
            form = self.recovery_id(None)

        return render(
            request,
            self.template_name,
            {
                "form": form,
            },
        )


def ajax_find_id_view(request):
    # name = request.POST.get("name")
    email = request.POST.get("email")
    # result_id = User.objects.get(name=name, email=email)
    result_id = User.objects.get(email=email)

    return HttpResponse(
        json.dumps({"result_id": result_id.username}, cls=DjangoJSONEncoder),
        content_type="application/json",
    )
