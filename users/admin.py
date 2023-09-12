from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


class UserViewAdmin(UserAdmin):
    list_display = ("nickname", "email", "is_active",)
    ordering = ("email", "nickname",)
    search_fields = ("email", "nickname",)

    fieldsets = (
        (None, {"fields": (
            "email", "name", "nickname", "password", "is_active", "is_superuser", "is_staff")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "name",
                "nickname",
                "email",
                "password",
                "is_active",
                "is_staff"
                "is_superuser",
            )}
         ),
    )

    filter_horizontal = ()


admin.site.register(User, UserViewAdmin)
