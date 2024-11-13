from django.db import models
from django.contrib.auth.models import User

class Hotel(models.Model):
    name=models.CharField(max_length=30)
    address=models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
class Booking(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE)
    check_in=models.DateTimeField()
    check_out=models.DateTimeField()

    def __str__(self):
        return f"Hotel name:{self.hotel.name} and name of the person is:{self.user.username}"
