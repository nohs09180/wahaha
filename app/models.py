from django.db import models
import sys
sys.path.append('../')
from users.models import User
from django.utils import timezone
from django.contrib.auth import get_user_model
# from django.core.validators import validate_comma_separated_integer_list
import numpy as np
from django.db import models
from ndarraydjango.fields import NDArrayField

User = get_user_model()

class Video(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100, default='no setting')
    video_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class SmileData(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    # data = models.CharField(validators=[validate_comma_separated_integer_list], max_length=100)
    # data = NDArrayField()
    data = models.CharField(max_length=1000)
    data_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.person} {self.video} {self.data}'
        # return f'{self.person} {self.video} {self.data_joined.month} {self.data_joined.day} {self.data_joined.hour} {self.data_joined.minute}'
        
class SmileRate(models.Model):
    user = models.CharField(max_length=100)
    video = models.CharField(max_length=100)
    smile_rate = models.DecimalField(max_digits=3, decimal_places=1)
    joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user} {self.video} {self.smile_rate}'

class SmileDosData(models.Model):
    user1 = models.CharField(max_length=100)
    user2 = models.CharField(max_length=100)
    video = models.CharField(max_length=100, default='no video')
    smile_dos = models.DecimalField(max_digits=4, decimal_places=1)
    joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user1} {self.user2} {self.video} {self.smile_dos}'

class SmileDos(models.Model):
    user1 = models.CharField(max_length=100)
    user2 = models.CharField(max_length=100)
    smile_dos = models.DecimalField(max_digits=4, decimal_places=1)
    joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user1} {self.user2} {self.smile_dos}'

