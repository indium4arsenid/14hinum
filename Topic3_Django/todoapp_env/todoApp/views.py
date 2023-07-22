from . import models
from datetime import datetime
from django.db.models import F
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect    # all new
from .forms import TodoListForm, TodoItemForm
from .models import TodoListModel, TodoItem, Owner
from django.core.exceptions import ValidationError
from django.contrib.auth import login, authenticate #add this
from django.contrib.auth.forms import AuthenticationForm #add this
from django.contrib.auth.decorators import login_required


#------------------- home view --------------------- +
''' - It is related to the home template that is main page and have sign up and sign in buttons
    - home function in view
    - its correspondance url in urls.py file --> path('', views.home, name='home')
    - its template in --> todoApp -> templates ->todoApp -> home.html
    - request is an object in django web-based frame work that takes all information from web browser
    - and brings that information to backend like here in home function
    - e.g what the user requested in browser or sent from browser to process (like POST, GET, form etc) 
    - it brings all information in view and all the functionalty
    - is performed in view accordingly and the response is sent back to browser
    - like here home function is view that takes the request and pass relevant html page that will 
    - display in browser with all functionality required 
    - as the view render the html will be passed to browser here more information and attriutes
    - can be passes to dispaly in browser
    - every view have its corresponding url in urls.py file
'''

def home(request):
    # render function always takes the request as its first object
    return render(request, 'todoApp/home.html')

#------------------- logout view --------------------- +
''' - logout view does not have any associated html template
    - It just takes the url request and logut user using django builtin logout function 
    - we import django logout function here -> from django.contrib.auth import logout
    - its correspondance url in urls.py file --> path('logout/', logout_view, name='logout'),
    - Whene we linked that url to logout button in html templates, browser will sent a request
    - on this url and brings that request to logout_review and return response after performing
    - the functionality in in this view 
    - e.g. here in loginpage.html <a href="{% url 'logout' %}" class="btn 
                                    btn-danger mt-2 mr-2 logout-button logout-custom">Logout</a>
    - we are calling this view url and, logut_view will process our request and respond to rowser accordingly
    - Lets proceed step by step how it will work and respond
    - When it receive logout request, It checks if user is logged in using user.is_authenticated function
    - if the condition is correct successfully logut user and pass a message in browser
    - we are displaying those messages in browser like that {% if messages %}  
    - if the condition is false pass another message and dont process logout function
    - once the request is processed we need to preview user some page
    - so we will keep the user on the same page from which the logout request is called  
'''

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have successfully logged out.")
        
    else:
        messages.error(request, "You are not logged in.")

    # Get the URL from where the request is made
    previous_page = request.META.get('HTTP_REFERER')
    
    if previous_page == "http://127.0.0.1:8000/signup/":
        return HttpResponseRedirect(previous_page)
    if previous_page == "http://127.0.0.1:8000/todolist/":
        return redirect('loginpage')
    else:
        return redirect('loginpage')

#------------------- loginpage view --------------------- +
''' - It is login page that have login form
    - loginpage function in view
    - its correspondance url in urls.py file --> path('loginpage/', views.loginpage, name='loginpage'),
    - its template in --> todoApp -> templates ->todoApp -> loginpage.html
    - loginpage view take POST request from browser when user submit different fields in form
    - Lets proceed step by step how it will work and respond
    - In the first step it will check if the request sent from the html template is POST
    - if user clicks on subimt button of form in browser it will be POST else it will be GET
    - e.g. when user reload page it will be GET request
    - <form>All fields data to be submitted <submit button></form> that's how we create form in html
    - once user clicks submit button request will passed here it will proceed and check for all
    - required fields in form, (all the fields inside form tag will carry information here)
    - it will check for username and password in POST request .get('username') here attribute name
    - must be same as name="username" in html input field
    - <input type="text" class="form-control" name="username" id="username" placeholder="Enter username">
    - next using django builtin authenticate function it will verify if user exists in database
    - with same name and password
    - if the authentification is successful it will proceed login request using django builtin login function
    - "from django.contrib.auth import login, authenticate" here we import these functions
    - once the user is successfully logged in it will be directly move to todolist template in browser
    - if the authenciation is failed the user will be notify with a message in browser
    - note that all these steps will proceed only if request is POST
    - last code line will proceed even if the POST request is flase and view does not return anything before
    - it will return the same loginpage template and will pass extra information as a context
    - that is user authentication function -> request.user.is_authenticated
    - this function sent in browser will be used to authenticate user in browser under different conditions
    - e.g. here in login in template we are using this function to valide user login to generate an alert 
    - or move to next page, if user clicks "Todolist" link it will move to that page only if the user is logged in
    - in other case it will show an alert for login
    -           {% if user.is_authenticated %}
                    <a href="{% url 'todolist' %}" class="forward-link">TodoList</a>
                {% else %}
    
                    <a href="#", onclick="loginAlert()", class="forward-link">TodoList</a>
                {% endif %}
'''

