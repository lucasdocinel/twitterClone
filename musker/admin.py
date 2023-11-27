from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Meep


# Unregister initial Profile
admin.site.unregister(Group)

# Mix Profile indo into User
class ProfileInline(admin.StackedInline):
    model = Profile

# Extend User model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username']
    inlines = [ProfileInline]


# Unregister initial User
admin.site.unregister(User)

# Reregister User and Profile
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)

# Register Meeps
admin.site.register(Meep)


