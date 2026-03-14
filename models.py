from django.db import models
from django.contrib.auth.models import User

# COURSE PROVIDER
class Cp(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    place = models.CharField(max_length=20)
    post = models.CharField(max_length=20)
    pin = models.CharField(max_length=10)
    district = models.CharField(max_length=20)
    state = models.CharField(max_length=20, default="")
    status = models.CharField(max_length=100)
    proof = models.CharField(max_length=500, default="")
    photo = models.CharField(max_length=500, default="")
    description = models.CharField(max_length=1000, default="")
    USER = models.OneToOneField(User, on_delete=models.CASCADE)

# REGISTRATION
class Registration(models.Model):  # renamed to avoid clash with built-in User
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    dob = models.CharField(max_length=30)
    gender = models.CharField(max_length=30)
    photo = models.CharField(max_length=500)
    place = models.CharField(max_length=20)
    post = models.CharField(max_length=20)
    pin = models.CharField(max_length=10)
    district = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    USER = models.OneToOneField(User, on_delete=models.CASCADE)

# REVIEW
class Review(models.Model):
    review = models.CharField(max_length=30)
    rating = models.CharField(max_length=30)
    date = models.CharField(max_length=30)
    REGISTRATION = models.ForeignKey(Registration, on_delete=models.CASCADE)

# COURSE
class Course(models.Model):
    coursecode = models.CharField(max_length=30,default="")
    coursename = models.CharField(max_length=30,default="")
    duration = models.CharField(max_length=30)
    description = models.CharField(max_length=500,default="")
    CP = models.ForeignKey(Cp, on_delete=models.CASCADE)

# Material
class Material(models.Model):
    materialename = models.CharField(max_length=30,default="")
    File = models.CharField(max_length=30)
    COURSE = models.ForeignKey(Course, on_delete=models.CASCADE)


# COURSEREVIEW
class Creview(models.Model):
    review = models.CharField(max_length=30)
    rating = models.CharField(max_length=30)
    date = models.CharField(max_length=30)
    REGISTRATION = models.ForeignKey(Registration, on_delete=models.CASCADE)
    COURSE=models.ForeignKey(Course, on_delete=models.CASCADE)





# VIDEO
class Video(models.Model):
    videoFile = models.CharField(max_length=200,default="")
    COURSE = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,default="")
    transcribedtext= models.TextField(max_length=65535)
    date = models.DateField()

# JOINING
class Join(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    REGISTRATION = models.ForeignKey(Registration, on_delete=models.CASCADE)
