from django.db import models


class Base(models.Model):
    criacao = models.DateTimeField('Criação', auto_now_add=True)
    modificacao = models.DateTimeField('Modificação', auto_now=True)

    class Meta:
        abstract = True


class Macrorregiao(Base):
    # Decidi não vincular a Macrorregião à Unidade Federativa em razão de que, ainda em 2021, o IBGE
    # não faz vínculo nem estipula código entre a Macrorregião e a UF nas tabelas públicas que ele disponibiliza.
    nome = models.CharField('Nome da Macrorregião', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Macrorregião'
        verbose_name_plural = 'Macrorregiões'

    def __str__(self):
        return self.nome
    
    
class Mesorregiao(Base):
    nome = models.CharField('Nome da Mesorregião', max_length=200, unique=True)
    macrorregiao = models.ForeignKey('Macrorregiao', related_name="mesorregioes", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Mesorregião'
        verbose_name_plural = 'Mesorregiões'

    def __str__(self):
        return self.nome


class Microrregiao(Base):
    nome = models.CharField('Nome da Microrregião', max_length=200, unique=True)
    mesorregiao = models.ForeignKey('Mesorregiao', related_name="microrregioes", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Microrregião'
        verbose_name_plural = 'Microrregiões'

    def __str__(self):
        return self.nome


class RegiaoSaude(Base):
    numero = models.PositiveIntegerField('Número da Região de Saúde', unique=True)

    class Meta:
        verbose_name = 'Região de Saúde'
        verbose_name_plural = 'Regiões de Saúde'

    def __str__(self):
        return str(self.numero)


class UnidadeFederativa(Base):
    nome = models.CharField('Nome da Unidade Federativa', max_length=200, unique=True)
    sigla = models.CharField('Sigla da Unidade Federativa', max_length=10, unique=True)
    cod_ibge = models.CharField('Código do IBGE', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Unidade Federativa'
        verbose_name_plural = 'Unidades Federativas'

    def __str__(self):
        return str(self.nome)


class Municipio(Base):
    nome = models.CharField('Nome do Município', max_length=200, unique=True)
    cod_ibge = models.CharField('Código do IBGE', max_length=200, unique=True)
    uf = models.ForeignKey('UnidadeFederativa', related_name="municipios", on_delete=models.CASCADE)
    regiao_saude = models.ForeignKey('RegiaoSaude', related_name="municipios", on_delete=models.CASCADE)
    microrregiao = models.ForeignKey('Microrregiao', related_name="municipios", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Município'
        verbose_name_plural = 'Municípios'

    def __str__(self):
        return self.nome
