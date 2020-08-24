"""
Descr: main module to operate log parsing
@author: vaal, corvit
Created: Fri Jul 24 2020 13:45 MSK
"""
import functools
import logging
import os
import pytz
import re
import time

from django.conf import settings
from datetime import datetime, timedelta
from ast import literal_eval

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
# Ensure settings are read
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from data.models import Airfield, Airfield_Mission, Mission, Mission_Event, Mission_Object, Mission_Objective, Player, \
    Player_Craft, Sortie

logger = logging.getLogger(__name__)
global mission, tik_last

GAME_CLASSES = (
    'CAeroplaneFragment',
    'CAerostat',
    'CAerostatAI',
    'CAIPoi',
    'CAirfield',
    'CAnimationOperator',
    'CAttachedVehicle',
    'CBallistics',
    'CBanner',
    'CBatchBallistics',
    'CBatchExplosion',
    'CBatchTrash',
    'CBatchTrashAnimated',
    'CBFManager',
    'CBlocksArray',
    'CBombSiteAim',
    'CBot',
    'CBotAimingHead',
    'CBotCharacter',
    'CBotController',
    'CBotFieldController',
    'CBotHead',
    'CBotInputController',
    'CCameraOperator',
    'CCloudSky',
    'CClusterBallistics',
    'CCommanderInputController',
    'CComplexTrigger',
    'CCumulativeRocket',
    'CDFMission',
    'CDistantLOD',
    'CDummyObject',
    'CEjectionPlace',
    'CEjectorController',
    'CFlag',
    'CFlareGun',
    'CForestBody',
    'CGameChat',
    'CGameMission',
    'CInfluenceArea',
    'CMouseControlCameraOperator',
    'CParachute',
    'CParachutedContainer',
    'CParatroopersCreator',
    'CPhysPlatformRadioTurretAI',
    'CPlane',
    'CPlaneAI',
    'CPlaneInputController',
    'CPlatformTank',
    'CRobotCameraOperator',
    'CRocket',
    'CSharedGroup',
    'CShip',
    'CShipAI',
    'CSolidTrash',
    'CSpotlight',
    'CSpotter',
    'CStaticBlock',
    'CStaticEmitter',
    'CStaticVehicle',
    'CSubmarine',
    'CTank',
    'CTerrainArray',
    'CTorpedo',
    'CTrainAI',
    'CTrainLocomotive',
    'CTrainWagon',
    'CTrash',
    'CTrashAnimated',
    'CTruck',
    'CTurret',
    'CTurretCamera',
    'CTurretRadioAI',
    'CTurretRadioAIInputController',
    'CTurretRiffle',
    'CVehicleAI',
    'CVehicleExplosionTurret',
    'CVehicleInputController',
    'CVehicleRangefinderTurret',
    'CVehicleRangefinderTurretAI',
    'CVehicleRocketTurret',
    'CVehicleRocketTurretAI',
    'CVehicleTorpedoTurret',
    'CVehicleTorpedoTurretAI',
    'CVehicleTurret',
    'CVehicleTurretAI',
    'CVehicleTurretInputController',
    'CWindsock',
)

@functools.lru_cache(maxsize=1024)
def object_name_handler(type_):
    # :type type_: str
    if type_.startswith(GAME_CLASSES):
        return type_.split('_')[0]
    else:
        return type_


# старт миссии
# T:0 AType:0 GDate:1942.9.19 GTime:14:0:0 MFile:Multiplayer/Dogfight\result.msnbin MID: GType:2 CNTRS:0:0,101:1,201:2
# SETTS:000000000010000100000000110 MODS:0 PRESET:0 AQMID:0 ROUNDS: 1 POINTS: 15000
atype_0 = re.compile(r'^T:(?P<tik>\d+) AType:0 GDate:(?P<date>(\d{4}.\d{1,2}.\d{1,2} GTime:\d{1,2}:\d{1,2}:\d{1,2})) '
                     r'MFile:(?P<file_path>.+) MID:\d* GType:(?P<game_type_id>\d+) CNTRS:(?P<countries>[,:\d]+) '
                     r'SETTS:(?P<settings>\d+) MODS:(?P<mods>\d) PRESET:(?P<preset_id>\d)')

# попадание пули/бомбы в объект
# T:63164 AType:1 AMMO:BULLET_GER_792x57_SS AID:138247 TID:59392
atype_1 = re.compile(r'^T:(?P<tik>\d+) AType:1 AMMO:(?P<ammo>[-\w]+) AID:(?P<attacker_id>\d+) TID:(?P<target_id>\d+)$')

