from django.contrib import admin

from .models import Municipio, UnidadeFederativa, RegiaoSaude, Microrregiao, Mesorregiao


@admin.register(Municipio)
class MunicipiosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'uf', 'regiao_saude', 'microrregiao', 'get_mesorregiao', 'cod_ibge')

    def get_mesorregiao(self, obj):
        return obj.microrregiao.mesorregiao

    get_mesorregiao.short_description = 'Mesorregião'
    get_mesorregiao.admin_order_field = 'mesorregiao__microrregiao'


@admin.register(UnidadeFederativa)
class UnidadeFederativaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sigla')


@admin.register(RegiaoSaude)
class RegioesSaudeAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero')


@admin.register(Microrregiao)
class MicrorregioesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')


@admin.register(Mesorregiao)
class MesorregioesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
