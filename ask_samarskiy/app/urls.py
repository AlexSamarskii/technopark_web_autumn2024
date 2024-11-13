from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('ask/', views.ask, name='ask'),
    path('tag/<slug:tag_name>', views.tag, name='tag'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('question/<int:question_id>', views.question, name='one_question'),
    path('admin/', admin.site.urls),
]
