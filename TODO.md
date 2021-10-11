# TO DO

1) Passar vista nos testes somente para ver se algo deixado sem querer (acho que não).
2) DEPLOY NO HEROKU, INCLUIR LINK NO README.

## Stages para deploy / Instruções pro README:

- manage.py migrate (O MAKEMIGRATIONS SOMENTE NO DEV PARA COMMIT, na production deve usar as mesmas migrations)
- executar o cadastrar localidades_brasileiras
- executar o cadastrar grupos
- criar o usuário admin
- docker-compose com server, db e envs
DJANGO REVERSION + AUDIT LOG??? (dessa vez melhor não, não é preciso)


1) Fazer testes DRF olhar site do DRF e se esse tá atualizado:
https://dev.to/sherlockcodes/pytest-with-django-rest-framework-from-zero-to-hero-8c4

APIRequestFactory (retorna REQUEST) para testes unitários de views e serializers

APIClient (retorna RESPONSE) para teste full-cycle de integração

---------------
Serializers: uns dizem só para testar 
(1) as funções próprias que criou dentro do serializers, e de repente se quiser um 
(2) formato especifico fazer teste para impedir que alterem o formato de saída. (ESSA PARTE TENHO FEITO NO EXPECTED_JSON DO TESTE DAS VIEWS) 

Here is what we do at edX: https://github.com/edx/course-discovery/blob/7b7ca8924f0fb83dfe1363a6a0b112494e0bac59/course_discovery/apps/api/tests/test_serializers.py#L98-L120.

Our philosophy is to test the serializers, and use the (now tested/trusted) serializers to validate the data of our views. See https://github.com/edx/course-discovery/blob/7b7ca8924f0fb83dfe1363a6a0b112494e0bac59/course_discovery/apps/api/v1/tests/test_views/test_course_runs.py#L38-L46 for an example of a view test.

## Apenas para salvar:

- [Definir qual Serializer chamar baseado nas actions](https://medium.com/aubergine-solutions/decide-serializer-class-dynamically-based-on-viewset-actions-in-django-rest-framework-drf-fb6bb1246af2)
- [criar usuario com senha via DRF pelo create_user, não create](https://stackoverflow.com/questions/29746584/django-rest-framework-create-user-with-password)
- [sobre passar context para serializer sem ser via nome de campo](https://www.django-rest-framework.org/api-guide/serializers/#including-extra-context)
- [10 itens importantes DRF](https://profil-software.com/blog/development/10-things-you-need-know-effectively-use-django-rest-framework/)
- [How to set current user to user field in Django Rest Framework?](https://stackoverflow.com/questions/35518273/how-to-set-current-user-to-user-field-in-django-rest-framework)
- fazer create e update no serializer onde há nested relacionamentos [Writable nested serializers](https://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers)
- custom to_representation para retornar os dados completos, mas aceitar apenas PK no post [site aqui](https://stackoverflow.com/a/46944720)