# повреждение (дамаг может быть отрицательным - баг?)
# T:524734 AType:2 DMG:0.007 AID:172089 TID:133194 POS(23876.303,119.281,28392.604)
# atype_2 = parse_tpl('T:<tik> AType:2 DMG:<damage> AID:<attacker_id> TID:<target_id> POS(<pos>)')
atype_2 = re.compile(r'^T:(?P<tik>\d+) AType:2 DMG:(?P<damage>\S{5,6}) AID:(?P<attacker_id>[-\d]+) '
                     r'TID:(?P<target_id>[-\d]+) POS\((?P<pos>.+)\)$')

# убийство/смерть
# T:26383 AType:3 AID:107527 TID:106497 POS(25131.697,744.438,23284.689)
atype_3 = re.compile(r'^T:(?P<tik>\d+) AType:3 AID:(?P<attacker_id>[-\d]+) '
                     r'TID:(?P<target_id>[-\d]+) POS\((?P<pos>.+)\)$')

# конец вылета
# T:27071 AType:4 PLID:106497 PID:107521 BUL:869 SH:0 BOMB:0 RCT:0 (25727.014,57.894,23335.092)
atype_4 = re.compile(r'^T:(?P<tik>\d+) AType:4 PLID:(?P<aircraft_id>\d+) PID:(?P<bot_id>\d+) BUL:(?P<cartridges>\d+) '
                     r'SH:(?P<shells>\d+) BOMB:(?P<bombs>\d+) RCT:(?P<rockets>\d+) \((?P<pos>.+)\)$')

# взлет (скорость больше чего то и высота больше 50 м)
# T:16960 AType:5 PID:109572 POS(23800.740, 116.003, 28128.986)
atype_5 = re.compile(r'^T:(?P<tik>\d+) AType:5 PID:(?P<aircraft_id>\d+) POS\((?P<pos>.+)\)$')

# приземление
# T:27080 AType:6 PID:106497 POS(25729.223, 58.303, 23334.037)
atype_6 = re.compile(r'^T:(?P<tik>\d+) AType:6 PID:(?P<aircraft_id>\d+) POS\((?P<pos>.+)\)$')

# завершение миссии
# T:525287 AType:7
atype_7 = re.compile(r'^T:(?P<tik>\d+) AType:7$')

# статус какой-то задачи в миссии
# T:3745 AType:8 OBJID:102 POS(37286.734,0.000,18839.822) COAL:1 TYPE:0 RES:1 ICTYPE:0
atype_8 = re.compile(r'^T:(?P<tik>\d+) AType:8 OBJID:(?P<object_id>\d+) POS\((?P<pos>.+)\) COAL:(?P<coal_id>\d) '
                     r'TYPE:(?P<task_type_id>\d+) RES:(?P<success>\d) ICTYPE:(?P<icon_type_id>[\-\d]+)$')

# инфа об аэродроме и какой самолет к нему привязан
# T:10 AType:9 AID:13312 COUNTRY:501 POS(30178.900, 66.126, 25254.000) IDS()
# T:10 AType:9 AID:22528 COUNTRY:101 POS(97874.656, 90.384, 141539.406) IDS(0,0,0)
# T:10 AType:9 AID:150527 COUNTRY:201 POS(144322.453, 82.669, 259528.047) IDS(-1,-1,-1)
atype_9 = re.compile(r'^T:(?P<tik>\d+) AType:9 AID:(?P<airfield_id>\d+) COUNTRY:(?P<country_id>\d{1,3}) '
                     r'POS\((?P<pos>.+)\) IDS\((?P<aircraft_id_list>[,\-\d]*)\)$')

# респаун игрока (INAIR: 0 - в воздухе, 1 - с полосы (двигатель вкл), 2 - со стоянки
# T:15 AType:10 PLID:276479 PID:277503 BUL:2000 SH:0 BOMB:0 RCT:0 (133119.406,998.935,185101.141)
# IDS:6f3b5e69-38d7-4d83-868c-4e7b8129f41a LOGIN:60dc67e3-ffb2-4df3-a6e5-579e945b4018 NAME:=FB=Vaal
# TYPE:Il-2 mod.1942 COUNTRY:101 FORM:0 FIELD:0 INAIR:0 PARENT:-1 ISPL:1 ISTSTART:1 PAYLOAD:0 FUEL:1.000 SKIN: WM:1
atype_10 = re.compile(r'^T:(?P<tik>\d+) AType:10 PLID:(?P<aircraft_id>\d+) PID:(?P<bot_id>\d+) BUL:(?P<cartridges>\d+) '
                      r'SH:(?P<shells>\d+) BOMB:(?P<bombs>\d+) RCT:(?P<rockets>\d+) \((?P<pos>.+)\) '
                      r'IDS:(?P<profile_id>[-\w]{36}) LOGIN:(?P<account_id>[-\w]{36}) NAME:(?P<name>.*) '
                      r'TYPE:(?P<aircraft_name>[\w\(\) .\-_/]+) COUNTRY:(?P<country_id>\d{1,3}) FORM:(?P<form>\d+) '
                      r'FIELD:(?P<airfield_id>\d+) INAIR:(?P<airstart>\d) PARENT:(?P<parent_id>[-\d]+) '
                      r'ISPL:(?P<is_pilot>\d+) ISTSTART:(?P<is_tracking_stat>\d+) '
                      r'PAYLOAD:(?P<payload_id>\d+) FUEL:(?P<fuel>\S{5,6}) '
                      r'SKIN:(?P<skin>[\S ]*) WM:(?P<weapon_mods_id>\d+)')


