from django.contrib import messages
from django.shortcuts import redirect


def logout_message_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "접속중인 사용자입니다.")
            return redirect("accounts:login")

        return function(request, *args, **kwargs)

    return wrap
