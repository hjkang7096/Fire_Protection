from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.shortcuts import resolve_url, redirect


class User(AbstractUser):
    # phone_number = models.CharField(
    #     max_length=13,
    #     blank=True,
    #     validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")],
    # )
    avatar = models.ImageField(blank=True, upload_to="accounts/avatar/%Y/%m/%d")
    # zipcode = models.CharField(max_length=10, blank=True, null=True)
    # address1 = models.CharField(max_length=50, blank=True)
    # address2 = models.CharField(max_length=50, blank=True)

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return resolve_url("pydenticon_image", self.username)

    @property
    def name(self):
        return "{} {}".format(self.last_name, self.first_name)
