# Generated by Django 5.2.4 on 2025-07-17 17:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FootballCompetition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Competition_Name', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='FootballFederationM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Fed_Name', models.CharField(max_length=20)),
                ('Type_Fed', models.CharField(choices=[('GL', 'GLOBAL'), ('CN', 'CONTINENTAL')], max_length=2)),
                ('Founded_Year', models.PositiveIntegerField()),
                ('Members', models.IntegerField(help_text='Dont counting associate members')),
                ('Associate_Member', models.IntegerField(blank=True, default=0, help_text='Members who not full join to federation. Default value 0')),
                ('Main_tournament', models.CharField()),
            ],
            options={
                'verbose_name': 'FootballFederation',
                'verbose_name_plural': 'FootballFederations',
            },
        ),
        migrations.CreateModel(
            name='FootballLeague',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('League_Name', models.CharField()),
                ('Country', models.CharField()),
                ('Count_Team', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FootballTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Team_Name', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='CountryFootball',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Country_Name', models.CharField()),
                ('Tournament_In_Country', models.ManyToManyField(related_name='countries', to='db.footballcompetition')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='FootballSeason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Start_Season', models.PositiveIntegerField()),
                ('End_Season', models.PositiveIntegerField()),
                ('Season_League', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season', to='db.footballleague')),
            ],
        ),
        migrations.CreateModel(
            name='Standings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Match_Played', models.PositiveIntegerField()),
                ('Season_Year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.footballseason')),
                ('Standing_League', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.footballleague')),
            ],
        ),
    ]