# группа объектов, с лидером и список членов
# T:1 AType:11 GID:115711 IDS:17407,26623,35839 LID:17407
atype_11 = re.compile(r'^T:(?P<tik>\d+) AType:11 GID:(?P<group_id>\d+) '
                      r'IDS:(?P<members_id>[,\d]*) LID:(?P<leader_id>\d+)$')

# респаун какого-то игрового объекта
# T:504220 AType:12 ID:410733 TYPE:Sopwith Camel COUNTRY:102 NAME:noname PID:-1
# T:53 AType:12 ID:61440 TYPE:bridge_big_1[265,1] COUNTRY:201 NAME:Bridge PID:-1
# T:48738 AType:12 ID:649216 TYPE:static_zis[-1,-1] COUNTRY:101 NAME:Block PID:-1
# T:171760 AType:12 ID:1266700 TYPE:CParachute_1266700 COUNTRY:101 NAME:CParachute_1266700 PID:-1
# T:15 AType:12 ID:137215 TYPE:LaGG-3 ser.29 COUNTRY:101 NAME:LaGG-3 ser.29 PID:-1 POS(19666.344,998.778,33864.637)
atype_12 = re.compile(r'^T:(?P<tik>\d+) AType:12 ID:(?P<object_id>\d+) '
                      r'TYPE:(?P<object_name>[ .\'\-\w\(\)/]*)(\[-?\d+,-?\d+\])* '
                      r'COUNTRY:(?P<country_id>\d{1,3}) NAME:(?P<name>.*) PID:(?P<parent_id>[-\d]+)')

# зона, количество самолетов в воздухе для каждой коалиции (0, 1, 2, 3, 4, 5, 6, 7) находящихся в данный момент в зоне
# T:0 AType:13 AID:39936 COUNTRY:501 ENABLED:1 BC(0,0,0,0,0,0,0,0)
atype_13 = re.compile(r'^T:(?P<tik>\d+) AType:13 AID:(?P<area_id>\d+) COUNTRY:(?P<country_id>\d{1,3}) '
                      r'ENABLED:(?P<enabled>\d) BC\((?P<in_air>[,\d]+)\)$')

# границы зоны, список вершин зоны (произвольный многоугольник)
# T:1 AType:14 AID:39936 BP((26968.0,74.3,22949.0),(30848.0,74.3,23891.0),(35717.0,74.3,23876.0),(55007.0,74.3,15026.0),
# (55001.0,74.3,55020.0),(-5018.0,74.3,55042.0),(-4991.0,74.3,34620.0),(2552.0,74.3,34401.0),(8185.0,74.3,29341.0),
# (17968.0,74.3,26690.0),(21055.0,74.3,27434.0),(22561.0,74.3,24669.0),(25287.6,74.3,24965.3))
atype_14 = re.compile(r'^T:(?P<tik>\d+) AType:14 AID:(?P<area_id>\d+) BP(?P<boundary>[-,\(\)\.\d]+)$')

# версия системы логов?
# T:0 AType:15 VER:17
atype_15 = re.compile(r'^T:(?P<tik>\d+) AType:15 VER:(?P<version>\d+)$')

# утилизация объекта?
# T:32497 AType:16 BOTID:108551 POS(23899.598,154.684,20580.168)
atype_16 = re.compile(r'^T:(?P<tik>\d+) AType:16 BOTID:(?P<bot_id>\d+) POS\((?P<pos>.+)\)$')

# текущая позиция объекта
# T:58 AType:17 ID:107519 POS(39013.016,45.535,16807.107)
atype_17 = re.compile(r'^T:(?P<tik>\d+) AType:17 ID:(?P<object_id>\d+) POS\((?P<pos>.+)\)$')

# прыжок?
# T:68207 AType:18 BOTID:1662987 PARENTID:1661963 POS(103313.617,358.759,168764.578)
atype_18 = re.compile(r'^T:(?P<tik>\d+) AType:18 BOTID:(?P<bot_id>\d+) '
                      r'PARENTID:(?P<parent_id>[-\d]+) POS\((?P<pos>.+)\)$')

# конец раунда
# T:706771 AType:19
atype_19 = re.compile(r'^T:(?P<tik>\d+) AType:19$')

