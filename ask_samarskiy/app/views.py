import copy
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.auth import authenticate, login
from app.models import Question, Answer, Tag, Like, Profile


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
styles = [
                'text-bg-primary', 'text-bg-secondary', 'text-bg-success', 'text-bg-danger',
                'text-bg-warning', 'text-bg-info', 'text-bg-light', 'text-bg-dark'
        ]

fixed = {'best_profiles': Profile.objects.best(), 
            'popular_tags': [[tag, style] for tag, style in zip(Tag.objects.most_popular(), styles)]
}

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
                  context={'questions': paginator(Question.objects.new(), request)} | fixed)

def hot(request):
    return render(request, template_name="hot.html",
                  context={'questions': paginator(Question.objects.hot(), request)} | fixed)
    
    
def question(request, question_id):
    one_question = get_object_or_404(Question, pk=question_id)
    answers = paginator(Answer.objects.answers_for_question(question_id), request, 5)
    return render(request, template_name="one-question.html",
                  context={'question': one_question,
                           'answers': answers} | fixed)
                           
def login(request):
    return redirect(template_name='login.html', 
                    context={'best_profiles': Profile.objects.best(),
                           'popular_tags': Tag.objects.most_popular()})

def logout(request):
    next_page = request.GET.get('', '/')
    return redirect(next_page, 
                    context={'best_profiles': Profile.objects.best(),
                           'popular_tags': Tag.objects.most_popular()})

def signup(request):
    return render(request, template_name='signup.html', 
                  context={'best_profiles': Profile.objects.best(),
                           'popular_tags': Tag.objects.most_popular()})
    
def ask(request):
    return render(request, template_name='ask.html',
                     context={'title': 'New Question'} | fixed)

def profile(request):
    return render(request, template_name='profile.html',
                  context=fixed)
    
def tag(request, tag_name):
    tag = Tag.objects.get(title=tag_name)
    return render(request, 'tag.html',
                  context={'tag': tag, 'questions': paginator(Question.objects.by_tag(tag_name), request)} | fixed)


                  

