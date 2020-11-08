# Generated by Django 2.2.17 on 2020-11-08 12:11

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TodoList',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField(default='')),
                ('status', models.CharField(blank=True, default='not_start', max_length=10)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('todo_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='api.TodoList')),
            ],
            options={
                'ordering': ('deadline',),
                'unique_together': {('title', 'todo_list')},
            },
        ),
    ]
