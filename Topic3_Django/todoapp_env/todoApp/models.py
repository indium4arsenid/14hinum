from django.db import models   # all new
from django.utils import timezone
from django.contrib.auth.models import User

'''In simple words all the models are tables of database
   and all the attributes declared in models are attributes of database tables
   to access any attribute value in view or html template we need to pass exactly same attribute name
   it is case sensitive
   - all attributes are objects of models'''

class Owner(User):
    """Inherited Model definition for Owners"""


#----------------------- TodoListModel ---------------+
# linked with todolist view
# .IntegerField, .CharField, .DateTimeField specifies the type of data that will be stored 
# in respective field
class TodoListModel(models.Model):
    # initialize listid filed/object
    # values will be updated in todolist view
    listid = models.IntegerField(primary_key=True, default=0)
    # initialize list name values will be updated from forms.py when user submit request
    listname = models.CharField(max_length=1000)
    # initialize deadline values will be updated from forms.py when user submit request
    deadline = models.DateField()
    # initialize todocount filed/object
    # values will be updated in todoitem view
    todocount = models.IntegerField(default=0)
    # automatically add the current date
    created_date = models.DateTimeField(auto_now_add=True)
    
    # a Many-to-One relationship with User Model
    owner = models.ForeignKey(Owner, blank=False, null=False, on_delete=models.CASCADE, related_name="Owner")
    
    class Meta:
        # each TodoList should be unique within its owner
        unique_together = (("listid", "owner"),)
    # pass all the attributes to view, when passing these attributes from view to browser template
    # name must be exactly same
    def __str__(self):
        return ' '.join(["List id:", str(self.listid), "Owner:", str(self.owner.username),  ", List name:", self.listname, ", Todo Count:", str(self.todocount), ", Created on:", str(self.created_date),
                         ", Deadline:", str(self.deadline)])


#----------------------- TodoItem ---------------+
# linked with todolitem view
# .AutoField, .BooleanField, .TextField specifies the type of data that will be stored 
# in respective field
class TodoItem(models.Model):
    # todoid will be updated automatically
    todoid = models.AutoField(primary_key=True)
    # get vlaue from form
    newtodo = models.TextField()
    # updated in todoid view
    done = models.BooleanField()

    # a Many-to-One relationship with TodoList Model
    ownertodos = models.ForeignKey(TodoListModel, blank=False, null=False,
                                      on_delete=models.CASCADE, related_name="todolist")

    class Meta:
        # user can not create 2 items with the same content in same TodoList
        unique_together = (("newtodo", "ownertodos"),)
    # pass all the attributes to view, when passing these attributes from view to browser template
    # name must be exactly same
    def __str__(self):
        return ' '.join(["Todo id:", str(self.todoid), "Todo Text:", self.newtodo, ", Done:", str(self.done),
                         ", Belongs to:", str(self.ownertodos.listname)])

