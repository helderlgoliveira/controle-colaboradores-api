import os
import binascii
import random
from django.utils import timezone
from datetime import timedelta

from django.db import models, transaction
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model


class CustomUsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório.')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')

        return self._create_user(email, password, **extra_fields)


class CustomUsuario(AbstractUser):
    email = models.EmailField('E-mail', unique=True)
    is_staff = models.BooleanField('Membro da equipe', default=False)

    USERNAME_FIELD = 'email'

    # Nome e sobrenome serão definidos ao criar o perfil, dessa forma não serão obrigatórios aqui.
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    objects = CustomUsuarioManager()


class PasswordResetToken(models.Model):
    usuario = models.ForeignKey(get_user_model(), related_name="password_reset_tokens", on_delete=models.CASCADE)
    token = models.CharField('Token', unique=True, max_length=64, db_index=True)
    criacao = models.DateTimeField('Criação', auto_now_add=True)
    ativo = models.BooleanField('Ativo', default=True)

    @property
    def expirado(self):
        prazo_em_dias = 1
        expiracao = self.criacao + timedelta(days=prazo_em_dias)
        if timezone.now() > expiracao:
            return True
        return False

    def gerar_token(self):
        length = random.randint(40, 60)
        return binascii.hexlify(os.urandom(length)).decode()[0:length]

    def enviar_token_por_email(self):
        return send_mail(
            f'Criar nova senha - {settings.NOME_DO_PROJETO}',
            f'Olá!\n'
            f'Conforme o solicitado, segue o link para criar a sua nova senha: \n'
            f'{settings.URL_BASE_CRIAR_NOVA_PASSWORD_APOS_RESETAR_PASSWORD}{self.token}',
            None,
            [self.usuario.email],
            fail_silently=False,
        )

    def save(self, *args, **kwargs):
        if self._state.adding:
            with transaction.atomic():
                self.token = self.gerar_token()
                super().save(*args, **kwargs)
                self.enviar_token_por_email()
        else:
            super().save(*args, **kwargs)