# вход игрока
# T:2126 AType:20 USERID:3cf05e60-809a-4c12-bfa4-832f6d282f0d USERNICKID:19ce5f28-1bd6-4116-9e5e-fbe1cb955da3
atype_20 = re.compile(r'^T:(?P<tik>\d+) AType:20 USERID:(?P<account_id>[-\w]{36}) USERNICKID:(?P<profile_id>[-\w]{36})$')

# выход игрока
# T:18573 AType:21 USERID:d5bc9e4c-055c-46c2-8ace-8a7daa9eed4a USERNICKID:e608236e-332a-4843-8421-8e013c59685f
atype_21 = re.compile(r'^T:(?P<tik>\d+) AType:21 USERID:(?P<account_id>[-\w]{36}) USERNICKID:(?P<profile_id>[-\w]{36})$')

# начало движения танка
# T:36160 AType:22 PID:1684580 POS(223718.406, 10.337, 242309.250)
atype_22 = re.compile(r'^T:(?P<tik>\d+) AType:22 PID:(?P<parent_id>[-\d]+) POS\((?P<pos>.+)\)$')


atype_handlers = [
    atype_0, atype_1, atype_2, atype_3, atype_4, atype_5, atype_6, atype_7, atype_8, atype_9, atype_10, atype_11,
    atype_12, atype_13, atype_14, atype_15, atype_16, atype_17, atype_18, atype_19, atype_20, atype_21, atype_22,
]


re_pos = re.compile(r'[.\-\d]+,\s*[.\-\d]+,\s*[.\-\d]+')

def pos_handler(pos):
    """
    :type pos: str
    """
    if re_pos.match(pos.strip()):
        pos = tuple(map(float, pos.split(',')))
        return dict(zip(['x', 'y', 'z'], pos))
    else:
        return None


param_handlers = {
    'aircraft_id': int,
    'bombs': int,
    'bot_id': int,
    'cartridges': int,
    'coal_id': int,
    'country_id': int,
    'game_type_id': int,
    'leader_id': int,
    'payload_id': int,
    'preset_id': int,
    'rockets': int,
    'shells': int,
    'target_id': int,
    'task_type_id': int,
    'tik': int,
    'group_id': int,
    'object_id': int,
    'area_id': int,

    'attacker_id': lambda s: int(s) if s != '-1' else None,
    'aircraft_id_list': lambda s: list(map(int, s.split(','))) if s else [],
    'airfield_id': lambda s: int(s) or None,
    'airstart': lambda s: s == '0',
    'is_pilot': lambda s: s == '1',
    'boundary': literal_eval,
    'countries': lambda s: dict(map(int, x.split(':')) for x in s.split(',')),
    'damage': lambda s: round(float(s) * 100, 1) if '#' not in s else None,
    'date': lambda s: datetime.strptime(s, '%Y.%m.%d GTime:%H:%M:%S'),
    'enabled': lambda s: s == '1',
    'fuel': lambda s: float(s) * 100 if '#' not in s else None,
    'icon_type_id': lambda s: int(s) if s != '-1' else None,
    'in_air': lambda s: [int(s) for s in s.split(',')],
    'members_id': lambda s: list(map(int, s.split(','))) if s else [],
    'mods': lambda s: s == '1',
    'parent_id': lambda s: int(s) if s != '-1' else None,
    'pos': pos_handler,
    'settings': lambda s: tuple(map(int, s)),
    'success': lambda s: s == '1',
    'object_name': object_name_handler,
    #'weapon_mods_id': lambda s: [i for i, wm in enumerate(bin(int(s))[2:-1][::-1], start=1) if wm == '1'],
    'weapon_mods_id': int,
}


def pos_to_tup(pos):
    return (pos['x'], pos['y'], pos['z'])


def add_mission_event(**kwargs):
    if 'pos' in kwargs:
        pos = kwargs.pop('pos')
        kwargs['pos_x'], kwargs['pos_y'], kwargs['pos_z'] = pos_to_tup(pos)

    kwargs['mission'] = mission

    if not Mission_Event.objects.filter(mission=mission, sortie=kwargs['sortie'], tik=kwargs['tik'],
                                    atype_id=kwargs['atype_id']).exists():
        mission_event =Mission_Event.objects.create(**kwargs)
        mission_event.save()


def event_mission_start(**kwargs):
    global mission

    mission.game_date = kwargs['date']
    mission.save()
    pass


def event_hit(**kwargs):
    # data: {'tik': 36542, 'ammo': 'NPC_SHELL_RUS_25_HE', 'attacker_id': 834560, 'target_id': 9218, 'atype_id': 1}
    kwargs['sortie_status'] = 'hit'
    event_damage(**kwargs)