def loginpage(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("todolist")
        else:
            messages.error(request,"Invalid username or password.")

    return render(request=request, template_name="todoApp/loginpage.html", context={"user_authenticated": request.user.is_authenticated})

#------------------- signup view --------------------- +
'''
    - It is signup page that have signup form
    - signup function in view
    - its correspondance url in urls.py file --> path('signup/', views.signup, name='signup'),
    - its template in --> todoApp -> templates ->todoApp -> signup.html
    - signup view takes POST request from browser when user submit different fields in form
    - Lets proceed step by step how it will work and respond
    - In the first step it will check if the request sent from the html template is POST
    - we discussed above POST and GET requests and how it works
    - it will get all attributes of form from get request
    - username, email, password and confirm password fields
    - it will check if passwords enters are same, if not it will prompt a message
    - and return user to the same page in browser
    - next it will create new user in database by default that allow user to be stored only if
    - the user name does not exist in database
    - Owner is our model that inherit dajango USER class
    - it allows us to create user in database with all the given attributes
    - if the user creation in databse is successful it will pass login request and open todolist in browser
    - if the user creation failed it will generate Integrity error message
    - and return to same page
    - In other case if request is not POST it will just return the same signup page

'''

def signup(request):
    """SignUp page view that signs up new user to the system, according to given information."""

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['confirm-password'] 
        if password != password_confirm:
            messages.error(request,"Password does not match. Please try again.")
            return HttpResponseRedirect(request.get_full_path())        
        try:
            user = Owner.objects.create_user(username, email, password)
            login(request, user)
            return redirect('todolist')
        except IntegrityError:
            messages.error(request,"Oops! It seems like this username is taken, "
                "please choose another username.")
            return HttpResponseRedirect(request.get_full_path())
            
    else:
        return render(request, 'todoApp/signup.html')

#------------------- todolist view --------------------- +
'''
   - There are multiple code blocks in todolist view for add, delete and edit that will work based on which POST request is True
   - if the user generates request for edit, edit or create operation the request will process accrodingly
   - Let's move step by step
   - @login_required(login_url='loginpage') it is used to authenticate if a user is logged in
   - user will be able to access this todolist view and page only if user is logged in 
   - if user try to access page and not logged in it will generate error so to avoid that error and
   - pass user to back on login page with message we have used login url
   - Owner is our model for user, it is basically database table that stores each user login information

'''

@login_required(login_url='loginpage')
def todolist(request):
    # filter the user from database which username and password is passed in login request
    # all the attributes of a table are its objects we will use filter to access only that user
    # As each user can create their own todolist so it will help to show in browser only logged in user todolist
    owner = Owner.objects.filter(username=request.user)[0]
    # it creates an instance of TodoListForm object this is form that we declared in forms.py file
    # Form will take POST request information from todolist page and will populate all form attriutes
    # with the given information, if there is no POST request it will make an empty form with all
    # required attributes, all attributes of TodoListForm form are defined in forms.py
    # after processing this line we will have a form that may be empty or populated
    form = TodoListForm(request.POST or None)

    #------------------------- add operation ------------------------+
    ''' - It wil work from the todolist template where we are entering a new todolist name, deadline and 
    - clicking on add button that will generate a POST request to the todolist view function
    - and brings the attributes information as we can see from forms.py TodoListForm required two attributes
    - fields = ['listname', 'deadline']
    - we have multiple POST requests from browser so we will handle each separately based on its 
    - specific name, at first we will check if the request is POST, then if "add" name is in request
    - here in todolist.html we assign a specific name -> name ="add" to each submit request to distinct 
    - all of these   <button type="submit" name ="add" value="add" class="btn btn-primary 
                                                 btn-lg ml-2" style="width: 120px;">Add</button>
    - after filtering the relevant POST request, it will check if form contains information
    - and extract specific attributes values based on there names

    '''
    
    if request.method == "POST":
        if 'add' in request.POST:
            if form.is_valid():
                listname = form.cleaned_data['listname']
                deadline = form.cleaned_data['deadline']
                # TodoListModel is our object instance, model that is created in models.py file
                # in generic this table will have all users todolist information
                # distinguishing all based on relations between owner and todolistmodel
                # from that table we will filter information that belongs to only logged in user
                # .exists() will check if that listname we received in form already exists in table
                # genererate an error message
                if TodoListModel.objects.filter(owner=owner, listname=listname).exists():
                    messages.error(request,"Create operation failed. Please make sure that your"\
                                       " TodoList name does not exist in current TodoLists")
                # if the name does not exist in table
                else:
                    try:
                        # here we are assigning unique listids to all listnames
                        # if there is no instance in that table keep it 0
                        if TodoListModel.objects.count() == 0:
                            newlistid = 0
                        else:
                            # get the current listid and increment listid by 1
                            newlistid = TodoListModel.objects.latest('listid').listid + 1
                        # save the new information we get in form in database
                        new_todo_list = form.save(commit=False)
                        # as our table has more attributes other than two form attributes
                        # that we declared in models.py
                        # we need to save all those attributes information as well
                        # keep newlistd value in form object
                        new_todo_list.listid = newlistid
                        # keep owner information
                        new_todo_list.owner = owner
                        # and initially keep the total count of list names 0
                        new_todo_list.todocount = 0
                        # save new inforamtion of all attributes it will by default commit and update database
                        new_todo_list.save()
                        # return the user to todolist template back in browser
                        return redirect('todolist')
                        # try block will not work if the todolist name creation failed and listname already exists in database
                        # so exception will generate integrity message
                    except IntegrityError:

                        messages.error(request,"Create operation failed. Please make sure that your"\
                                       " TodoList name does not exist in current TodoLists")
        
        #------------------------- delete operation ------------------------+
            '''  - check if the request is for delete operation
          - get the list of specific listname listids which were asked to delete
          - we have added functionality in todolist html that when user check or select the row in 
          - table that is displayed in browser get the specific listid that is assigned to each checkbox
          - in that row take that id and pass with submit POST request so if the request is for delete
          - it will be processed based on those specific ids and delete that ids and corresponding 
          - values from table in databse, we have created todolist one to many relation with todoitems
          - as it makes sense one todolist name can have many todos but many todos can have only one 
          - specific listname, so based on this relationship when the todolist name is deleted its 
          - corresponding todoitems will also be deleted

        '''
        elif 'delete' in request.POST:  
            # get the ids
            todolist_ids = request.POST.getlist('listid')
            # filter the rows from table where listid match
            # get the todo items to delete
            todolist_ids_to_delete = TodoListModel.objects.filter(listid__in=todolist_ids)
            # count the items that are requested to delete
            items_count = todolist_ids_to_delete.count()
            # delete the todo items
            todolist_ids_to_delete.delete()

        #------------------------- edit operation ------------------------+
        elif 'edit' in request.POST:
            # we have created a functionality in todolist html template that when user check the 
            # specific row to edit it will get that value based on listid and allow a user to edit 
            # edited value will be stored in hidden field that have name 'edited_value' and will pass with
            # POST request, here we will get id and new value from POST request and process
            edited_value = request.POST.get('edited_value')
            list_id = request.POST.getlist('listid')
            # check if new value does not have any valid character generate error message
            if not(edited_value and any(c.isalpha() for c in edited_value)):
                messages.error(request,"Create operation failed. Please enter a valid"\
                                       " TodoList name")
                # return the same page
                return HttpResponseRedirect(request.get_full_path())
            # if there is a valid value filter it from the table and check if already exists
            # generate error message
            elif TodoListModel.objects.filter(owner=owner, listname=edited_value).exists():
                messages.error(request,"Edit operation failed. Please make sure that your"\
                                       " TodoList name does not exist in current TodoLists")
                return HttpResponseRedirect(request.get_full_path())
            # if the value is valid filter that vlaue from table based on its lisid
            # and update that id listname with new list name
            else:
                TodoListModel.objects.filter(listid=list_id[0]).update(listname=edited_value)
           
    # ------------------------ if POST request is false ------------+
    # note that all above operations will work only if any of the post request is True
    # in other case it will make an empty form object
    else:
        form = TodoListForm()

    # --------------------- final block ----------------------------+
    # it will process either any condition is true or false
    # but it will contain information based on which operation processed above
    # filter the todolist of logged in owner
    todo_lists = models.TodoListModel.objects.filter(owner=owner)
    # make a context dictionary that will keep updated todo_lists information and form
    context = {'todo_lists': todo_lists, 'form': form}
    # after procssing the user request in view todolist template will be passed to browser
    # and todolist updated information will be passed
    # as you can see we displayed user todolist information in table form in browser
    # it will updated based on what's updated in database
    # that functionaly processed here as we pass the updated information and display in browser
    return render(request, 'todoApp/todolist.html', context)


#------------------- todoitem view --------------------- +
'''
   - There are multiple code blocks in todoitem view for add, delete, open and edit that will work based on which POST request is True
   - if the user generates request for edit, delete, done or create operation the request will process accrodingly
   - Let's move step by step
   - @login_required(login_url='loginpage') it is used to authenticate if a user is logged in
   - user will be able to access this todoitem view and page only if user is logged in 
   - if user try to access page and not logged in it will generate error so to avoid that error and
   - pass user to back on login page with message we have used login url
   - Owner is our model for user, it is basically database table that stores each user login information

'''
@login_required(login_url='loginpage')
def todoitem(request, listid=None):
    # filter logged in user from database
    owner = Owner.objects.filter(username=request.user)[0]
    # being in this view means we came from todolist page by selecting a specific todolistname
    # and working on that todolistname either adding or updating todos for that specific listname
    # get the listname and deadline of the todolist for which we are adding todos
    listname = TodoListModel.objects.filter(owner=owner, listid=listid).values('listname')[0]['listname']
    deadline = TodoListModel.objects.filter(owner=owner, listid=listid).values('deadline')[0]['deadline']
    # make a form instance based on request
    form = TodoItemForm(request.POST or None)
    # if request is POST move further
    if request.method == "POST":

       #------------------------- add operation ------------------------+
        ''' - It wil work from the todoitem template where we are entering a new todoitem name and 
    - clicking on add button that will generate a POST request to the todoitem view function
    - and brings the attributes information as we can see from forms.py TodoItemForm required one attributes
    - fields = ['newtodo']
    - we have multiple POST requests from browser so we will handle each separately based on its 
    - specific name, at first we will check if the request is POST, then if "add" name is in request
    - after filtering the relevant POST request, it will check if form contains information
    - and extract specific attributes values based on there names

    '''
        if 'add' in request.POST:
            # TodoItem is our object instance, model that is created in models.py file
            # in generic this table will have all users todoitem information
            # distinguishing all based on relations between ownertodos_id 
            # from that table we will filter information that belongs to only logged in user
            # .exists() will check if that listname we received in form already exists in table
            # genererate an error message
            if form.is_valid():
                newtodo = form.cleaned_data['newtodo']
                # check if the newtodo already exists in the ownertodos list for the current user
                if TodoItem.objects.filter(newtodo=newtodo, ownertodos_id=listid).exists():
                    # generate error message
                    messages.error(request, "Please choose a Todo name which does not exist in your current set of Todo and Done Tasks.")
                else:
                    try:
                        # whenever user enters a new todo name update the total count of todos in TodoListModel 
                        TodoListModel.objects.filter(listid=listid, owner=owner).update(todocount=F('todocount') + 1)
                        # save the ne form information
                        new_todo = form.save(commit=False)
                        # assign values to specific attributes
                        new_todo.newtodo = newtodo
                        # initially set done value to false
                        new_todo.done = False
                        # linking with the TodoListModel
                        new_todo.ownertodos = TodoListModel.objects.get(listid=listid) 
                        # save updated information in database
                        new_todo.save()
                        # get the associated todo list and increment its todocount
                        todo_list = TodoListModel.objects.get(listid=listid)
                        # save updated todolist table
                        todo_list.save()
                    # try block will not work if the newtodo creation failed and todoitem already exists in database
                    # so exception will generate integrity message
                    except IntegrityError:
                        
                        messages.error(request,"Create operation failed. Please make sure that your Todo content " \
                                "does not exist in current or done Todos.")
                        return HttpResponseRedirect(request.get_full_path())
                        
        #------------------------- delete operation ------------------------+
            '''  - check if the request is for delete operation
          - get the list of specific todo todoids which were asked to delete
          - we have added functionality in todoitem html that when user check or select the row in 
          - table that is displayed in browser get the specific todoid that is assigned to each checkbox
          - in that row take that id and pass with submit POST request so if the request is for delete
          - it will be processed based on those specific ids and delete that ids and corresponding 
          - values from table in databse

         '''

        elif 'delete' in request.POST: 
            # get the ids
            todolist_ids = request.POST.getlist('todoid')
            # filter the rows from table where todoid match
            # get the todo items to delete
            todo_items_to_delete = TodoItem.objects.filter(todoid__in=todolist_ids)
            # count the items to delete as we are keeping track of total todos
            items_count = todo_items_to_delete.count()
            # delete the todo items
            todo_items_to_delete.delete()
            # from the TodoListModel table filter owner and update the value of todocount
            # as the todo that are deleted will be removed from count as well
            TodoListModel.objects.filter(listid=listid, owner=owner).update(todocount=F('todocount') - items_count)
            # retrieve the updated instance
            updated_list = TodoListModel.objects.get(listid=listid, owner=owner)

            
        #---------------------------- done operation ------------------------+
        # it works behind done button in browser
        elif 'open' in request.POST:
            # when user selects rows and clicks done get all selected ids here
            todolist_ids = request.POST.getlist('todoid')
            # filter those from todo table and keep in donetodos
            # as we are keeping track of done tasks so we will update value of done to true
            # for all the ids that are marked as done
            donetodos = TodoItem.objects.filter(todoid__in=todolist_ids).update(done=True)
        
        #---------------------------- edit operation ------------------------+
        elif 'edit' in request.POST:
            # we have created a functionality in todoitem html template that when user check the 
            # specific row to edit it will get that value based on todoid and allow a user to edit 
            # edited value will be stored in hidden field that have name 'edited_value' and will pass with
            # POST request, here we will get id and new value from POST request and process
            edited_value = request.POST.get('edited_value')
            todo_id = request.POST.getlist('todoid')
            # check if new value does not have any valid character generate error message
            # if there is a valid value filter it from the table and check if already exists
            # generate error message
            if not(edited_value and any(c.isalpha() for c in edited_value)):
                messages.error(request,"Create operation failed. Please enter a valid"\
                                       " TodoList name")
                return HttpResponseRedirect(request.get_full_path())
            elif TodoItem.objects.filter(newtodo=edited_value, ownertodos_id=listid).exists():
                messages.error(request,"Edit operation failed. Please make sure that your"\
                                       " TodoList name does not exist in current TodoLists")
                return HttpResponseRedirect(request.get_full_path())
            # if the value is valid filter that vlaue from table based on its todoid
            # and update that id todoname with new todo name
            else:
                TodoItem.objects.filter(todoid=todo_id[0]).update(newtodo=edited_value)
            
            
            

    else:
        form = TodoItemForm()
    # --------------------- final block ----------------------------+
    # it will process either any condition is true or false
    # but it will contain information based on which operation processed above
    # filter the todoitem of logged in owner
    todo_item = TodoItem.objects.filter(ownertodos_id=listid, done=False)
    # count tasks that are not done
    notdone_count = models.TodoItem.objects.filter(ownertodos_id=listid, done=False).count()
    # count tasks that are done
    done_count = models.TodoItem.objects.filter(ownertodos_id=listid, done=True).count()
    # keep done tasks here
    done_items = models.TodoItem.objects.filter(ownertodos_id=listid, done=True)
    # make context pass all updated attribute values
    context = {'todo_item': todo_item, 'form': form, 'listname': listname, 'deadline':deadline, 'deadline':deadline, 'done_items':done_items, 'done_count':done_count, 'notdone_count':notdone_count}
    # after procssing the user request in view todoitem template will be passed to browser
    # and todoitem updated information will be passed
    # as you can see we displayed user todoitem information in table form in browser
    # it will updated based on what's updated in database
    # that functionaly processed here as we pass the updated information and display in browser
    return render(request, 'todoApp/todoitem.html', context)


