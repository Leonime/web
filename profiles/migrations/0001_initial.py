# Generated by Django 3.0.8 on 2020-07-09 13:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import thumbnails.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(blank=True, help_text='The user location', max_length=220, null=True)),
                ('bio', models.TextField(blank=True, help_text='The user bio', null=True)),
                ('image', thumbnails.fields.ImageField(blank=True, help_text='The profile picture', max_length=1024, null=True, upload_to='profiles/profile/')),
                ('email_confirmed', models.BooleanField(default=False, help_text='Tells if email has been confirmed.')),
                ('followers', models.ManyToManyField(blank=True, help_text='The user followers', related_name='following', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(help_text='The user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalProfile',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('location', models.CharField(blank=True, help_text='The user location', max_length=220, null=True)),
                ('bio', models.TextField(blank=True, help_text='The user bio', null=True)),
                ('image', models.CharField(blank=True, help_text='The profile picture', max_length=1024, null=True)),
                ('email_confirmed', models.BooleanField(default=False, help_text='Tells if email has been confirmed.')),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.TextField(null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, help_text='The user', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical profile',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
