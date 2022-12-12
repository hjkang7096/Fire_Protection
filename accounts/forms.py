from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm as AuthPasswordChangeForm
from django.core.exceptions import ValidationError
from .models import User


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):  # python 3.0 문법
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields["email"].required = True

        self.fields["avatar"].label = "프로필사진"

    #     # self.fields["zipcode"].required = True
    #     # self.fields["address1"].required = True
    #     # self.fields["address2"].required = True
    #
    #     self.fields["username"].widget.attrs = {
    #         "placeholder": "아이디를 입력해주세요",
    #     }
    #     self.fields["phone_number"].widget.attrs = {
    #         "placeholder": "예시) 010-9999-9999",
    #     }
    #     self.fields["zipcode"].widget.attrs = {
    #         "placeholder": "여기를 클릭해서 주소를 검색해 주세요",
    #     }
    #     self.fields["password1"].widget.attrs = {
    #         "placeholder": "비밀번호",
    #     }
    #     self.fields["password2"].widget.attrs = {
    #         "placeholder": "비밀번호 확인",
    #     }
    #     self.fields["username"].help_text = None
    #     self.fields["avatar"].help_text = "프로필 이미지를 등록해주세요. (미 등록시에는 랜덤이미지 생성)"
    #     self.fields["password1"].help_text = None
    #     self.fields["password2"].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            query = User.objects.filter(email=email)  # self.get_object( ) 사용 가능
            if query.exists():
                raise forms.ValidationError("이미 등록된 이메일입니다.")
        return email

    class Meta(UserCreationForm.Meta):  # UserCreationForm Meta를 상속한 것임.
        model = User
        fields = [
            "username",
            # "phone_number",
            "email",
            # "zipcode",
            # "address1",
            # "address2",
            "avatar",
        ]


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):  # python 3.0 super문법
        super(ProfileForm, self).__init__(*args, **kwargs)

        #     # self.fields["email"].required = True
        #     # self.fields["zipcode"].required = True
        #     # self.fields["address1"].required = True
        #     # self.fields["address2"].required = True
        #
        # self.fields["phone_number"].label = "휴대폰번호"
        # self.fields["phone_number"].help_text = "<ul><li>{}</li><ul>".format(
        #     "입력예시) 010-9999-9999"
        # )
        # self.fields["phone_number"].widget.attrs = (
        #     {
        #         "placeholder": "예시) 010-9999-9999",
        #     },
        # )
        # self.fields["zipcode"].label = "우편번호"
        # self.fields["zipcode"].help_text = "<ul><li>{}</li><li>{}</li><ul>".format(
        #     "검색버튼을 눌러 주소를 검색해주세요", "정확한 주소는 추후 서비스제공에 편리를 제공합니다."
        # )
        #
        # self.fields["address1"].label = "기본주소"
        # self.fields["address2"].label = "상세주소"
        #
        self.fields["avatar"].label = "프로필사진"

    #     self.fields["zipcode"].widget.attrs = {
    #         "placeholder": "여기를 클릭해서 주소를 검색해 주세요",
    #     }
    #     self.fields["avatar"].help_text = "프로필 이미지를 등록해주세요. (미 등록시에는 랜덤이미지 생성)"

    class Meta:
        model = User
        fields = [
            # "phone_number",
            "email",
            # "zipcode",
            # "address1",
            # "address2",
            "avatar",
        ]


# class CheckPasswordForm(forms.Form):
#     password = forms.CharField(
#         label="비밀번호",
#         widget=forms.PasswordInput(
#             attrs={
#                 "class": "form-control",
#             }
#         ),
#     )

# def __init__(self, user, *args, **kwargs):  # 현재 유저를 가져올 수 있는 방법
#     super().__init__(*args, **kwargs)
#     self.user = user

#
# def clean(self):
#     cleaned_data = super().clean()
#     password = cleaned_data.get("password")
#     confirm_password = self.user.password

# def clean_password(self):
#     password = self.cleaned_data.get("password")
#     confirm_password = self.user.password
#
#     if password:
#         if not check_password(password, confirm_password):
#             self.add_error("password", "비밀번호가 일치하지 않습니다.")
#
#     return password


class CheckPasswordForm(forms.Form):
    password = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    # def __init__(self, user, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.user = user  # user 생성을 위해서 __init__ 함수 생성
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data.get("password")
    #     confirm_password = self.user.password
    #
    #     if password:
    #         if not check_password(password, confirm_password):
    #             self.add_error("password", "비밀번호가 일치하지 않습니다.")


class PasswordChangeForm(AuthPasswordChangeForm):  # 상속문법
    def clean_new_password2(self):
        old_password = self.cleaned_data.get("old_password")
        new_password2 = super().clean_new_password2()

        if old_password and new_password2:
            if old_password == new_password2:
                raise ValidationError("기존암호와 다르게 입력해 주세요.")

        return new_password2


class RecoveryIdForm(forms.Form):
    # name = forms.CharField(widget=forms.TextInput)
    email = forms.EmailField(widget=forms.EmailInput)

    class Meta:
        fields = ["email"]
        # fields = ["name", "email"]

    def __init__(self, *args, **kwargs):
        super(RecoveryIdForm, self).__init__(*args, **kwargs)
        # self.fields["name"].label = "이름"
        # self.fields["name"].widget.attrs.update(
        #     {
        #         "class": "form-control",
        #         "id": "form_name",
        #     }
        # )
        self.fields["email"].label = "이메일"
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "form_email",
            }
        )
