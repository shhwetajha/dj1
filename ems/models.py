from django.db import models

# Create your models here.

class Student(models.Model):
    name=models.CharField(max_length=50)
    age=models.IntegerField()
    rollno=models.IntegerField()
    file=models.FileField(upload_to="C:/Users/dell/OneDrive/Desktop/django1/djangoall/djangonew/dj1/",max_length=550,null=True,blank=True)


    def __str__(self):
        return self.name