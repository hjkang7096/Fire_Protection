from django import forms
from .models import Post, Comment
from django_summernote.widgets import SummernoteWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "category",
            "phone_number",
            "content",
            "postcode",
            "roadAddress",
            "jibunAddress",
            "detailAddress",
        ]

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields["postcode"].widget.attrs = {
            "id": "sample4_postcode",
        }
        self.fields["roadAddress"].widget.attrs = {
            "id": "sample4_roadAddress",
        }
        self.fields["jibunAddress"].widget.attrs = {
            "id": "sample4_jibunAddress",
        }
        self.fields["detailAddress"].widget.attrs = {
            "id": "sample4_detailAddress",
        }
        self.fields["phone_number"].widget.attrs = {
            "placeholder": "예시)010-9999-9999",
        }

        # self.fields["title"].label = "제목"
        # self.fields["phone_number"].label = "전화번호"
        # self.fields["category"].label = "서비스 선택"
        # self.fields["roadAddress"].label = "도로명주소"
        # self.fields["jibunAddress"].label = "지번주소"
        # self.fields["detailAddress"].label = "상세주소"
        self.fields["content"].label = "남기는말"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["message"]

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields["message"].widget.attrs = {
            "placeholder": "메세지를 입력해 주세요",
            "rows": 3,
            "cols": 60,
        }
