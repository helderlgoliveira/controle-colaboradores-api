from django.db import models, transaction
from django.contrib.auth import get_user_model

from controle_colaboradores_api.apps.localidades.models import Municipio
from configuracoes.leitor_configuracoes import LeitorConfiguracoes


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
                                            on_delete=models.PROTECT)

    class Meta:
        abstract = True


class Perfil(BaseParaModelsImportantes):
    usuario = models.OneToOneField(get_user_model(), related_name="perfil", on_delete=models.CASCADE)
    nome = models.CharField('Nome', max_length=200)
    sobrenome = models.CharField('Sobrenome', max_length=200)
    # telefones (related_name da class Telefone)
    # outros_emails (related_name da class OutroEmail)

    municipios_onde_trabalha = \
        models.ManyToManyField(Municipio,
                               help_text=LeitorConfiguracoes.obter_help_text_especifico(
                                   "perfil_municipios_onde_trabalha"),
                               through='MunicipioOndeTrabalha')

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


class Telefone(Base):
    perfil = models.ForeignKey(Perfil, related_name="telefones", on_delete=models.CASCADE)

    # Formato: (DD) 99999-9999 ou (DD) 3333-3333
    numero = models.CharField('Telefone',
                              max_length=20,
                              help_text=LeitorConfiguracoes.obter_help_text_especifico(
                                  "perfil_telefone_numero")
                              )

    class Meta:
        verbose_name = 'Telefone'
        verbose_name_plural = 'Telefones'

    def __str__(self):
        return self.numero


class OutroEmail(Base):
    perfil = models.ForeignKey(Perfil, related_name="outros_emails", on_delete=models.CASCADE)

    email = models.EmailField('E-mail',
                              help_text=LeitorConfiguracoes.obter_help_text_especifico(
                                  "perfil_outro_email")
                              )

    class Meta:
        verbose_name = 'Outro e-mail'
        verbose_name_plural = 'Outros e-mails'

    def __str__(self):
        return self.email


class MunicipioOndeTrabalha(Base):
    # ManyToOne porque um município pode ser atribuído a mais de um usuário (substitutos, designados etc).
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)

    municipio = models.ForeignKey(Municipio,
                                  related_name="perfis",
                                  verbose_name='Município onde trabalha',
                                  on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Município onde trabalha'
        verbose_name_plural = 'Municípios onde trabalha'

    def __str__(self):
        return f'{self.perfil.usuario.email} - {self.municipio.nome}'
