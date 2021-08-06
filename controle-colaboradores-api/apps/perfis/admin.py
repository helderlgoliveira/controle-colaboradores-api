from django.contrib import admin

from .models import Perfil, Telefone, OutroEmail


class TelefoneInline(admin.TabularInline):
    model = Telefone


class OutrosEmailsInline(admin.TabularInline):
    model = OutroEmail


class MunicipiosInline(admin.TabularInline):
    model = Perfil.municipios_onde_trabalha.through


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario',
                    'nome',
                    'sobrenome',
                    'get_outros_emails',
                    'get_municipios_onde_trabalha',
                    'modificacao',
                    'usuario_modificacao'
                    )
    inlines = [
        TelefoneInline,
        OutrosEmailsInline,
        MunicipiosInline
    ]
    exclude = ['usuario_modificacao']

    def get_outros_emails(self, obj):
        return ', '.join([n.email for n in obj.outros_emails.all()])

    get_outros_emails.short_description = 'Outros e-mails'

    def get_municipios_onde_trabalha(self, obj):
        return ', '.join([n.nome for n in obj.municipios_onde_trabalha.all()])

    get_municipios_onde_trabalha.short_description = 'Municípios'

    def save_model(self, request, obj, form, change):
        obj.usuario_modificacao_id = request.user.id
        super().save_model(request, obj, form, change)
