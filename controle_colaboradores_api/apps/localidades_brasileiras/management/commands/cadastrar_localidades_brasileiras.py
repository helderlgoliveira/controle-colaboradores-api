import csv

from django.core.management.base import BaseCommand
from django.db import transaction

from controle_colaboradores_api.apps.localidades_brasileiras.models import UnidadeFederativa, Municipio


class Command(BaseCommand):
    help = "Cadastra ou confirma a existência das localidades brasileiras no banco de dados."

    @transaction.atomic
    def handle(self, *args, **options):
        self._cadastrar_unidades_federativas()
        self._cadastrar_municipios()

    @transaction.atomic
    def _cadastrar_unidades_federativas(self):
        try:
            with open('controle_colaboradores_api/apps/localidades_brasileiras/dados/unidades_federativas.csv') as f:
                leitor = csv.reader(f)
                next(leitor)  # ignora o cabeçalho
                for row in leitor:
                    obj, created = UnidadeFederativa.objects.get_or_create(
                        cod_ibge=row[0],
                        sigla=row[1],
                        nome=row[2],
                        latitude=row[3],
                        longitude=row[4]
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"UF {row[2]} cadastrada."))
                    else:
                        self.stdout.write(f"UF {row[2]} não precisou ser cadastrada pois já existe.")
        except Exception as e:
            print(f"Ocorreu um erro no cadastro de Unidades Federativas: {repr(e)}")
            raise

    @transaction.atomic
    def _cadastrar_municipios(self):
        try:
            with open('controle_colaboradores_api/apps/localidades_brasileiras/dados/municipíos.csv') as f:
                leitor = csv.reader(f)
                next(leitor)  # ignora o cabeçalho
                for row in leitor:
                    obj, created = Municipio.objects.get_or_create(
                        cod_ibge=row[0],
                        nome=row[1],
                        latitude=row[2],
                        longitude=row[3],
                        uf=row[4],
                        cod_siafi=row[5],
                        ddd=row[6],
                        fuso_horario=row[7]
                        )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Município {row[2]} cadastrado."))
                    else:
                        self.stdout.write(f"Município {row[2]} não precisou ser cadastrado pois já existe.")
        except Exception as e:
            print(f"Ocorreu um erro no cadastro de Municípios: {repr(e)}")
            raise
