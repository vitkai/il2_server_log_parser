# Generated by Django 3.1 on 2020-09-07 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airfield',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airfield_id', models.IntegerField(unique=True)),
                ('pos_x', models.FloatField(blank=True, null=True)),
                ('pos_y', models.FloatField(blank=True, null=True)),
                ('pos_z', models.FloatField(blank=True, null=True)),
            ],
        ),
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
            name='Mission_Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField()),
                ('object_name', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=128)),
                ('country_id', models.IntegerField()),
                ('tik', models.IntegerField()),
                ('date_spawn', models.DateTimeField(blank=True, null=True)),
                ('game_date_spawn', models.DateTimeField(blank=True, null=True)),
                ('parent_id', models.IntegerField(blank=True, null=True)),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.mission')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.CharField(db_index=True, max_length=40, null=True)),
                ('profile_id', models.CharField(db_index=True, max_length=40, null=True)),
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
            name='Player_Craft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airfield', models.IntegerField(blank=True, null=True)),
                ('pos_x', models.FloatField(blank=True, null=True)),
                ('pos_y', models.FloatField(blank=True, null=True)),
                ('pos_z', models.FloatField(blank=True, null=True)),
                ('bot_id', models.IntegerField(blank=True, null=True)),
                ('cartridges', models.IntegerField(blank=True, null=True)),
                ('shells', models.IntegerField(blank=True, null=True)),
                ('bombs', models.IntegerField(blank=True, null=True)),
                ('rockets', models.IntegerField(blank=True, null=True)),
                ('form', models.CharField(max_length=128)),
                ('airstart', models.BooleanField()),
                ('is_pilot', models.BooleanField()),
                ('payload_id', models.IntegerField(blank=True, null=True)),
                ('fuel', models.IntegerField(blank=True, null=True)),
                ('skin', models.CharField(max_length=128)),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.mission')),
                ('mission_object_plane', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.mission_object')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.player')),
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
            name='VLife',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=False)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.player')),
            ],
            options={
                'verbose_name': 'virtual life',
                'verbose_name_plural': 'virtual lives',
                'db_table': 'vlife',
            },
        ),
        migrations.CreateModel(
            name='Sortie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tik', models.IntegerField(blank=True, null=True)),
                ('player_role', models.CharField(choices=[('Pilot', 'plane pilot'), ('Gunner', 'plane gunner'), ('Tankman', 'tank player'), ('Tank_Gunner', 'Tank_Gunner')], default='Pilot', editable=False, max_length=25)),
                ('date_start', models.DateTimeField(blank=True, null=True)),
                ('date_end', models.DateTimeField(blank=True, null=True)),
                ('date_takeoff', models.DateTimeField(blank=True, null=True)),
                ('date_land', models.DateTimeField(blank=True, null=True)),
                ('flight_time', models.IntegerField(default=0)),
                ('duration', models.IntegerField(default=0)),
                ('is_alive', models.BooleanField(default=True)),
                ('is_bailed', models.BooleanField(default=False)),
                ('is_destroyed', models.BooleanField(default=False)),
                ('is_disco_after_damage', models.BooleanField(default=False)),
                ('is_disco_in_flight', models.BooleanField(default=False)),
                ('is_in_flight', models.BooleanField(default=False)),
                ('plane_damage', models.FloatField(default=0)),
                ('pilot_damage', models.FloatField(default=0)),
                ('hits', models.IntegerField(default=0)),
                ('kills', models.IntegerField(default=0)),
                ('hits_friend', models.IntegerField(default=0)),
                ('kills_friend', models.IntegerField(default=0)),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sorties_list', to='data.mission')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sorties_list', to='data.player')),
                ('player_craft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.player_craft')),
                ('vlife', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sorties_list', to='data.vlife')),
            ],
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64)),
                ('name_en', models.CharField(blank=True, max_length=64)),
                ('name_ru', models.CharField(blank=True, max_length=64)),
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
            name='Mission_Objective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coal', models.IntegerField()),
                ('object', models.IntegerField()),
                ('task_type', models.IntegerField()),
                ('tik', models.IntegerField(blank=True, db_index=True, null=True)),
                ('icon_type_id', models.IntegerField(blank=True, null=True)),
                ('pos_x', models.FloatField(blank=True, null=True)),
                ('pos_y', models.FloatField(blank=True, null=True)),
                ('pos_z', models.FloatField(blank=True, null=True)),
                ('success', models.BooleanField(default=False)),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.mission')),
            ],
        ),
        migrations.CreateModel(
            name='Mission_Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tik', models.IntegerField(blank=True, db_index=True, null=True)),
                ('account_id', models.CharField(db_index=True, max_length=40, null=True)),
                ('profile_id', models.CharField(db_index=True, max_length=40, null=True)),
                ('area_id', models.IntegerField(blank=True, null=True)),
                ('atype_id', models.IntegerField(blank=True, null=True)),
                ('airfield_id', models.IntegerField(blank=True, null=True)),
                ('aircraft_id', models.IntegerField(blank=True, null=True)),
                ('attacker_id', models.IntegerField(blank=True, null=True)),
                ('bot_id', models.IntegerField(blank=True, null=True)),
                ('coal_id', models.IntegerField(blank=True, null=True)),
                ('country_id', models.IntegerField(blank=True, null=True)),
                ('icon_type_id', models.IntegerField(blank=True, null=True)),
                ('group_id', models.IntegerField(blank=True, null=True)),
                ('leader_id', models.IntegerField(blank=True, null=True)),
                ('object_id', models.IntegerField(blank=True, null=True)),
                ('parent_id', models.IntegerField(blank=True, null=True)),
                ('payload_id', models.IntegerField(blank=True, null=True)),
                ('target_id', models.IntegerField(blank=True, null=True)),
                ('task_type_id', models.IntegerField(blank=True, null=True)),
                ('ammo', models.CharField(blank=True, max_length=40, null=True)),
                ('aircraft_name', models.CharField(blank=True, max_length=128, null=True)),
                ('airstart', models.BooleanField(default=False)),
                ('bombs', models.IntegerField(blank=True, null=True)),
                ('cartridges', models.IntegerField(blank=True, null=True)),
                ('damage', models.FloatField(blank=True, null=True)),
                ('form', models.CharField(blank=True, max_length=128, null=True)),
                ('fuel', models.IntegerField(blank=True, null=True)),
                ('is_pilot', models.BooleanField(default=False)),
                ('is_tracking_stat', models.BooleanField(default=False)),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('object_name', models.CharField(blank=True, max_length=128, null=True)),
                ('rockets', models.IntegerField(blank=True, null=True)),
                ('shells', models.IntegerField(blank=True, null=True)),
                ('skin', models.CharField(blank=True, max_length=128, null=True)),
                ('sortie_status', models.CharField(blank=True, max_length=40, null=True)),
                ('success', models.IntegerField(blank=True, null=True)),
                ('weapon_mods_id', models.IntegerField(blank=True, null=True)),
                ('enabled', models.BooleanField(default=False)),
                ('in_air', models.IntegerField(blank=True, null=True)),
                ('friendly_fire', models.BooleanField(default=False)),
                ('pos_x', models.FloatField(blank=True, null=True)),
                ('pos_y', models.FloatField(blank=True, null=True)),
                ('pos_z', models.FloatField(blank=True, null=True)),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.mission')),
                ('player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.player')),
                ('player_craft', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.player_craft')),
                ('sortie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.sortie')),
            ],
        ),
        migrations.CreateModel(
            name='Kill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tik', models.IntegerField(blank=True, null=True)),
                ('target_object_name', models.CharField(blank=True, max_length=128, null=True)),
                ('target_is_player', models.BooleanField(default=False)),
                ('target_is_friend', models.BooleanField(default=False)),
                ('target_is_kill', models.BooleanField(default=False)),
                ('target_damage', models.FloatField(default=0.0)),
                ('target_kill_share', models.FloatField(blank=True, null=True)),
                ('target_was_killed', models.BooleanField(default=False)),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.mission')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attacker_player', to='data.player')),
                ('sortie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.sortie')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.mission_object')),
                ('target_player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target_player', to='data.player')),
            ],
        ),
        migrations.CreateModel(
            name='Airfield_Mission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_id', models.IntegerField()),
                ('tik', models.IntegerField()),
                ('airfield', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.airfield')),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.mission')),
            ],
        ),
    ]
