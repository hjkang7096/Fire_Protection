from django.core.validators import RegexValidator
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
        related_name="board2_author_set",
    )
    title = models.CharField(max_length=50)
    content = HTMLField()
    phone_number = models.CharField(
        max_length=13,
        validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")],
    )
    postcode = models.CharField(max_length=10)
    roadAddress = models.CharField(max_length=50)
    jibunAddress = models.CharField(max_length=50)
    detailAddress = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ["-id"]

    def get_absolute_url(self):
        return reverse("board2:post_detail", args=[self.pk])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="board2_my_author_set",
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
