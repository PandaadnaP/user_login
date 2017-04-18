# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from tools import RegisterForm, LoginForm
from django.contrib.auth.models import User
from USER_login.models import Questions, Chapters, Difficulty, Cut, WrongQuestions
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
import random
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

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
        question = get_question_not_in_cut(request, 1)
        return render(request, '../templates/exercise_selection.html', {'question': question})
    else:
        return HttpResponseRedirect('login.html')

def exercise_write(request):
    if request.user.is_authenticated():
        question = get_question_not_in_cut(request, 2)
        return render(request, '../templates/exercise_write.html', {'question': question})
    else:
        return HttpResponseRedirect('login.html')

def exercise_calculation(request):
    if request.user.is_authenticated():
        question = get_question_not_in_cut(request, 3)
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
    if request.user.is_authenticated():
        limit = 10
        wrong_questions = WrongQuestions.objects.filter(userid=request.user.id)
        paginator = Paginator(wrong_questions, limit)
        page = request.GET.get('page')

        try:
            wrong_questions = paginator.page(page)  # 获取某页对应的记录
        except PageNotAnInteger:  # 如果页码不是个整数
            wrong_questions = paginator.page(1)  # 取第一页的记录
        except EmptyPage:  # 如果页码太大，没有相应的记录
            wrong_questions = paginator.page(paginator.num_pages)  # 取最后一页的记录

        question_list =[]
        for i in wrong_questions:
            question_list.append(get_question_dict(Questions.objects.get(id=i.questionid)))



        return render_to_response('../templates/wrong_questions.html', {'wrong_questions': wrong_questions,
                                                                        'questions': question_list})
    else:
        return HttpResponseRedirect('login.html')


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

def set_difficulty(user, chapter_id, diff):
    difficulty = Difficulty.objects.get(userid=user.id, chapterid=chapter_id)
    frequecy = difficulty.difficulty_frequency
    difficulty.difficulty_frequency = int(frequecy) + int(diff)
    difficulty.save()

def get_question(request, type_of_question):
    if request.method == 'POST':
        chapter_id = request.POST.get('chapter_id')
        question_id = request.POST.get('question_id')
        if request.POST.has_key('difficulty'):
            diff = request.POST.get('difficulty')
            print chapter_id
            print diff
            set_difficulty(request.user, chapter_id, diff)
        elif request.POST.has_key('cut'):
            exist = Cut.objects.filter(userid=request.user.id, questionid=int(question_id)).count()
            if exist > 0:
                pass
            else:
                Cut.objects.create(userid=request.user.id, questionid=int(question_id))
        elif request.POST.has_key('wrong'):
            exist = WrongQuestions.objects.filter(userid=request.user.id, questionid=int(question_id)).count()
            if exist > 0:
                pass
            else:
                WrongQuestions.objects.create(userid=request.user.id, questionid=int(question_id))


    difficulties = Difficulty.objects.filter(userid=request.user.id)
    difficulties_dict = {}
    for difficulty in difficulties:
        difficulties_dict[difficulty.chapterid] = difficulty.difficulty_frequency
    chapter_id = get_chapter_id(difficulties_dict)
    question_total = Questions.objects.filter(chapter_id=chapter_id, type=type_of_question).count()
    random_get = random.randint(0, question_total-1)
    question_query = Questions.objects.filter(chapter_id=chapter_id, type=type_of_question)[random_get]
    return get_question_dict(question_query)


def get_question_not_in_cut(request, type_of_question):
    question = get_question(request, type_of_question)
    while Cut.objects.filter(questionid=question['question_id']).count() > 0:
        question = get_question(request, type_of_question)
    return question

def get_question_dict(question_query):
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
        'answer': question_query.answer,
        'chapter_id': question_query.chapter_id,
        'question_id': question_query.id
    }
    return question

