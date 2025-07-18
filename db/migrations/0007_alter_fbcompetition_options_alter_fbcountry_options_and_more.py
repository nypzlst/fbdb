# Generated by Django 5.2.4 on 2025-07-18 15:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0006_alter_fbleague_country_league'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fbcompetition',
            options={'ordering': ['competition_name'], 'verbose_name': 'Football Competition', 'verbose_name_plural': 'Football Competions'},
        ),
        migrations.AlterModelOptions(
            name='fbcountry',
            options={'ordering': ['country_name'], 'verbose_name': 'Country', 'verbose_name_plural': 'Countries'},
        ),
        migrations.AlterModelOptions(
            name='fbleague',
            options={'verbose_name': 'Football League', 'verbose_name_plural': 'Football Leagues'},
        ),
        migrations.AlterModelOptions(
            name='fbseason',
            options={'ordering': ['name_league'], 'verbose_name': 'Football Season', 'verbose_name_plural': 'Football Seasons'},
        ),
        migrations.AlterModelOptions(
            name='fbstandings',
            options={'verbose_name': 'Football Standing', 'verbose_name_plural': 'Football Standings'},
        ),
        migrations.AlterModelOptions(
            name='fbteam',
            options={'verbose_name': 'Football Team', 'verbose_name_plural': 'Football Teams'},
        ),
        migrations.AddField(
            model_name='fbteam',
            name='league_where_play_team',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='db.fbleague'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fbleague',
            name='league_name',
            field=models.ForeignKey(limit_choices_to={'type_competition': 'L'}, on_delete=django.db.models.deletion.CASCADE, to='db.fbcompetition'),
        ),
        migrations.CreateModel(
            name='FbMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_team_score', models.PositiveSmallIntegerField(default=0)),
                ('away_team_score', models.PositiveSmallIntegerField(default=0)),
                ('match_time', models.DateTimeField()),
                ('away_team', models.ForeignKey(limit_choices_to={'league_where_play_team': models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='league_match', to='db.fbleague')}, on_delete=django.db.models.deletion.CASCADE, related_name='away_team', to='db.fbteam')),
                ('home_team', models.ForeignKey(limit_choices_to={'league_where_play_team': models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='league_match', to='db.fbleague')}, on_delete=django.db.models.deletion.CASCADE, related_name='home_team', to='db.fbteam')),
                ('match_on_league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='league_match', to='db.fbleague')),
            ],
        ),
    ]
