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
    WITH_VARIANTS = 'WV'
    TEXT_FILL = 'TF'

    KIND_CHOICES = (
        (WITH_VARIANTS, 'С вариантами ответа'),
        (TEXT_FILL, 'Поле ввода'),
    )
    title = models.TextField()
    order = models.IntegerField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    correct = models.CharField(max_length = 50, null = True, default= None)
    kind = models.CharField(max_length = 2, choices = KIND_CHOICES, default = WITH_VARIANTS)
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