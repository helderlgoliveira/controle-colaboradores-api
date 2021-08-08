from django.core.management.base import BaseCommand
from django.db import transaction

from django.contrib.auth.models import Group, Permission

from configuracoes.leitor_configuracoes import LeitorConfiguracoes as lConf


class Command(BaseCommand):
    help = "Cria ou confirma a criação dos grupos de usuários essenciais ao funcionamento do projto."

    @transaction.atomic
    def handle(self, *args, **options):
        grupos = lConf.obter_configuracao_especifica("implantacao_no_deploy")["grupos_de_usuarios"]
        for g in grupos:
            obj, created = Group.objects.get_or_create(name=g['name'])

            permissions = Permission.objects.filter(codename__in=g['permissions'])
            obj.permissions.set(permissions)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Grupo '{g['name']}' criado. Permissões atribuídas."))
            else:
                self.stdout.write(f"Grupo '{g['name']}' não precisou ser criado pois já existe. Permissões foram"
                                  f" substituídas pelas informadas.")
