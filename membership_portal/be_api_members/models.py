from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

martial_Status = (
    ('Mr.','Mr.'),
    ('Ms.','Ms.'),
    ('Miss.','Miss.'),
    ('Dr.','Dr.')
)

status = (
    ('A','Active'),
    ('NA','Not Active')
)
# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=100)
    emailAddress = models.EmailField(max_length=100)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'fs_business_mvt/static/uploads',default = "",blank=False,null=False)
    dob = models.DateField('Date of Birth')
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    email = models.EmailField(max_length = 100)
    # TO BE ADDED WHEN THE SALUTAION DATA IS AVAILABLE / comment by : Hussain
    # salutation = models.OneToOneField(Salutation,on_delete=models.CASCADE)
    martial = models.CharField(
        choices = martial_Status,
        default = ""
        )
    nationality = models.CharField(max_length=100)
    gender = models.CharField(choices = (('Male','Male'),('Female','Female')))
    orgnization = models.OneToOneField(Organization, on_delete = models.CASCADE)
    role = models.IntegerField(
        validators = [
            MaxValueValidator(4),
            MinValueValidator(1)
        ]
    )
    job_title = models.CharField(max_length = 100)
    status = models.CharField(
        choices = status,
        default = status[0][0]
    )
    

    
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
    country_code = models.CharField(max_length=5)
    listed = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Countries'

