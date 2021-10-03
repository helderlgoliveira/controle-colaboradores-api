from django.db import models, transaction
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


class Base(models.Model):
    criacao = models.DateTimeField('Criação', auto_now_add=True)
    modificacao = models.DateTimeField('Modificação', auto_now=True)

    class Meta:
        abstract = True


class BaseParaModelsImportantes(Base):
    ativo = models.BooleanField('Ativo', default=True)
    usuario_modificacao = models.ForeignKey(get_user_model(),
                                            verbose_name="Usuário da modificação",
                                            related_name="+",
                                            on_delete=models.RESTRICT)

    class Meta:
        abstract = True


class Perfil(BaseParaModelsImportantes):
    usuario = models.OneToOneField(get_user_model(), related_name="perfil", on_delete=models.CASCADE)
    nome = models.CharField('Nome', max_length=200)
    sobrenome = models.CharField('Sobrenome', max_length=200)
    cpf = models.CharField('CPF', max_length=40, unique=True, blank=True)
    contrato_identificador = models.CharField('Identificador do Contrato', max_length=200)
    data_admissao = models.DateField('Data de admissão')
    data_demissao = models.DateField('Data de demissão', null=True)
    dados_bancarios_banco = models.CharField('Dados bancários - Banco', max_length=200, blank=True)
    dados_bancarios_agencia = models.CharField('Dados bancários - Agência', max_length=200, blank=True)
    dados_bancarios_conta = models.CharField('Dados bancários - Conta', max_length=200, blank=True)

    # Cargos, Departamentos e Municípios múltiplos pela possibilidade de acumulação
    cargos = models.ManyToManyField('Cargo', related_name='perfis', blank=True)
    departamentos = models.ManyToManyField('Departamento', related_name='perfis', blank=True)
    municipios_onde_trabalha = models.ManyToManyField('localidades_brasileiras.Municipio',
                                                      related_name='perfis',
                                                      blank=True)

    # Mais atributos já existentes via related_name:
    # - telefones (class Telefone)
    # - outros_emails (class OutroEmail)
    # - enderecos (class Endereco)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return f'{self.usuario.email} - {self.nome} {self.sobrenome}'

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.usuario.first_name = self.nome
            self.usuario.last_name = self.sobrenome
            self.usuario.save()
            super().save(*args, **kwargs)


class Endereco(Base):
    perfil = models.ForeignKey(Perfil, related_name="enderecos", on_delete=models.CASCADE)
    is_principal = models.BooleanField("É o endereço principal", default=False)
    logradouro = models.CharField('Logradouro', max_length=200)
    numero = models.CharField('Número', max_length=10)
    bairro = models.CharField('Bairro', max_length=50)
    complemento = models.CharField('Complemento', max_length=50, blank=True)
    municipio = models.ForeignKey('localidades_brasileiras.Municipio', related_name="enderecos", on_delete=models.RESTRICT)
    cep = models.CharField('CEP', max_length=20)

    @property
    def endereco_completo(self):
        return f"{self.logradouro}, {self.numero}, {self.bairro}," \
               f" {self.complemento}, {self.municipio.nome}-{self.municipio.uf.sigla}, {self.cep}."

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
        ordering = ['perfil']
        constraints = [
            models.UniqueConstraint(fields=['perfil', 'is_principal'],
                                    condition=Q(is_principal=True),
                                    name='unique_endereco_principal_por_perfil')
        ]

    def __str__(self):
        return f'{self.perfil.usuario.email} - {self.endereco_completo}'


class Telefone(Base):
    perfil = models.ForeignKey(Perfil, related_name="telefones", on_delete=models.CASCADE)

    # Formato: (DD) 99999-9999 ou (DD) 3333-3333
    numero = models.CharField('Telefone',
                              max_length=25)

    class Meta:
        verbose_name = 'Telefone'
        verbose_name_plural = 'Telefones'

    def __str__(self):
        return self.numero


class OutroEmail(Base):
    perfil = models.ForeignKey(Perfil, related_name="outros_emails", on_delete=models.CASCADE)

    email = models.EmailField('E-mail')

    class Meta:
        verbose_name = 'Outro e-mail'
        verbose_name_plural = 'Outros e-mails'

    def __str__(self):
        return self.email


class Cargo(BaseParaModelsImportantes):
    nome = models.CharField('Nome', max_length=50)
    classe = models.CharField('Classe', max_length=50)
    salario = models.DecimalField('Salário', decimal_places=2, max_digits=20, validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        unique_together = ['nome', 'classe']
        constraints = [
            models.CheckConstraint(check=Q(salario__gt=0), name='salario_gt_zero')
        ]

    def __str__(self):
        return f'{self.nome} - {self.classe}'


class Departamento(BaseParaModelsImportantes):
    nome = models.CharField('Nome', unique=True, max_length=100)
    diretor = models.ForeignKey(Perfil,
                                verbose_name="Diretor do departamento",
                                on_delete=models.RESTRICT,
                                related_name="diretor_em")
    diretor_substituto = models.ForeignKey(Perfil,
                                           verbose_name="Diretor substituto do departamento",
                                           on_delete=models.RESTRICT,
                                           null=True,
                                           related_name="diretor_substituto_em")
    departamento_superior = models.ForeignKey('Departamento',
                                              null=True,
                                              related_name="departamentos_subordinados",
                                              on_delete=models.RESTRICT)

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return f'{self.nome}'
