from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Department)
admin.site.register(HOD)
admin.site.register(ERoll)
admin.site.register(Election)
admin.site.register(Student)
admin.site.register(Nomination)
