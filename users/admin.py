from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewAdmin(UserAdmin):
    list_display = ("first_name", "last_name", "email", "is_active",)
    ordering = ("email",)
    search_fields = ("email",)

    fieldsets = (
        (None, {"fields": (
            "email", "first_name", "last_name", "password", "is_active", "is_superuser", "is_staff")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "first_name",
                "last_name",
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
