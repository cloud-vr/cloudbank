from django.db import models

class User(models.Model):
    username = models.CharField('User Name', max_length=200)
    password = models.CharField('Password', max_length=200)
    role = models.CharField('Role', max_length=200)

    def __str__(self):
        return self.username