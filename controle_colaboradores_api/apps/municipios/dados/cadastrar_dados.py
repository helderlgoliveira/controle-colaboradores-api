import csv
from controle_colaboradores_api.apps.municipios.models import Municipio, RegiaoSaude, Microrregiao, Mesorregiao

# Cadastrar Regiões de Saúde
with open('controle_colaboradores_api/apps/municipios/dados/regioesdesaude.csv') as f:
    leitor = csv.reader(f)
    next(leitor) # pula cabeçalho
    for row in leitor:
        RegioesSaude.objects.get_or_create(numero=row[0])
        
# Cadastrar Microrregiões
with open('controle_colaboradores_api/apps/municipios/dados/microrregioes.csv') as f:
    leitor = csv.reader(f)
    next(leitor) # pula cabeçalho
    for row in leitor:
        Microrregioes.objects.get_or_create(nome=row[0])
        
# Cadastrar Mesorregiões
with open('controle_colaboradores_api/apps/municipios/dados/mesorregioes.csv') as f:
    leitor = csv.reader(f)
    next(leitor) # pula cabeçalho
    for row in leitor:
        Mesorregiao.objects.get_or_create(nome=row[0])
        
# Cadastrar Municípios
with open('controle_colaboradores_api/apps/municipios/dados/municipios.csv') as f:
    leitor = csv.reader(f)
    next(leitor) # pula cabeçalho
    for row in leitor:
        Municipios.objects.get_or_create(
            nome=row[0],
            regiao_saude_id=row[1],
            microrregiao_id=row[2],
            mesorregiao_id=row[3],
            cod_ibge=row[4]
            )
        