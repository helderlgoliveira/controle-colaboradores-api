# API para Controle de Colaboradores

REST API para controle de colaboradores de uma empresa/instituição.

Documentação feita com [Swagger](https://swagger.io/):
[Acesse aqui a documentação on-line da API]().


## Instalação dos requisitos

Baixe ou clone o repositório:
```
git clone https://github.com/helderlgoliveira/controle-colaboradores-api.git
cd controle-colaboradores-api
```
Instale os pacotes preferencialmente utilizando [poetry](https://python-poetry.org/):
```
poetry install --no-dev
```
Caso prefira via pip (indica-se sempre executar dentro de [virtualenv](https://virtualenv.pypa.io/en/latest/)):
```
pip install -r requirements.txt
```

## Execução

No ambiente virtual (`poetry shell` ou virtualenv ativado):
```
./manage.py migrate
./manage.py criar_grupos_do_projeto
./manage.py cadastrar_localidades_brasileiras
./manage.py runserver
```

## Desenvolvimento

Instale os todos os pacotes. 
Via [poetry](https://python-poetry.org/):
```
poetry install
```
Via pip:
```
pip install -r requirements-inclusive-dev.txt
```

## Testes
No ambiente virtual, execute os testes com [pytest](https://docs.pytest.org/en/latest/):
```
pytest
```
