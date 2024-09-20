# Generated by Django 4.2.9 on 2024-09-20 01:18

import django.contrib.auth.validators
from django.db import migrations, models
import helpers.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150, verbose_name='Nome completo')),
                ('email', models.EmailField(help_text='Seu melhor e-mail. Será usado para login também.', max_length=254, unique=True, verbose_name='E-mail')),
                ('username', models.CharField(error_messages={'unique': 'Já existe um usuário com este username.'}, help_text='Obrigatório. 150 caracteres ou menos. Letras, números e os símbolos @/./+/-/_ são permitidos.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='Usuário')),
                ('token', models.JSONField(blank=True, null=True, verbose_name='Token da Mensagem')),
                ('is_staff', models.BooleanField(default=False, help_text='Pode logar no Admin', verbose_name='Staff')),
                ('is_superuser', models.BooleanField(default=False, help_text='Usuário com acesso irrestrito no sistema.', verbose_name='Usuário administrador')),
                ('is_active', models.BooleanField(default=True, help_text='Desmarque esta opção em vez de deletar o usuário.', verbose_name='Ativo')),
                ('is_client', models.BooleanField(help_text='Cliente da empresa que tem acesso apenas a algumas funcionalidades', verbose_name='Cliente')),
                ('is_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')),
                ('last_login', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
                'db_table': 'User',
                'ordering': ['created_at'],
            },
            managers=[
                ('objects', helpers.manager.UserManager()),
            ],
        ),
    ]
