# Generated by Django 3.1 on 2020-08-08 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_mission_mission_events_sortie'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={},
        ),
        migrations.AddField(
            model_name='mission_events',
            name='data',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='player',
            name='account_id',
            field=models.CharField(db_index=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='name',
            field=models.CharField(db_index=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='profile_id',
            field=models.CharField(db_index=True, max_length=40, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set(),
        ),
        migrations.AlterModelTable(
            name='player',
            table=None,
        ),
        migrations.RemoveField(
            model_name='player',
            name='accuracy',
        ),
        migrations.RemoveField(
            model_name='player',
            name='ak_assist',
        ),
        migrations.RemoveField(
            model_name='player',
            name='ak_total',
        ),
        migrations.RemoveField(
            model_name='player',
            name='bailout',
        ),
        migrations.RemoveField(
            model_name='player',
            name='captured',
        ),
        migrations.RemoveField(
            model_name='player',
            name='ce',
        ),
        migrations.RemoveField(
            model_name='player',
            name='crashed',
        ),
        migrations.RemoveField(
            model_name='player',
            name='dead',
        ),
        migrations.RemoveField(
            model_name='player',
            name='disco',
        ),
        migrations.RemoveField(
            model_name='player',
            name='ditched',
        ),
        migrations.RemoveField(
            model_name='player',
            name='elo',
        ),
        migrations.RemoveField(
            model_name='player',
            name='fairplay',
        ),
        migrations.RemoveField(
            model_name='player',
            name='fairplay_time',
        ),
        migrations.RemoveField(
            model_name='player',
            name='fak_total',
        ),
        migrations.RemoveField(
            model_name='player',
            name='fgk_total',
        ),
        migrations.RemoveField(
            model_name='player',
            name='flight_time',
        ),
        migrations.RemoveField(
            model_name='player',
            name='ft_streak_current',
        ),
        migrations.RemoveField(
            model_name='player',
            name='ft_streak_max',
        ),
        migrations.RemoveField(
            model_name='player',
            name='gk_total',
        ),
        migrations.RemoveField(
            model_name='player',
            name='gkd',
        ),
        migrations.RemoveField(
            model_name='player',
            name='gkhr',
        ),
        migrations.RemoveField(
            model_name='player',
            name='gkl',
        ),
        migrations.RemoveField(
            model_name='player',
            name='gks',
        ),
        migrations.RemoveField(
            model_name='player',
            name='in_flight',
        ),
        migrations.RemoveField(
            model_name='player',
            name='kd',
        ),
        migrations.RemoveField(
            model_name='player',
            name='khr',
        ),
        migrations.RemoveField(
            model_name='player',
            name='kl',
        ),
        migrations.RemoveField(
            model_name='player',
            name='ks',
        ),
        migrations.RemoveField(
            model_name='player',
            name='landed',
        ),
        migrations.RemoveField(
            model_name='player',
            name='lost_aircraft_current',
        ),
        migrations.RemoveField(
            model_name='player',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='player',
            name='relive',
        ),
        migrations.RemoveField(
            model_name='player',
            name='respawn',
        ),
        migrations.RemoveField(
            model_name='player',
            name='score_streak_current',
        ),
        migrations.RemoveField(
            model_name='player',
            name='score_streak_max',
        ),
        migrations.RemoveField(
            model_name='player',
            name='shotdown',
        ),
        migrations.RemoveField(
            model_name='player',
            name='sortie_max_ak',
        ),
        migrations.RemoveField(
            model_name='player',
            name='sortie_max_gk',
        ),
        migrations.RemoveField(
            model_name='player',
            name='sorties_streak_current',
        ),
        migrations.RemoveField(
            model_name='player',
            name='sorties_streak_max',
        ),
        migrations.RemoveField(
            model_name='player',
            name='streak_current',
        ),
        migrations.RemoveField(
            model_name='player',
            name='streak_ground_current',
        ),
        migrations.RemoveField(
            model_name='player',
            name='streak_ground_max',
        ),
        migrations.RemoveField(
            model_name='player',
            name='streak_max',
        ),
        migrations.RemoveField(
            model_name='player',
            name='takeoff',
        ),
        migrations.RemoveField(
            model_name='player',
            name='type',
        ),
        migrations.RemoveField(
            model_name='player',
            name='wl',
        ),
        migrations.RemoveField(
            model_name='player',
            name='wounded',
        ),
    ]
