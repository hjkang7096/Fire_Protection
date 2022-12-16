# Generated by Django 4.0 on 2022-10-30 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_zipcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='zipcode',
            field=models.CharField(blank=True, help_text='검색버튼을 눌러 주소를 입력해주세요!', max_length=10, null=True),
        ),
    ]