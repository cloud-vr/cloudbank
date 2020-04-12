from django.db import models
models.fields

class Client(models.Model):
    fname = models.CharField('First Name', max_length=20)
    lname = models.CharField('Last Name', max_length=20)
    addr = models.CharField('Address', max_length=50)
    acct_num = models.IntegerField('Account Number')
    mobile_num = models.IntegerField('Mobile Number')
    email_addr = models.EmailField('Email Address', max_length=200)

    def __str__(self):
        return self.fname