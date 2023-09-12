from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


class UserViewAdmin(UserAdmin):
    list_display = ("nickname", "email", "is_confirmed",)
    ordering = ("email", "nickname",)
    search_fields = ("email", "nickname",)

    fieldsets = (
        (None, {"fields": (
            "email", "nickname", "password", "is_confirmed", "is_staff", "is_superuser", "name",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "name",
                "nickname",
                "email",
                "password",
                "is_confirmed",
                "is_active",
                "is_superuser",
                "is_staff",
            )}
         ),
    )

    filter_horizontal = ()


admin.site.register(User, UserViewAdmin)
