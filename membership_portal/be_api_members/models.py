from django.db import models
INTERESTS = (
    ('1', 'Organization & Effectiveness'),
    ('2', 'Projects & Construction'),
    ('3', 'Banking & Finance'),
    ('4', 'Hospitality, Leisure & Tourism'),
    ('5', 'ICT'),
    ('6', 'Legal'),
    ('7', 'Women in Business'),
    ('8', 'Young Professionals'), 
)
# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    logo = models.ImageField(upload_to='main_app/static/uploads', default="")
    cr_number = models.CharField(max_length=20, blank=False, null=False)
    phone_number = models.CharField(max_length=100, blank=False, null=False)
    email_address = models.EmailField(max_length=100, blank=False, null=False)
    sector = models.CharField(max_length=100, blank=False, null=False)
    website = models.CharField(max_length=100)
    address_1 = models.CharField(max_length=100, blank=False, null=False)
    address_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=False, null=False)
    # country = models.CharField(max_length=100)
    zip_code = models.IntegerField(blank=False, null=False)
    content_info = models.TextField(max_length=250, blank=False, null=False)
    interests = models.CharField(max_length=1, choices=INTERESTS, default=INTERESTS[0][0])
    # assistant = models.CharField()
    # admin = models.CharField()

    def __str__(self):
        return self.name