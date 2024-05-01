# Generated by Django 5.0.2 on 2024-05-01 16:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('drive_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('relevance_score', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=500)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=256)),
                ('vote_type', models.CharField(choices=[('UP', 'Up'), ('DOWN', 'Down')], max_length=4)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docu_query.document')),
            ],
            options={
                'indexes': [models.Index(fields=['user', 'document'], name='docu_query__user_6472b4_idx')],
                'unique_together': {('user', 'document')},
            },
        ),
    ]