def event_damage(**kwargs):
    # data: {'tik': 24925, 'damage': 0.3, 'attacker_id': None, 'target_id': 10244,
    #               'pos': {'x': 119480.9688, 'y': 56.9919, 'z': 156564.7344}, 'atype_id': 2}
    # logger.debug('Event handler for [event_damage] is empty')

    # looking for attacker's player craft
    if (kwargs['attacker_id'] is not None) and \
            Mission_Object.objects.filter(object_id=kwargs['attacker_id']).exists():
        attacker = Mission_Object.objects.get(object_id=kwargs['attacker_id'])
        if Player_Craft.objects.filter(mission_object_plane=attacker).exists():
            attacker = Player_Craft.objects.get(mission_object_plane=attacker)

            sortie = Sortie.objects.get(player_craft=attacker)
            if 'sortie_status' not in kwargs:
                kwargs['sortie_status'] = 'damaged'
            elif kwargs['sortie_status'] == 'kill':
                sortie.kills = sortie.kills + 1
            elif kwargs['sortie_status'] == 'hit':
                sortie.hits = sortie.hits + 1

            sortie.is_in_flight = True
            sortie.save()

            kwargs['sortie'] = sortie
            kwargs['player_craft'] = attacker

            add_mission_event(**kwargs)

    # looking for target's player craft
    parent_object = False
    pilot_object = False
    add_event = False
    if (kwargs['target_id'] is not None) and \
            Mission_Object.objects.filter(object_id=kwargs['target_id']).exists():
        real_target = Mission_Object.objects.filter(object_id=kwargs['target_id']).first()

        # if Player Craft exists for given mission object, we need to update Sortie
        if Player_Craft.objects.filter(mission_object_plane=real_target).exists():
            target = Player_Craft.objects.get(mission_object_plane=real_target)
            parent_object = True
            add_event = True
        elif Mission_Object.objects.filter(object_id=real_target.parent_id).exists():
            target = Mission_Object.objects.get(object_id=real_target.parent_id)
            if real_target.object_name.startswith('BotPilot'):
                pilot_object = True
            if Player_Craft.objects.filter(mission_object_plane=target).exists():
                target = Player_Craft.objects.get(mission_object_plane=target)
                add_event = True

        if add_event:
            sortie = Sortie.objects.get(player_craft=target)
            if 'sortie_status' not in kwargs:
                if 'damage' in kwargs:
                    kwargs['sortie_status'] = 'was damaged'
                    # update sortie for parent object (player craft)
                    if parent_object:
                        sortie.plane_damage = sortie.plane_damage + kwargs['damage']
                        sortie.is_in_flight = True
                        sortie.save()
                    # update sortie if player (pilot)
                    elif pilot_object:
                        sortie.pilot_damage = sortie.pilot_damage + kwargs['damage']
                        sortie.is_in_flight = True
                        sortie.save()
                else:
                    kwargs['sortie_status'] = 'hit'
            elif kwargs['sortie_status'] == 'kill':
                if parent_object:
                    sortie.is_destroyed = True
                    sortie.save()
                # update sortie if player (pilot)
                elif pilot_object:
                    sortie.is_alive = False
                    sortie.save()

            kwargs['player_craft'] = target
            kwargs['sortie'] = sortie

            add_mission_event(**kwargs)
    pass


def event_kill(**kwargs):
    # data: {'tik': 37104, 'attacker_id': 8195, 'target_id': 64515,
    #       'pos': {'x': 105927.6953, 'y': 52.026, 'z': 182844.0625}, 'atype_id': 3}

    kwargs['sortie_status'] = 'kill'
    event_damage(**kwargs)


def event_sortie_end(**kwargs):
    # data: {'tik': 25486, 'aircraft_id': 10244, 'bot_id': 11268, 'cartridges': 5175, 'shells': 0, 'bombs': 6,
    #   'rockets': 0, 'pos': {'x': 119494.9531, 'y': 55.5708, 'z': 156456.7188}, 'atype_id': 4}

    kwargs['sortie_status'] = 'end'
    """
    if kwargs['aircraft_id'] == 0:
        miss_obj = Mission_Object.objects.get(object_id=kwargs['bot_id'], mission_id=mission)
        miss_obj = Mission_Object.objects.get(object_id=miss_obj.parent_id, mission_id=mission)
    else:
        miss_obj = Mission_Object.objects.get(object_id=kwargs['aircraft_id'], mission_id=mission)
    player_craft = Player_Craft.objects.get(mission_object_plane=miss_obj)
    """
    player_craft = Player_Craft.objects.get(bot_id=kwargs['bot_id'])
    kwargs['player_craft'] = player_craft

    sortie_upd(**kwargs)


