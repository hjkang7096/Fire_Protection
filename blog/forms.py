from django import forms
from .models import Post, Comment
from django_summernote.widgets import SummernoteWidget
from tinymce.widgets import TinyMCE


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "head_image", "file_upload", "category"]
        # widgets = {
        #     "content": TinyMCE(
        #         # attrs={"summernote": {"width": "50%", "height": "400px"}}
        #     ),
        # }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields["content"].widget.attrs = {
            # "placeholder": "본문에 #을 이용하여 태그를 사용해 보세요",
            "rows": 15,
            "cols": 60,
        }

        self.fields["title"].label = "제목"
        self.fields["content"].label = "내용"
        self.fields["head_image"].label = "이미지업로드"
        self.fields["file_upload"].label = "파일업로드"
        self.fields["category"].label = "카테고리"


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
