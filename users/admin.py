from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    # Form per l'aggiunta e la modifica degli utenti
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # Campi da visualizzare nella lista utenti
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active'
    ]

    # Filtri disponibili nella sidebar
    list_filter = [
        'is_staff',
        'is_active'
    ]

    # Configurazione dei fieldset per la modifica utente
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'address')}),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Configurazione dei fieldset per la creazione utente
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'first_name',
                'last_name',
                'address',
                'password1',
                'password2',
                'is_staff',
                'is_active'
            )}
         ),
    )

    # Campi per cui è disponibile la ricerca
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # Ordinamento predefinito
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)