from django.db import models


class Base(models.Model):
    criacao = models.DateTimeField('Criação', auto_now_add=True)
    modificacao = models.DateTimeField('Modificação', auto_now=True)

    class Meta:
        abstract = True


class UnidadeFederativa(Base):
    nome = models.CharField('Nome', max_length=200, unique=True)
    sigla = models.CharField('Sigla', max_length=10, unique=True)
    cod_ibge = models.CharField('Código do IBGE', max_length=50, unique=True)
    latitude = models.CharField('Latitude', max_length=50)
    longitude = models.CharField('Longitude', max_length=50)
    capital = models.OneToOneField('Municipio', related_name="capital_de", on_delete=models.RESTRICT, null=True)

    class Meta:
        verbose_name = 'Unidade Federativa'
        verbose_name_plural = 'Unidades Federativas'

    def __str__(self):
        return str(self.nome)


class Municipio(Base):
    nome = models.CharField('Nome do Município', max_length=200)
    cod_ibge = models.CharField('Código do IBGE', max_length=50, unique=True)
    uf = models.ForeignKey('UnidadeFederativa', related_name="municipios", on_delete=models.CASCADE)
    latitude = models.CharField('Latitude', max_length=50)
    longitude = models.CharField('Longitude', max_length=50)
    ddd = models.PositiveSmallIntegerField('DDD')
    fuso_horario = models.CharField('Fuso horário', max_length=50)
    cod_siafi = models.CharField('Código do SIAFI', max_length=20)

    class Meta:
        verbose_name = 'Município'
        verbose_name_plural = 'Municípios'

    def __str__(self):
        return self.nome
