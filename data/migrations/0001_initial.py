# Generated by Django 3.1 on 2020-08-09 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.IntegerField(unique=True)),
                ('name', models.CharField(blank=True, db_index=True, max_length=256)),
                ('date_start', models.DateTimeField(db_index=True)),
                ('date_end', models.DateTimeField()),
                ('duration', models.IntegerField(default=0)),
                ('game_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mission_Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('miss_log_id', models.IntegerField(db_index=True, default=0)),
                ('is_processed', models.BooleanField(default=False, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_id', models.CharField(db_index=True, max_length=40, null=True)),
                ('account_id', models.CharField(db_index=True, max_length=40, null=True)),
                ('name', models.CharField(db_index=True, max_length=128, null=True)),
                ('date_first_sortie', models.DateTimeField(null=True)),
                ('date_last_sortie', models.DateTimeField(null=True)),
                ('date_last_combat', models.DateTimeField(null=True)),
                ('score', models.BigIntegerField(db_index=True, default=0)),
                ('rating', models.BigIntegerField(db_index=True, default=0)),
                ('ratio', models.FloatField(default=1)),
                ('sorties_total', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(editable=False, unique=True)),
                ('nickname', models.CharField(db_index=True, max_length=128)),
                ('is_hide', models.BooleanField(db_index=True, default=False)),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
                'db_table': 'profiles',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(editable=False, max_length=24)),
                ('type', models.CharField(choices=[('int', 'integer'), ('pct', 'percent')], default='int', editable=False, max_length=3)),
                ('value', models.IntegerField(default=0, editable=False)),
                ('custom_value', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'score',
                'verbose_name_plural': 'scoring',
                'db_table': 'scoring',
                'ordering': ['key'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Sortie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=128)),
                ('date_start', models.DateTimeField(blank=True, null=True)),
                ('date_end', models.DateTimeField(blank=True, null=True)),
                ('flight_time', models.IntegerField(default=0)),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.mission')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sorties_list', to='data.player')),
            ],
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64)),
                ('log_name', models.CharField(editable=False, max_length=64, unique=True)),
                ('cls_base', models.CharField(blank=True, choices=[('aircraft', 'aircraft'), ('ammo', 'ammo'), ('block', 'block'), ('crew', 'crew'), ('turret', 'turret'), ('vehicle', 'vehicle')], max_length=24)),
                ('cls', models.CharField(blank=True, choices=[('aaa_heavy', 'aaa_heavy'), ('aaa_light', 'aaa_light'), ('aaa_mg', 'aaa_mg'), ('aerostat', 'aerostat'), ('aircraft_gunner', 'aircraft_gunner'), ('aircraft_heavy', 'aircraft_heavy'), ('aircraft_light', 'aircraft_light'), ('aircraft_medium', 'aircraft_medium'), ('aircraft_pilot', 'aircraft_pilot'), ('aircraft_static', 'aircraft_static'), ('aircraft_transport', 'aircraft_transport'), ('aircraft_turret', 'aircraft_turret'), ('armoured_vehicle', 'armoured_vehicle'), ('artillery_field', 'artillery_field'), ('artillery_howitzer', 'artillery_howitzer'), ('artillery_rocket', 'artillery_rocket'), ('block', 'block'), ('bomb', 'bomb'), ('building_big', 'building_big'), ('building_medium', 'building_medium'), ('building_small', 'building_small'), ('bullet', 'bullet'), ('car', 'car'), ('driver', 'driver'), ('explosion', 'explosion'), ('locomotive', 'locomotive'), ('machine_gunner', 'machine_gunner'), ('parachute', 'parachute'), ('rocket', 'rocket'), ('searchlight', 'searchlight'), ('ship', 'ship'), ('ship_heavy', 'ship_heavy'), ('ship_light', 'ship_light'), ('ship_medium', 'ship_medium'), ('shell', 'shell'), ('tank_heavy', 'tank_heavy'), ('tank_light', 'tank_light'), ('tank_medium', 'tank_medium'), ('tank_driver', 'tank_driver'), ('tank_turret', 'tank_turret'), ('trash', 'trash'), ('truck', 'truck'), ('vehicle_crew', 'vehicle_crew'), ('vehicle_static', 'vehicle_static'), ('vehicle_turret', 'vehicle_turret'), ('wagon', 'wagon')], max_length=24)),
                ('is_playable', models.BooleanField(default=False, editable=False)),
                ('score', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.score')),
            ],
            options={
                'verbose_name': 'object',
                'verbose_name_plural': 'objects',
                'db_table': 'objects',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Mission_Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.IntegerField(unique=True)),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.mission')),
                ('sorties', models.ManyToManyField(to='data.Sortie')),
            ],
        ),
    ]
