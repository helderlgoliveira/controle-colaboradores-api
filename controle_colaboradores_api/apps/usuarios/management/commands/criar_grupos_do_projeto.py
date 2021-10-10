from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings

from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Cria ou confirma a criação dos grupos de usuários necessários ao funcionamento do projeto."

    @transaction.atomic
    def handle(self, *args, **options):
        grupos = settings.USER_GROUPS_DO_PROJETO
        for grupo in grupos:
            obj, created = Group.objects.get_or_create(name=grupo)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Grupo '{grupo}' criado."))
            else:
                self.stdout.write(f"Grupo '{grupo}' não precisou ser criado pois já existe.")
        return "Fim da execução bem sucedida."
