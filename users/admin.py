from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'email',
        'username',
        'status',
        'is_verified',
        'is_staff',
        'is_superuser',
        'is_email_active',
    ]
    fields = [
        "email",
        "username",
        "status",
        "is_verified",
        "is_staff",
        "is_superuser",
        "is_email_active",
        "bio",
        "avatar",
        "rating",
        "phone_number",
        "wallet"
    ]
    readonly_fields = ["wallet"]
