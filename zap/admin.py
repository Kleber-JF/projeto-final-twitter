from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Meep

# Unregister groups.

admin.site.unregister(Group)

#Extend User Model

#Mix Profile info into User info
class ProfileInline(admin.StackedInline):
    model = Profile
class UserAdmin(admin.ModelAdmin):
    model = User
    #Just display username fields on admin page
    fields = ['username']
    inlines = [ProfileInline]

#Unregister initial User
admin.site.unregister(User)

#Reregister User and Profile
admin.site.register(User, UserAdmin)
#admin.site.register(Profile)
#Register Meep model
admin.site.register(Meep)