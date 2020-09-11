from django.contrib import admin

from .models import TaskList
# same as from todolist_app.models import TaskList

# Register your models here.
admin.site.register(TaskList)