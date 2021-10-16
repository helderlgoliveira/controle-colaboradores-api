# Generated by Django 3.2.7 on 2021-10-16 22:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('perfis', '0001_initial'),
        ('localidades_brasileiras', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='perfil',
            name='usuario_modificacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuário da modificação'),
        ),
        migrations.AddField(
            model_name='outroemail',
            name='perfil',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outros_emails', to='perfis.perfil'),
        ),
        migrations.AddField(
            model_name='endereco',
            name='municipio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='enderecos', to='localidades_brasileiras.municipio'),
        ),
        migrations.AddField(
            model_name='endereco',
            name='perfil',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enderecos', to='perfis.perfil'),
        ),
        migrations.AddField(
            model_name='departamento',
            name='departamento_superior',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='departamentos_subordinados', to='perfis.departamento'),
        ),
        migrations.AddField(
            model_name='departamento',
            name='diretor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='diretor_em', to='perfis.perfil', verbose_name='Diretor do departamento'),
        ),
        migrations.AddField(
            model_name='departamento',
            name='diretor_substituto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='diretor_substituto_em', to='perfis.perfil', verbose_name='Diretor substituto do departamento'),
        ),
        migrations.AddField(
            model_name='departamento',
            name='usuario_modificacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuário da modificação'),
        ),
        migrations.AddField(
            model_name='cargo',
            name='usuario_modificacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuário da modificação'),
        ),
        migrations.AddConstraint(
            model_name='endereco',
            constraint=models.UniqueConstraint(condition=models.Q(('is_principal', True)), fields=('perfil', 'is_principal'), name='unique_endereco_principal_por_perfil'),
        ),
        migrations.AddConstraint(
            model_name='cargo',
            constraint=models.CheckConstraint(check=models.Q(('salario__gt', 0)), name='salario_gt_zero'),
        ),
        migrations.AlterUniqueTogether(
            name='cargo',
            unique_together={('nome', 'classe')},
        ),
    ]
