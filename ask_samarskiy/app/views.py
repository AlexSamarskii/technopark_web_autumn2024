import copy
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.auth import authenticate, login
from app.models import Questions, Answers, Tags, Like


# ANSWERS = [
#     {
# 'title': f'Answer {i}',
# 'text': f'Text for answer # {i}',
# 'id': i,
#     } for i in range(10)
# ]
# TAGS = [
#     {
# 'title': f'tag{i}',
# 'index': i
#     } for i in range(10)
# ] 
# QUESTIONS = [
#     {
# 'title': f'Title {i}',
# 'id': i,
# 'text': f'Text for question # {i}',
# 'tags': [TAGS[1], TAGS[5] , TAGS[(i%10)]],
# 'answers': ANSWERS
#     } for i in range(30)
# ]

# fixed = {'best_profiles': Profile.objects.best(), 
#             'popular_tags': Tags.objects.most_popular()}

def paginator(object_list, request, per_page=10):
    required_page = []
    paginator = Paginator(object_list, per_page)
    num_pages = paginator.num_pages
    page = request.GET.get('page')
    try:
        required_page = paginator.get_page(page)
    except PageNotAnInteger:
        required_page = paginator.get_page(1)
    except EmptyPage:
        if(required_page < 1):
            required_page = paginator.get_page(1)
        elif(required_page > num_pages):
            required_page = paginator.get_page(num_pages)
    return required_page    
           

def index(request):
    return render(request, template_name="index.html",
                  context={'questions': paginator(Questions.objects.new(), request)})

def hot(request):
    return render(request, template_name="hot.html",
                  context={'questions': paginator(Questions.objects.hot(), request)})
    
    
def question(request, question_id):
    one_question = get_object_or_404(Questions, pk=question_id)
    answers = Answers.objects.answers_for_question(question_id)
    return render(request, template_name="one-question.html",
                  context={'question': one_question, 'answers': paginator(answers, request, 5)})
    
    
def login(request):
    return redirect(template_name='login.html')

def logout(request):
    next_page = request.GET.get('', '/')
    return redirect(next_page)

def signup(request):
    return render(request, template_name='signup.html')
    
def ask(request):
    return render(request, template_name='ask.html',
                     context={'title': 'New Question'})

def profile(request):
    return render(request, template_name='profile.html')
    
def tag(request, tag_name):
    tag = Tags.objects.get(title=tag_name)
    return render(request, 'tag.html',
                  context={'tag': tag, 'questions': paginator(Questions.objects.by_tag(tag_name), request)})


                  

