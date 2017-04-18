# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from tools import RegisterForm, LoginForm
from django.contrib.auth.models import User
from USER_login.models import Questions, Chapters, Difficulty
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
import random

import django
django.setup()

# Create your views here.

def home_page(request):
    return render(request, '../templates/home_page.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():  # 如果提交的数据合法
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(username, email, password)
            chapters = Chapters.objects.all()
            for chapter in chapters:
                Difficulty.objects.create(chapterid=chapter.id, userid=user.id, difficulty_frequency=100)

            user.save()

            return HttpResponseRedirect('login.html')
    else:
        form = LoginForm()
    return render(request, '../templates/register.html')

def forgot_password(request):
    return render(request, '../templates/forget_password.html')

def exercise_selection(request):
    if request.user.is_authenticated():
        difficulties = Difficulty.objects.filter(userid=request.user.id)
        difficulties_dict = {}
        for difficulty in difficulties:
            difficulties_dict[difficulty.chapterid] = difficulty.difficulty_frequency
        chapter_id = get_chapter_id(difficulties_dict)
        question_total = Questions.objects.filter(chapter_id=chapter_id, type=1).count()
        random_get = random.randint(0, question_total)
        question_query = Questions.objects.filter(chapter_id=chapter_id, type=1)[random_get]
        difficulty_1 = []
        difficulty_2 = []
        for i in range(question_query.difficulty):
            difficulty_1.append(i)
        for i in range(5 - question_query.difficulty):
            difficulty_2.append(i)
        question = {
            'difficulty_1': difficulty_1,
            'difficulty_2': difficulty_2,
            'create_date': question_query.created_at,
            'description': question_query.description,
            'answer': question_query.answer
        }
        return render(request, '../templates/exercise_selection.html', {'question': question})
    else:
        return HttpResponseRedirect('login.html')

def exercise_write(request):
    if request.user.is_authenticated():
        difficulties = Difficulty.objects.filter(userid=request.user.id)
        difficulties_dict = {}
        for difficulty in difficulties:
            difficulties_dict[difficulty.chapterid] = difficulty.difficulty_frequency
        chapter_id = get_chapter_id(difficulties_dict)
        question_total = Questions.objects.filter(chapter_id=chapter_id, type=2).count()
        random_get = random.randint(0, question_total)
        question_query = Questions.objects.filter(chapter_id=chapter_id, type=2)[random_get]
        difficulty_1 = []
        difficulty_2 = []
        for i in range(question_query.difficulty):
            difficulty_1.append(i)
        for i in range(5 - question_query.difficulty):
            difficulty_2.append(i)
        question = {
            'difficulty_1': difficulty_1,
            'difficulty_2': difficulty_2,
            'create_date': question_query.created_at,
            'description': question_query.description,
            'answer': question_query.answer
        }
        return render(request, '../templates/exercise_write.html', {'question': question})
    else:
        return HttpResponseRedirect('login.html')

def exercise_calculation(request):
    if request.user.is_authenticated():
        difficulties = Difficulty.objects.filter(userid=request.user.id)
        difficulties_dict = {}
        for difficulty in difficulties:
            difficulties_dict[difficulty.chapterid] = difficulty.difficulty_frequency
        chapter_id = get_chapter_id(difficulties_dict)
        question_total = Questions.objects.filter(chapter_id=chapter_id, type=3).count()
        random_get = random.randint(0, question_total)
        question_query = Questions.objects.filter(chapter_id=chapter_id, type=3)[random_get]
        difficulty_1 = []
        difficulty_2 = []
        for i in range(question_query.difficulty):
            difficulty_1.append(i)
        for i in range(5 - question_query.difficulty):
            difficulty_2.append(i)
        question = {
            'difficulty_1': difficulty_1,
            'difficulty_2': difficulty_2,
            'create_date': question_query.created_at,
            'description': question_query.description,
            'answer': question_query.answer
        }
        return render(request, '../templates/exercise_calculation.html', {'question': question})
    else:
        return HttpResponseRedirect('login.html')

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():  # 如果提交的数据合法
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('exercise_selection.html')
            else:
                # 此处应当返回一个错误给前端，显示用户名或密码错误
                error = r'<p><p>hahahjK</p></p>'
                return render(request, '../templates/login.html', {'error_message': error})
    else:
        form = LoginForm()
    return render(request, '../templates/login.html')

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('home_page.html')

def user_info(request):
    return render(request, '../templates/information.html')

def wrong_question_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():  # 如果提交的数据合法
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('exercise_selection.html')
            else:
                # 此处应当返回一个错误给前端，显示用户名或密码错误
                error = r'<p><p>用户名或密码不正确</p></p>'
                return render(request, '../templates/login.html', {'error_message': error})
    else:
        form = LoginForm()
    return render(request, '../templates/login.html')

def get_chapter_id(dic_of_chapter):
    chapters = []
    frequencies = []
    max_frequency = 0
    for chapter, frequency in dic_of_chapter.items():
        chapters.append(chapter)
        max_frequency += frequency
        frequencies.append(max_frequency)

    get_frequency = random.randint(1, max_frequency)

    for chapter, frequency in zip(chapters, frequencies):
        if get_frequency < frequency:
            return chapter