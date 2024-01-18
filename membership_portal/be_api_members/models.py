from django.db import models

# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=100)
    emailAddress = models.EmailField(max_length=100)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    # class Meta:
    #     permissions = (("change_org_name_"))
    
class Country(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=20)
    nationality_name = models.CharField(max_length=40)
    flag = models.CharField(max_length=200)
    capital = models.CharField(max_length=200)
    currency = models.CharField(max_length=100)
    currency_sign = models.CharField(max_length=20)
    country_code = models.CharField(max_length=4)
    listed = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Countries'