def event_takeoff(**kwargs):
    global mission

    # data: {'tik': 18990, 'aircraft_id': 8195, 'pos': {'x': 119872.8906, 'y': 77.0816, 'z': 158145.7813}, 'atype_id': 5}
    # logger.debug('Event handler for [event_takeoff] is empty')
    player_craft = Mission_Object.objects.get(object_id=kwargs['aircraft_id'], mission_id=mission)
    # print(f'Mission object: {player_craft}')
    player_craft = Player_Craft.objects.get(mission_object_plane=player_craft)
    # print(f'Player Craft: {player_craft}')

    kwargs['player_craft'] = player_craft
    kwargs['sortie_status'] = 'takeoff'
    # kwargs['player_id'] = player_craft.player

    player_upd(**kwargs)
    sortie_upd(**kwargs)


def event_landing(**kwargs):
    # data: {'tik': 46530, 'aircraft_id': 9218, 'pos': {'x': 104675.8281, 'y': 77.5108, 'z': 181554.7188}, 'atype_id': 6}
    global mission

    player_craft = Mission_Object.objects.get(object_id=kwargs['aircraft_id'], mission_id=mission)
    player_craft = Player_Craft.objects.get(mission_object_plane=player_craft)

    kwargs['player_craft'] = player_craft
    kwargs['sortie_status'] = 'landing'

    sortie_upd(**kwargs)

    pass


def event_mission_end():
    pass


def event_mission_result(**kwargs):
    # data: {'tik': 1105, 'object_id': 64137, 'pos': {'x': 118595.8047, 'y': 67.232, 'z': 227313.5625}, 'coal_id': 1,
    #       'task_type_id': 14, 'success': True, 'icon_type_id': None, 'atype_id': 8}
    global mission

    if not Mission_Objective.objects.filter(mission=mission, object=kwargs['object_id']).exists():
        # Add objective
        mis_objective = Mission_Objective(mission=mission, object=kwargs['object_id'], tik=kwargs['tik'],
                                          coal=kwargs['coal_id'], task_type=kwargs['task_type_id'],
                                          success=kwargs['success'], icon_type_id=kwargs['icon_type_id'],
                                          pos_x=kwargs['pos']['x'], pos_y=kwargs['pos']['y'], pos_z=kwargs['pos']['z'])
        mis_objective.save()


def event_airfield(**kwargs):
    # airfield initialization event
    """
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    airfield_id = models.IntegerField(unique=True)
    country_id = models.IntegerField()
    tik = models.IntegerField()"""

    if Airfield.objects.filter(airfield_id=kwargs['airfield_id']).exists():
        logger.info(f"Airfield [{kwargs['airfield_id']}] - exists in the DB")
        airfield = Airfield.objects.get(airfield_id=kwargs['airfield_id'])
    else:
        # Add airfield
        airfield = Airfield(airfield_id=kwargs['airfield_id'], pos_x=kwargs['pos']['x'], pos_y=kwargs['pos']['y'],
                            pos_z=kwargs['pos']['z'])
        airfield.save()

    # check whether airfiled exists in the current mission
    if not Airfield_Mission.objects.filter(mission=mission, airfield=airfield).exists():
        airfield_mission = Airfield_Mission(mission=mission, airfield=airfield, country_id=kwargs['country_id'],
                            tik=kwargs['tik'])
        airfield_mission.save()


def player_upd(**kwargs):
    if kwargs['atype_id'] == 10:    # plane init
        if Player.objects.filter(profile_id=kwargs['profile_id'], account_id=kwargs['account_id']).exists():
            logger.info(f"Player [{kwargs['profile_id']}] - exists in the DB")
            player = Player.objects.get(profile_id=kwargs['profile_id'], account_id=kwargs['account_id'])
        else:
            # Add Player
            name = ''
            if 'name' in kwargs:
                name = kwargs['name']
            player = Player(profile_id=kwargs['profile_id'], account_id=kwargs['account_id'], name=name)
            player.save()

        return player
    elif kwargs['atype_id'] == 16:  # bot deinit
        """
        player_id = Player_Craft.objects.get(bot_id=kwargs['bot_id'])
        player = Player.objects.get(pk=player_id)

        player.sorties_total = player.sorties_total + 1
        player.save
        """
        pass
    elif kwargs['atype_id'] == 5:  # takeoff
        # player = Player.objects.get(pk=kwargs['player_craft'].player)
        player = kwargs['player_craft'].player
        # print(f"Player info: {player.account_id} | {player.sorties_total}")
        player.sorties_total = player.sorties_total + 1
        player.save()


