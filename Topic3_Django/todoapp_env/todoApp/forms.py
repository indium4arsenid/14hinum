from django import forms
from .models import TodoListModel, TodoItem

#-------------------- Form objects ---------------+
# Linked with TodoListModel and todolist view
class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoListModel
        # all the attriutes of form that will be created in template
        fields = ['listname', 'deadline']
# Linked with TodoItem model and todoitem view
class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        # all the attriutes of form that will be created in template
        fields = ['newtodo']

