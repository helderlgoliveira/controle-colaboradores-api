# TO DO

- Fazer o formato para cadastrar o perfil completo:-
-- com todos os nested, lembrando que o municipio_onde_trabalha recebe PK do perfil e do municipio para cadastrar, dessa forma primeiro acho salva sem eles acho e depois update partial o PK do perfil (depois de gerado ne, assim: [Writable nested serializers](https://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers))

## Apenas para salvar:
- fazer create e update no serializer onde há nested relacionamentos [Writable nested serializers](https://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers)
- custom to_representation para retornar os dados completos, mas aceitar apenas PK no post [site aqui](https://stackoverflow.com/a/46944720)

## Stages para deploy

- executar o cadsatrar localidades_brasileiras
- executar o cadastrar grupos
- docker-compose com server, db e envs
