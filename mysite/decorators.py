from django.shortcuts import redirect
from django.contrib import messages


def superuser_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser:
            # if request.user.level == "1" or request.user.level == "0":
            return function(request, *args, **kwargs)

        messages.info(request, "접근 권한이 없습니다.")
        return redirect("board2:post_list")

    return wrap


def logout_message_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "접속중인 사용자입니다.")
            return redirect("/")

        return function(request, *args, **kwargs)

    return wrap
