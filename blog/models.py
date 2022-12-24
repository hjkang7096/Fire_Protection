import os.path, re
from django.db import models
from django.conf import settings
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
from tinymce.models import HTMLField


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/blog/post_list_tag/{}/".format(self.name)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = HTMLField()
    head_image = models.ImageField(upload_to="blog/images/%Y/%m/%d", blank=True)
    head_image_thumbnail = ImageSpecField(
        source="head_image",  # 원본 ImageField 명
        processors=[Thumbnail(850, 350)],  # 처리할 작업목록
        format="JPEG",  # 최종 저장 포맷
        options={"quality": 60},
    )  # 저장 옵션
    file_upload = models.FileField(upload_to="blog/files/%Y/%m%d", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    tag = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return "custom Post object({})".format(self.id)

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.pk])

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split(".")[-1]

    def extract_tag_list(self):
        pattern = r"#([a-zA-Z\dㄱ-힣]+)"
        content = self.content.replace(" ", "")
        tag_name_list = re.findall(pattern, content)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list

    class Meta:
        ordering = ["-id"]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return "{}::{}".format(self.author, self.message)

    def get_absolute_url(self):
        return f"{self.post.get_absolute_url()}#comment-{self.pk}"

    # def get_avatar_url(self): Todo pydenticon 구현 후
    #     if self.author.socialaccount_set.exists():
    #         return self.author.socialaccount_set.first().get_avatar_url()
    #     else:
    #         return f'https://doitdjango.com/avatar/id/106/31c7242a73e4f345/svg/{self.author.email}'
