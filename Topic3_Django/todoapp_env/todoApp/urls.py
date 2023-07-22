from django.urls import path, re_path  # all new
from . import views
from .views import logout_view
from django.conf.urls import include

# relevant information from browser to view and view to browser will be
# carried on these respective urls name have complete html template name 
# that view will send to browser
# views.home --> home is view name for that respective html template
# when request is passed from bowser html page it will be taken to that view
# travel on that respective rl of each e.g. for home page url will be basic as we have not added extra path
# like: 127.0.0.0.8000 (8000 is port name on which you are running app)
# for signup 127.0.0.0.800/signup/

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('loginpage/', views.loginpage, name='loginpage'),
    path("todolist/", views.todolist, name='todolist'),
    path('logout/', logout_view, name='logout'),
    # here we are creating a url by passing each todolisid with todolist url
    # it will be like that 127.0.0.0.8000/todolist/1 -->for id 1
    # and on that url todoitem template will be displayed and
    # todoitem view will be processed
    re_path(r"^todolist/(?P<listid>[0-9]+)$", views.todoitem, name='todoitem'),
]