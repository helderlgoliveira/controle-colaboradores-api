# API para Controle de Colaboradores

Modelo de API REST para controle de colaboradores de uma empresa/instituição, com dados essenciais relativos aos perfis dos colaboradores, inclusive com gerenciamento de cargos e departamentos.

[Acesse aqui a documentação on-line da API](https://api-controle-colaboradores.herokuapp.com/api/v1/swagger).
Para utilizá-la on-line, realize _login_ com os seguintes usuários:

> Usuário do grupo de **Administradores**:
> _Email/Username_: administrador@email.com
> _Senha_: administrador
> 
> Usuário do grupo de **Colaboradores**:
> _Email/Username_: colaborador@email.com
> _Senha_: colaborador


## Instalação e requisitos

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

Defina as seguintes variáveis de ambiente:
```
SECRET_KEY=''
DATABASE_HOST=''
DATABASE_NAME=''
DATABASE_USER=''
DATABASE_PASSWORD=''
DATABASE_PORT=
DJANGO_SETTINGS_MODULE=''
EMAIL_HOST=''
EMAIL_HOST_USER=''
EMAIL_PORT=587
EMAIL_HOST_PASSWORD=''
DEFAULT_FROM_EMAIL=''
ADMINS='Nome1/email1@email.com Nome2/email2@email.com'
PRODUCTION_ALLOWED_HOSTS='dominio1.com dominio2.com'
DJANGO_SUPERUSER_EMAIL=''
DJANGO_SUPERUSER_USERNAME=''
DJANGO_SUPERUSER_PASSWORD=''
```

## Execução

No ambiente virtual (`poetry shell` ou virtualenv ativado):
```
./manage.py migrate
./manage.py criar_grupos_do_projeto
./manage.py cadastrar_localidades_brasileiras
./manage.py createsuperuser --noinput
./manage.py collectstatic
gunicorn controle_colaboradores_api.wsgi
```

Utilize o _superuser_ definido nas variáveis de ambiente para cadastrar o primeiro usuário e vinculá-lo ao grupo de Administradores, pode ser feito tanto via _shell_ quanto por meio do _endpoint_ de cadastro de usuários.

Após, é indicado mudar a senha do _superuser_.

A partir do cadastro do primeiro usuário do grupo de Administradores, não é mais necessário utilizar o _superuser_.

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
