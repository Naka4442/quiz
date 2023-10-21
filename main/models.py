from django.db import models

# Create your models here.
class User(models.Model):
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    status = models.IntegerField()
    def __str__(self) -> str:
        return self.name

class Quiz(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField()
    def __str__(self) -> str:
        return self.title

class Question(models.Model):
    title = models.TextField()
    order = models.IntegerField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.title

class Answer(models.Model):
    text = models.TextField()
    correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"{self.text} ({self.question.title})"
    
class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete= models.CASCADE)
    score = models.IntegerField()