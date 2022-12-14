from django.db import models
from django.contrib.auth.models import AbstractUser


class Agent(AbstractUser):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    # phone_no =
    about = models.TextField(null=True, blank=True)
    skype = models.URLField(null=True, blank=True) # Skype username
    avatar = models.ImageField(null=True, blank=True, default='avatar.svg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class HouseType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class HouseStatus(models.Model):
    type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.type


class House(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True, default='Country | State')
    house_type = models.ForeignKey(HouseType, on_delete=models.CASCADE, null=True, blank=True)
    price = models.FloatField()
    description = models.TextField()  # Change to CKEditor later
    image_one = models.ImageField(null=True, blank=True)
    image_two = models.ImageField(null=True, blank=True)
    image_three = models.ImageField(null=True, blank=True)
    no_of_bedrooms = models.IntegerField()
    area_per_meter_square = models.IntegerField()
    no_of_bathroom = models.IntegerField()
    garage = models.BooleanField(default=False)
    status = models.ForeignKey(HouseStatus, on_delete=models.CASCADE, null=True, blank=True)
    balcony = models.BooleanField(default=False)
    deck = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    outdoor_kitchen = models.BooleanField(default=False)
    tennis_court = models.BooleanField(default=False)
    sun_room = models.BooleanField(default=False)
    cable_tv = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    concrete_flooring = models.BooleanField(default=False)
    # count =
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.agent.username

    @property
    def image_one_url(self):
        try:
            url = self.image_one.url
        except:
            url = ''
        return url

    def image_two_url(self):
        try:
            url = self.image_two.url
        except:
            url = ''
        return url

    def image_three_url(self):
        try:
            url = self.image_three.url
        except:
            url = ''
        return url

    class Meta:
        ordering = ['-created']

