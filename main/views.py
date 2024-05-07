from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Quiz, Question, Answer, User, QuizResult
from .forms import Signupform, Signinform, Quizform
from .gpt import get_question
from random import randint

import json
# Create your views here.
def quiz(request, id):
    user = request.session.get("user", False)
    quiz = Quiz.objects.get(id=id)
    return render(request, "quiz.html",{"quiz":quiz, "user":user})

def neuro_quiz(request):
    user = request.session.get("user", False)
    return render(request, "neuro-quiz.html",{"user":user})

def neuro_question(request, theme):
    question = get_question(theme, randint(2, 4))
    print(question)
    return HttpResponse(question, content_type="application/json")

def questions(request, id):
    quiz = Quiz.objects.get(id=id)
    questions = Question.objects.filter(quiz=quiz)
    result = [{
        "text" : question.title,
        "kind" : question.kind,
        "correct" : question.correct,
        "answers" : [
            {
                "text" : answer.text,
                "correct" : answer.correct
            } 
            for answer in Answer.objects.filter(question=question)
        ]
    } for question in questions]
    return HttpResponse(json.dumps(result), content_type="application/json")

def signin(request):
    if request.method == "GET":
        form = Signinform()
        return render(request, "signin.html", {"form": form} )
    elif request.method == "POST":
        form = Signinform(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.filter(login=data.get("login"), password=data.get("password"))
            if len(user) == 1:
                request.session["user"] = {"name" : user.last().name, "login" : user.last().login, "status" : user.last().status, "id" : user.last().id}
                return redirect("home")
            else:
                return render(request, "signin.html", {"form" : "Неправильное сочетание логина и пароля"})
        else:
            return render(request, "signin.html", {"form": "Ошибка в данных"} )

def signup(request):
    if request.method == "GET":
        form = Signupform()
        return render(request, "signup.html", {"form": form} )
    elif request.method == "POST":
        form = Signupform(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            login, email = data.get("login"), data.get("email")
            users = User.objects.filter(login=login)
            if len(users) == 0:
                user = User()
                user.login = login
                user.email = email
                user.password = data.get("password")
                user.name = data.get("name")
                user.status = 2
                user.save()
                return redirect("signin")
            else:
                return render(request, "signup.html", {"form": "Такой пользователь уже есть"} )
        else:
            return render(request, "signup.html", {"form": "Ошибка в данных"} )

def home(request):
    quizes = Quiz.objects.all()
    user = request.session.get("user", False)
    return render(request, "home.html", {"quizes":quizes, "user" : user})

def profile(request):
    user = request.session.get("user", False)
    if user:
        user = User.objects.get(id=user.get("id"))
        quizes = Quiz.objects.filter(author=user)
        return render(request, "profile.html", {"user" : user, "quizes" : quizes})
    else:
        return redirect("signin")
        
def quizadd(request):
    if request.method == "GET":
        form = Quizform()
        return render(request, "quizadd.html", {"form" : form})
    elif request.method == "POST":
        form = Quizform(request.POST, request.FILES)
        print(request.POST, request.FILES.get("image"))
        if form.is_valid():
            data = form.cleaned_data
            quiz = Quiz()
            quiz.title = data.get("title")
            quiz.image = request.FILES.get("image")
            quiz.author = User.objects.get(id=request.session.get("user").get("id"))
            quiz.save()
            return HttpResponse("Викторина добавлена")
        return HttpResponse("Ошибка")

def add_questions(request, id):
    if request.method == "GET":
        quiz = Quiz.objects.get(id=id)
        questions = [{
            "id" : question.id,
            "title" : question.title,
            "kind" : question.kind,
            "correct" : question.correct,
            "answers" : [
                {
                    "id" : answer.id,
                    "text" : answer.text,
                    "correct" : answer.correct
                } 
                for answer in Answer.objects.filter(question=question)
            ]
        } for question in Question.objects.filter(quiz=quiz)]
        return render(request, "questions.html", {"questions" : questions, "quiz" : quiz})
    elif request.method == "POST":
        data = json.loads(request.body)
        
        quiz = Quiz.objects.get(id=id)
        questions = Question.objects.filter(quiz=quiz)
        order = questions.last().order if len(questions) > 0 else 1
        question = Question()
        title = data.get("title")
        kind = data.get("kind")
        if len(title) == 0:
            return HttpResponse(json.dumps({"result" : False}))
        question.title = title
        question.kind = kind
        question.order = order
        question.quiz = quiz
        question.save()
        return HttpResponse(json.dumps({"result" : True}))

def add_answer(request, id):
    data = json.loads(request.body)
    question = Question.objects.get(id=id)
    title = data.get("title")
    if len(title) == 0:
        return HttpResponse(json.dumps({"result" : False}))
    if question.kind == "TF":
        question.correct = title
        question.save()
        return HttpResponse(json.dumps({"result" : True}))
    else:
        answer = Answer()
        answer.question = question
        answer.text = title
        answer.correct = False
        answer.save()
        return HttpResponse(json.dumps({"result" : True}))

def correct_answer (request):
    data = json.loads(request.body)
    answer = Answer.objects.get(id=data.get("id"))
    # Если нужно сделать все вопросы неправильными
    # all_answers = Answer.objects.filter(question = answer.question)
    # for ans in all_answers:
    #     ans.correct = False
    #     ans.save()
    answer.correct = not answer.correct
    answer.save()
    return HttpResponse(json.dumps({"result" : True}))

def delete_question (request):
    data = json.loads(request.body)
    question = Question.objects.get(id=data.get("id"))
    question.delete()
    return HttpResponse(json.dumps({"result" : True}))

def edit_question(request):
    data = json.loads(request.body)
    question = Question.objects.get(id=data.get("id"))
    question.title = data.get("title")
    question.save()
    return HttpResponse(json.dumps({"result" : True}))

def delete_quiz (request, id):
    user = request.session.get("user", False)
    quiz = Quiz.objects.get(id=id)
    if quiz.author == User.objects.get(id=user.get("id")):
        quiz.delete()
    return redirect("profile")
    

def complete_quiz(request, id):
    data = json.loads(request.body)
    score = int(data.get("score"))
    quiz = Quiz.objects.get(id=id)
    session_user = request.session.get("user", False)
    if session_user:
        user_id = session_user.get("id")
        user = User.objects.get(id=user_id)

        result_exist = QuizResult.objects.filter(quiz = quiz, user = user)
        if len(result_exist) == 0:
            result = QuizResult()
            result.user = user
            result.quiz = quiz
            result.score = score
            
        else:
            result = result_exist.first()
            if result.score < score:
                result.score = score
        result.save()
        return HttpResponse(json.dumps({"result" : True}))
    return HttpResponse(json.dumps({"result" : False}))


def logout (request):
    request.session.pop("user")
    return redirect("home")

def rating(request, id):
    quiz = Quiz.objects.get(id = id)
    results = QuizResult.objects.filter(quiz = quiz).order_by("-score")
    session_user = request.session.get("user", False)
    if session_user:
        user_id = session_user.get("id")
        user = User.objects.get(id=user_id)
    else:
        user = False
    return render(request, "rating.html", {"results" : results, "quiz" : quiz, "user" : user})

def delete_answer (request):
    data = json.loads(request.body)
    mode = data.get("mode")
    if mode == "TF":
        question = Question.objects.get(id=data.get("id"))
        question.correct = None
        question.save()
        return HttpResponse(json.dumps({"result" : True}))
    elif mode == "WV":
        answer = Answer.objects.get(id=data.get("id"))
        answer.delete()
        return HttpResponse(json.dumps({"result" : True}))

