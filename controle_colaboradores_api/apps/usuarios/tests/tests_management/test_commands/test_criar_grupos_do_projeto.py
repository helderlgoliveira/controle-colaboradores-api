from django.conf import settings
from django.contrib.auth.models import Group

from controle_colaboradores_api.apps.usuarios.management.commands.criar_grupos_do_projeto import Command

class TestCommand:

    def test_handle(self, db):
        assert Command().handle() == "Fim da execução bem sucedida."
        for grupo in settings.USER_GROUPS_DO_PROJETO:
            assert Group.objects.filter(name=grupo).exists()