def sortie_upd(**kwargs):
    global mission

    date_start = None
    # TODO rework date_start since it is the same as Mission_Object.date_spawn
    date_end = None
    date_takeoff = None
    date_land = None

    sortie_upd = False

    # print(f"kwargs['player_craft'] = {kwargs['player_craft']}")
    player_craft = kwargs['player_craft']

    if Sortie.objects.filter(mission=mission, player_craft=player_craft).exists():
        #logger.debug(f"Sortie [{mission_obj}] - exists in the DB")
        sortie = Sortie.objects.get(mission=mission, player_craft=player_craft)
    else:
        # Add player craft
        sortie = Sortie.objects.create(mission=mission, player=kwargs['player'], player_craft=player_craft)
        sortie_upd = True

    if kwargs['sortie_status'] == 'init':
        sortie.date_start = mission.date_start + timedelta(seconds=kwargs['tik'] // 50)
        sortie.plane_damage = 0
        sortie.pilot_damage = 0
        sortie_upd = True
    elif kwargs['sortie_status'] == 'end':
        date_end = mission.date_start + timedelta(seconds=kwargs['tik'] // 50)
        sortie.date_end = date_end
        sortie_upd = True
    elif kwargs['sortie_status'] == 'takeoff':
        sortie.date_takeoff = mission.date_start + timedelta(seconds=kwargs['tik'] // 50)
        sortie.is_in_flight = True
        sortie_upd = True
    elif kwargs['sortie_status'] == 'landing':
        sortie.date_land = mission.date_start + timedelta(seconds=kwargs['tik'] // 50)
        sortie.is_in_flight = False
        sortie_upd = True

    if sortie_upd:
        sortie.save()

    kwargs['sortie'] = sortie
    add_mission_event(**kwargs)


def event_player_plane(**kwargs):
    """
    data: {'tik': 8985, 'aircraft_id': 8195, 'bot_id': 9219, 'cartridges': 5195, 'shells': 0, 'bombs': 6, 'rockets': 0,
           'pos': {'x': 119464.8438, 'y': 57.2057, 'z': 156934.5781},
           'profile_id': 'e920869f-4f7b-4cfb-a216-2b49f48c8817', 'account_id': 'd7405e94-04f7-4026-84ad-35a9be5b15a1',
           'name': 'II./JG51Walther', 'aircraft_name': 'Bf 110 E-2', 'country_id': 201, 'form': '0',
           'airfield_id': 23552, 'airstart': False, 'parent_id': None, 'is_pilot': True, 'is_tracking_stat': '1',
           'payload_id': 5, 'fuel': 32.28, 'skin': '', 'weapon_mods_id': 17, 'atype_id': 10}
    """
    global mission

    player = player_upd(**kwargs)

    mission_obj = Mission_Object.objects.filter(object_id=kwargs['aircraft_id']).last()
    # mission_obj_bot = Mission_Object.objects.filter(object_id=kwargs['bot_id']).last()

    pos_x = kwargs['pos']['x']
    pos_y = kwargs['pos']['y']
    pos_z = kwargs['pos']['z']

    bot_id = kwargs["bot_id"]
    cartridges = kwargs["cartridges"]
    shells = kwargs["shells"]
    bombs = kwargs["bombs"]
    rockets = kwargs["rockets"]
    form = kwargs["form"]
    airstart = kwargs["airstart"]
    is_pilot = kwargs["is_pilot"]
    payload_id = kwargs["payload_id"]
    fuel = kwargs["fuel"]
    skin = kwargs["skin"]

    if Player_Craft.objects.filter(player=player, mission_object_plane=mission_obj).exists():
        logger.debug(f"Player_Craft [{mission_obj}] - exists in the DB")
        player_craft = Player_Craft.objects.get(player=player, mission_object_plane=mission_obj)
    else:
        # Add player craft
        player_craft = Player_Craft.objects.create(mission=mission, player=player, mission_object_plane=mission_obj,
                                                   bot_id=bot_id, cartridges=cartridges, shells=shells, bombs=bombs,
                                                   rockets=rockets, form=form, airstart=airstart, is_pilot=is_pilot,
                                                   payload_id=payload_id, fuel=fuel, skin=skin,
                                                   pos_x=pos_x, pos_y=pos_y, pos_z=pos_z)
        player_craft.save()

    kwargs['player'] = player
    kwargs['player_craft'] = player_craft
    kwargs['sortie_status'] = 'init'

    # create or update Sortie info
    sortie_upd(**kwargs)


def event_group(**kwargs):
    # group initialization event
    logger.debug('Event handler for [group initialization] is empty')
    pass


def event_game_object(**kwargs):
    if Mission_Object.objects.filter(mission=mission, object_id=kwargs['object_id'], object_name=kwargs['object_name'],
                                     name=kwargs['name']).exists():
        logger.info(f"Object [{kwargs['object_id']}] - exists in the DB")
        # return
    else:
        date_spawn = mission.date_start + timedelta(seconds=kwargs['tik'] // 50)
        game_date_spawn = mission.date_start + timedelta(seconds=kwargs['tik'] // 50)

        # Add object
        object = Mission_Object(mission=mission, object_id=kwargs['object_id'], parent_id=kwargs['parent_id'],
                                object_name=kwargs['object_name'], name=kwargs['name'],
                                country_id=kwargs['country_id'], tik=kwargs['tik'], date_spawn = date_spawn,
                                game_date_spawn=game_date_spawn)
        object.save()
    pass


def event_influence_area():
    pass


def event_influence_area_boundary():
    pass


def event_log_version(tik, version, atype_id):
    logger.debug('Event handler for [log version] is empty')
    pass


def event_bot_deinitialization(**kwargs):
    # data: {'tik': 47099, 'bot_id': 10242, 'pos': {'x': 104586.3828, 'y': 74.2299, 'z': 181501.5313}, 'atype_id': 16}
    # data: {'tik': 25490, 'bot_id': 11268, 'pos': {'x': 119496.0469, 'y': 55.8246, 'z': 156457.3438}, 'atype_id': 16}
    global mission
    """
    mission_obj = Mission_Object.objects.get(object_id=kwargs['bot_id'])
    # print(f"mission_obj.parent_id: {mission_obj.parent_id}")
    if mission_obj.parent_id is not None:
        mission_obj = Mission_Object.objects.get(object_id=mission_obj.parent_id)

    player_craft = Player_Craft.objects.get(mission_object_plane=mission_obj)
    """
    player_craft = Player_Craft.objects.get(bot_id=kwargs['bot_id'])
    kwargs['player_craft'] = player_craft

    player_upd(**kwargs)    # update player stats

    sortie = Sortie.objects.get(mission=mission, player_craft=player_craft)
    kwargs['sortie'] = sortie
    kwargs['sortie_status'] = 'bot_deinit'
    add_mission_event(**kwargs)


def event_pos_changed():
    pass


def event_bot_eject_leave(**kwargs):
    # data: {'tik': 46324, 'bot_id': 10242, 'parent_id': 9218, 'pos': {'x': 104485.0, 'y': 206.2197, 'z': 181687.125},
    #           'atype_id': 18}
    """
    pilot = Mission_Object.objects.get(object_id=kwargs['bot_id'])
    if pilot.parent_id is not None:
        pilot = Mission_Object.objects.get(object_id=pilot.parent_id)

    pilot = Player_Craft.objects.get(mission_object_plane=pilot)
    """
    pilots_plane = Player_Craft.objects.get(bot_id=kwargs['bot_id'])
    sortie = Sortie.objects.get(player_craft=pilots_plane)
    sortie.is_bailed = True
    sortie.save()

    kwargs['sortie'] = sortie
    kwargs['sortie_status'] = 'bailed'
    kwargs['player_craft'] = pilots_plane

    add_mission_event(**kwargs)


def event_round_end():
    pass


def event_player_connected(**kwargs):
    pass


# def event_player_disconnected(**kwargs):
def event_player_disconnected():
    # data: {'tik': 42561, 'account_id': '3ba2a5c1-6ac6-4f96-8bfb-963efe9906dd',
    #   'profile_id': '9bf9b219-95eb-4ea6-9d61-cfb0a3cc011f', 'atype_id': 21}
    """
    to check/update Sortie parameters:
    is_disco_after_damage = models.BooleanField(default=False)
    is_disco_after_damage = models.BooleanField(default=False)
    is_disco_in_flight = models.BooleanField(default=False)
    :return:
    """
    pass


def event_tank_travel():
    pass


event_handlers = (event_mission_start, event_hit, event_damage, event_kill, event_sortie_end, event_takeoff,
                  event_landing, event_mission_end, event_mission_result, event_airfield, event_player_plane,
                  event_group, event_game_object, event_influence_area, event_influence_area_boundary,
                  event_log_version, event_bot_deinitialization, event_pos_changed, event_bot_eject_leave,
                  event_round_end, event_player_connected, event_player_disconnected, event_tank_travel)


def check_mission(mis_name):
    global mission, tik_last

    time_zone = pytz.timezone(settings.MISSION_REPORT_TZ)
    mission_timestamp = int(time.mktime(time.strptime(mis_name, '%Y-%m-%d_%H-%M-%S')))

    #mission = Mission.objects.get(timestamp=mission_timestamp)
    #if mission:
    if Mission.objects.filter(timestamp=mission_timestamp).exists():
        logger.info(f"{mission_timestamp} - exists in the DB")
        mission = Mission.objects.get(timestamp=mission_timestamp)
    else:
        real_date = time_zone.localize(datetime.fromtimestamp(mission_timestamp))
        real_date = real_date.astimezone(pytz.UTC)

        # Add mission
        mission = Mission(name=mis_name, timestamp=mission_timestamp, date_start=real_date, date_end=real_date,
                          duration=0)
        mission.save()

        tik_last = 0

def proc_data(data):
    global tik_last

    # atype_id = parse_result.pop('atype_id')
    atype_id = data['atype_id']
    logger.debug(f"atype_id = {atype_id}")
    logger.debug(f"event_handlers[atype_id] = {event_handlers[atype_id]}")

    """if data['tik'] > tik_last:
        tik_last = data['tik']
    """
    event_handlers[atype_id](**data)