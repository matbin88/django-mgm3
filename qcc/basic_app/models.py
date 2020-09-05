from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, models.CASCADE)

    admission_number = models.CharField(max_length=10)
    address = models.CharField(max_length=256)
    contact = models.CharField(max_length=10)    

    def __str__(self):
        return self.user.username

class Subject(models.Model):
    subject_name = models.CharField(max_length=25)
    img_url = models.CharField(max_length=256,null=True)

    def __str__(self):
        return self.subject_name

class Topic(models.Model):
    topic_name = models.CharField(max_length=255)
    img_url = models.CharField(max_length=256,null=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)

    def __str__(self):
        return self.topic_name 

class Video(models.Model):
    video_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)

    def __str__(self):
        return self.video_name                

class Frame(models.Model):
    frame_name = models.CharField(max_length=255)
    frame_description = models.TextField(null=True)
    img_url = models.CharField(max_length=256,null=True)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)

    def __str__(self):
        return self.frame_name                

class Question(models.Model):
    question = models.CharField(max_length=255)
    frame = models.ForeignKey(Frame,on_delete=models.CASCADE)

    def __str__(self):
        return self.question

class Option(models.Model):
    option = models.CharField(max_length=255)
    answer = models.BooleanField(default=False)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)

    def __str__(self):
        return self.option

class Test(models.Model):
    name = models.CharField(max_length=255)
    max_questions = models.IntegerField()
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    user_answer = models.ForeignKey(Option,on_delete=models.CASCADE)