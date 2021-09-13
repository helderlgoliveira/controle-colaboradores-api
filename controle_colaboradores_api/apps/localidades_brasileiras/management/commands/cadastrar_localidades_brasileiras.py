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
        self._relacionar_capitais_com_ufs()
        self.stdout.write(self.style.SUCCESS(f"-- Localidades brasileiras registradas/atualizadas com sucesso."))

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
            with open('controle_colaboradores_api/apps/localidades_brasileiras/dados/municipios.csv') as f:
                leitor = csv.reader(f)
                next(leitor)  # ignora o cabeçalho
                for row in leitor:
                    uf = UnidadeFederativa.objects.get(cod_ibge=row[4])
                    obj, created = Municipio.objects.get_or_create(
                        cod_ibge=row[0],
                        nome=row[1],
                        latitude=row[2],
                        longitude=row[3],
                        uf=uf,
                        cod_siafi=row[5],
                        ddd=row[6],
                        fuso_horario=row[7]
                        )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Município {row[1]} cadastrado."))
                    else:
                        self.stdout.write(f"Município {row[1]} não precisou ser cadastrado pois já existe.")
        except Exception as e:
            print(f"Ocorreu um erro no cadastro de Municípios: {repr(e)}")
            raise

    @transaction.atomic
    def _relacionar_capitais_com_ufs(self):
        try:
            with open('controle_colaboradores_api/apps/localidades_brasileiras/dados/unidades_federativas.csv') as f:
                leitor = csv.reader(f)
                next(leitor)  # ignora o cabeçalho
                for row in leitor:
                    codigo_ibge_uf = row[0]
                    codigo_ibge_capital = row[5]

                    uf = UnidadeFederativa.objects.get(cod_ibge=codigo_ibge_uf)
                    capital = Municipio.objects.get(cod_ibge=codigo_ibge_capital)
                    if uf.capital != capital:
                        uf.capital = capital
                        uf.save(update_fields=['capital'])
                        self.stdout.write(self.style.SUCCESS(f"Capital da UF {uf.nome} foi atualizada para:"
                                                             f" {capital.nome}."))
                    else:
                        self.stdout.write(f"Capital da UF {uf.nome} não precisou ser modificada pois"
                                          f" já estava atualizada.")
        except Exception as e:
            print(f"Ocorreu um erro no cadastro das capitais de Unidades Federativas: {repr(e)}")
            raise



