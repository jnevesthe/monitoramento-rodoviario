from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import Registrar, EditForm
from django.utils.html import format_html

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = Registrar       # form usado para criar usuários
    form = EditForm            # form usado para editar usuários
    model = User

    list_display = ('username', 'email', 'is_staff', 'autorizado', 'foto_admin')
    search_fields = ('username', 'email')

    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('autorizado', 'foto')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra', {'fields': ('autorizado', 'foto')}),
    )

    def foto_admin(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="width:40px;height:40px;border-radius:50%;" />', obj.foto.url)
        return "-"
    foto_admin.short_description = 'Foto'
