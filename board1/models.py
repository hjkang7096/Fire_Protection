import os
from django.db import models
from django.conf import settings
from django.urls import reverse
from tinymce.models import HTMLField


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="board1_author_set",
    )
    title = models.CharField(max_length=50)
    content = HTMLField()
    head_image = models.ImageField(upload_to="board1/images/%Y/%m/%d", blank=True)
    file_upload = models.FileField(upload_to="board1/files/%Y/%m%d", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ["-id"]

    def get_absolute_url(self):
        return reverse("board1:post_detail", args=[self.pk])

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split(".")[-1]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="board1_my_author_set",
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return "{}::{}".format(self.author, self.message)

    def get_absolute_url(self):
        return f"{self.post.get_absolute_url()}#comment-{self.pk}"
