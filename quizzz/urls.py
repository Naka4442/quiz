"""quizzz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from main import views as main

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/<int:id>', main.quiz, name="quiz"),
    path('questions/<int:id>', main.questions),
    path('signin/', main.signin, name="signin"),
    path('signup/', main.signup, name="signup"),
    path('quizadd/', main.quizadd),
    path('add_questions/<int:id>', main.add_questions, name="add_questions"),
    path('add_answer/<int:id>', main.add_answer),
    path('profile/', main.profile, name="profile"),
    path('', main.home, name="home"),
    path('delete_question/', main.delete_question),
    path('delete_answer/', main.delete_answer),
    path('edit_question/', main.edit_question, name="edit_question"),
    path('delete_quiz/<int:id>', main.delete_quiz, name="delete_quiz"),
    path('correct_answer/', main.correct_answer),
    path('logout/', main.logout, name="logout"),
    path('complete/<int:id>', main.complete_quiz),
    path('rating/<int:id>', main.rating, name="rating"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)