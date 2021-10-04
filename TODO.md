# TO DO

1) Fazer testes DRF olhar site do DRF e se esse tá atualizado:
https://dev.to/sherlockcodes/pytest-with-django-rest-framework-from-zero-to-hero-8c4

APIRequestFactory (retorna REQUEST) para testes unitários de views e serializers

APIClient (retorna RESPONSE) para teste full-cycle de integração

## Apenas para salvar:

- [Definir qual Serializer chamar baseado nas actions](https://medium.com/aubergine-solutions/decide-serializer-class-dynamically-based-on-viewset-actions-in-django-rest-framework-drf-fb6bb1246af2)
- [criar usuario com senha via DRF pelo create_user, não create](https://stackoverflow.com/questions/29746584/django-rest-framework-create-user-with-password)
- [sobre passar context para serializer sem ser via nome de campo](https://www.django-rest-framework.org/api-guide/serializers/#including-extra-context)
- [10 itens importantes DRF](https://profil-software.com/blog/development/10-things-you-need-know-effectively-use-django-rest-framework/)
- [How to set current user to user field in Django Rest Framework?](https://stackoverflow.com/questions/35518273/how-to-set-current-user-to-user-field-in-django-rest-framework)
- fazer create e update no serializer onde há nested relacionamentos [Writable nested serializers](https://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers)
- custom to_representation para retornar os dados completos, mas aceitar apenas PK no post [site aqui](https://stackoverflow.com/a/46944720)

## Stages para deploy

- manage.py migrate (O MAKEMIGRATIONS SOMENTE NO DEV PARA COMMIT, na production deve usar as mesmas migrations)
- executar o cadastrar localidades_brasileiras
- executar o cadastrar grupos
- docker-compose com server, db e envs
