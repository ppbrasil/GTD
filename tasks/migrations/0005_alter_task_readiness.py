# Generated by Django 3.2.16 on 2023-01-31 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_task_readiness'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='readiness',
            field=models.CharField(choices=[('inbox', 'Inbox'), ('anytime', 'Anytime'), ('waiting', 'Waiting'), ('sometime', 'Sometime')], default='inbox', max_length=20),
        ),
    ]
