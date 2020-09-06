import sys
from constants import Coalition
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

try:
    from django.db import models
except  Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

# Sample User model
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)


# Mission log class
class Mission_Log(models.Model):
    name = models.CharField(max_length=25)
    miss_log_id = models.IntegerField(default=0, db_index=True)
    is_processed = models.BooleanField(default=False, editable=False)


# Mission class
class Mission(models.Model):
    timestamp = models.IntegerField(unique=True)
    name = models.CharField(max_length=256, blank=True, db_index=True)

    date_start = models.DateTimeField(db_index=True)
    date_end = models.DateTimeField()
    duration = models.IntegerField(default=0)
    game_date = models.DateTimeField(null=True, blank=True)


class Score(models.Model):
    SCORE_TYPE = (
        ('int', 'integer'),
        ('pct', 'percent'),
    )
    key = models.CharField(max_length=24, editable=False)
    type = models.CharField(max_length=3, choices=SCORE_TYPE, editable=False, default='int')
    value = models.IntegerField(default=0, editable=False)
    custom_value = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'scoring'
        ordering = ['key']
        verbose_name = _('score')
        verbose_name_plural = _('scoring')

    def __str__(self):
        return '{key} [{value}]'.format(key=self.key, value=self.get_value())

    def get_value(self):
        if self.custom_value is not None:
            return self.custom_value
        else:
            return self.value


class Object(models.Model):
    CLASSES = (
        ('aaa_heavy', 'aaa_heavy'),
        ('aaa_light', 'aaa_light'),
        ('aaa_mg', 'aaa_mg'),
        ('aerostat', 'aerostat'),
        ('aircraft_gunner', 'aircraft_gunner'),
        ('aircraft_heavy', 'aircraft_heavy'),
        ('aircraft_light', 'aircraft_light'),
        ('aircraft_medium', 'aircraft_medium'),
        ('aircraft_pilot', 'aircraft_pilot'),
        ('aircraft_static', 'aircraft_static'),
        ('aircraft_transport', 'aircraft_transport'),
        ('aircraft_turret', 'aircraft_turret'),
        ('armoured_vehicle', 'armoured_vehicle'),
        ('artillery_field', 'artillery_field'),
        ('artillery_howitzer', 'artillery_howitzer'),
        ('artillery_rocket', 'artillery_rocket'),
        ('block', 'block'),
        ('bomb', 'bomb'),
        ('building_big', 'building_big'),
        ('building_medium', 'building_medium'),
        ('building_small', 'building_small'),
        ('bullet', 'bullet'),
        ('car', 'car'),
        ('driver', 'driver'),
        ('explosion', 'explosion'),
        ('locomotive', 'locomotive'),
        ('machine_gunner', 'machine_gunner'),
        ('parachute', 'parachute'),
        ('rocket', 'rocket'),
        ('searchlight', 'searchlight'),
        ('ship', 'ship'),
        ('ship_heavy', 'ship_heavy'),
        ('ship_light', 'ship_light'),
        ('ship_medium', 'ship_medium'),
        ('shell', 'shell'),
        ('tank_heavy', 'tank_heavy'),
        ('tank_light', 'tank_light'),
        ('tank_medium', 'tank_medium'),
        ('tank_driver', 'tank_driver'),
        ('tank_turret', 'tank_turret'),
        ('trash', 'trash'),
        ('truck', 'truck'),
        ('vehicle_crew', 'vehicle_crew'),
        ('vehicle_static', 'vehicle_static'),
        ('vehicle_turret', 'vehicle_turret'),
        ('wagon', 'wagon'),
    )
    CLASSES_BASE = (
        ('aircraft', 'aircraft'),
        ('ammo', 'ammo'),
        ('block', 'block'),
        ('crew', 'crew'),
        ('turret', 'turret'),
        ('vehicle', 'vehicle'),
    )

    name = models.CharField(max_length=64, blank=True)
    name_en = models.CharField(max_length=64, blank=True)
    name_ru = models.CharField(max_length=64, blank=True)
    log_name = models.CharField(max_length=64, editable=False, unique=True)
    cls_base = models.CharField(choices=CLASSES_BASE, max_length=24, blank=True)
    cls = models.CharField(choices=CLASSES, max_length=24, blank=True)
    score = models.ForeignKey(Score, on_delete=models.CASCADE)
    is_playable = models.BooleanField(default=False, editable=False)

    class Meta:
        db_table = 'objects'
        ordering = ['name']
        verbose_name = _('object')
        verbose_name_plural = _('objects')

    def __str__(self):
        return self.name

    def aircraft_image(self):
        return static('img/aircraft/{log_name}.png'.format(log_name=self.log_name))


class Profile(models.Model):
    uuid = models.UUIDField(unique=True, editable=False)
    nickname = models.CharField(max_length=128, db_index=True)

    # user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile',
    #                            blank=True, null=True, on_delete=models.SET_NULL)
    # squad = models.ForeignKey('squads.Squad', related_name='+', blank=True, null=True, on_delete=models.SET_NULL)
    is_hide = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ['-id']
        db_table = 'profiles'
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return self.nickname

    """def get_nicknames(self, exclude_current=True):
        nicknames = set(Sortie.objects.filter(profile_id=self.id)
                        .distinct('nickname').values_list('nickname', flat=True).order_by())
        if exclude_current:
            nicknames.discard(self.nickname)
        return nicknames
    """

    def uuid_sha256_hash(self):
        return hashlib.sha256(self.uuid.hex.encode('utf8')).hexdigest()

    """def connect_with_user(self, user):
        self.user = user
        if hasattr(user, 'squad_member'):
            self.squad = user.squad_member.squad
        self.save()
    """


class Player(models.Model):
    """
    'profile_id': '9bf9b219-95eb-4ea6-9d61-cfb0a3cc011f',
    'account_id': '3ba2a5c1-6ac6-4f96-8bfb-963efe9906dd',
    'name': '-DED-Zlodey',
    """
    account_id = models.CharField(max_length=40, null=True, db_index=True)
    profile_id = models.CharField(max_length=40, null=True, db_index=True)
    name = models.CharField(max_length=128, null=True, db_index=True)

    # tour = models.ForeignKey(Tour, related_name='+', on_delete=models.CASCADE)
    """
    PLAYER_TYPES = (
        ('pilot', 'pilot'),
        ('gunner', 'gunner'),
        ('tankman', 'tankman'),
    )

    type = models.CharField(choices=PLAYER_TYPES, max_length=8, default='pilot', db_index=True)
    """
    # profile = models.ForeignKey(Profile, related_name='players', on_delete=models.CASCADE)
    # squad = models.ForeignKey('stats.Squad', related_name='players', blank=True, null=True, on_delete=models.SET_NULL)

    date_first_sortie = models.DateTimeField(null=True)
    date_last_sortie = models.DateTimeField(null=True)
    date_last_combat = models.DateTimeField(null=True)

    score = models.BigIntegerField(default=0, db_index=True)
    rating = models.BigIntegerField(default=0, db_index=True)
    ratio = models.FloatField(default=1)

    sorties_total = models.IntegerField(default=0)
    # sorties_coal = ArrayField(models.IntegerField(default=0), default=default_coal_list)
    # sorties_cls = JSONField(default=default_sorties_cls)

    """COALITIONS = (
        (Coalition.neutral, pgettext_lazy('coalition', _('neutral'))),
        (Coalition.coal_1, settings.COAL_1_NAME),
        (Coalition.coal_2, settings.COAL_2_NAME),
    )

    coal_pref = models.IntegerField(default=Coalition.neutral, choices=COALITIONS)
    """

    """
    # налет в секундах?
    flight_time = models.BigIntegerField(default=0, db_index=True)

    # ammo = JSONField(default=default_ammo)
    accuracy = models.FloatField(default=0, db_index=True)

    streak_current = models.IntegerField(default=0, db_index=True)
    streak_max = models.IntegerField(default=0)

    score_streak_current = models.IntegerField(default=0, db_index=True)
    score_streak_max = models.IntegerField(default=0)

    streak_ground_current = models.IntegerField(default=0, db_index=True)
    streak_ground_max = models.IntegerField(default=0)

    sorties_streak_current = models.IntegerField(default=0)
    sorties_streak_max = models.IntegerField(default=0)

    ft_streak_current = models.IntegerField(default=0)
    ft_streak_max = models.IntegerField(default=0)

    sortie_max_ak = models.IntegerField(default=0)
    sortie_max_gk = models.IntegerField(default=0)

    lost_aircraft_current = models.IntegerField(default=0)

    bailout = models.IntegerField(default=0)
    wounded = models.IntegerField(default=0)
    dead = models.IntegerField(default=0)
    captured = models.IntegerField(default=0)
    relive = models.IntegerField(default=0)

    takeoff = models.IntegerField(default=0)
    landed = models.IntegerField(default=0)
    ditched = models.IntegerField(default=0)
    crashed = models.IntegerField(default=0)
    in_flight = models.IntegerField(default=0)
    shotdown = models.IntegerField(default=0)

    respawn = models.IntegerField(default=0)
    disco = models.IntegerField(default=0)

    ak_total = models.IntegerField(default=0, db_index=True)
    ak_assist = models.IntegerField(default=0)
    gk_total = models.IntegerField(default=0, db_index=True)
    fak_total = models.IntegerField(default=0)
    fgk_total = models.IntegerField(default=0)

    # killboard_pvp = JSONField(default=dict)
    # killboard_pve = JSONField(default=dict)

    ce = models.FloatField(default=0)
    kd = models.FloatField(default=0, db_index=True)
    kl = models.FloatField(default=0)
    ks = models.FloatField(default=0)
    khr = models.FloatField(default=0, db_index=True)
    gkd = models.FloatField(default=0)
    gkl = models.FloatField(default=0)
    gks = models.FloatField(default=0)
    gkhr = models.FloatField(default=0)
    wl = models.FloatField(default=0)
    elo = models.FloatField(default=1000)

    fairplay = models.IntegerField(default=100)
    fairplay_time = models.IntegerField(default=0)

    objects = models.Manager()
    # players = PlayerManager()

    class Meta:
        ordering = ['-id']
        db_table = 'players'
        # unique_together = (('profile', 'type', 'tour'),)
        unique_together = (('profile', 'type'),)

    def __str__(self):
        return self.profile.nickname

    def save(self, *args, **kwargs):
        self.update_accuracy()
        self.update_analytics()
        self.update_rating()
        self.update_ratio()
        self.update_coal_pref()
        super().save(*args, **kwargs)

    def get_profile_url(self):
        url = '{url}?tour={tour_id}'.format(url=reverse('stats:pilot', args=[self.profile_id, self.nickname]),
                                            tour_id=self.tour_id)
        return url

    def get_sorties_url(self):
        url = '{url}?tour={tour_id}'.format(url=reverse('stats:pilot_sorties', args=[self.profile_id, self.nickname]),
                                            tour_id=self.tour_id)
        return url

    def get_vlifes_url(self):
        url = '{url}?tour={tour_id}'.format(url=reverse('stats:pilot_vlifes', args=[self.profile_id, self.nickname]),
                                            tour_id=self.tour_id)
        return url

    def get_awards_url(self):
        url = '{url}?tour={tour_id}'.format(url=reverse('stats:pilot_awards', args=[self.profile_id, self.nickname]),
                                            tour_id=self.tour_id)
        return url

    def get_killboard_url(self):
        url = '{url}?tour={tour_id}'.format(url=reverse('stats:pilot_killboard', args=[self.profile_id, self.nickname]),
                                            tour_id=self.tour_id)
        return url

    def get_position_by_field(self, field='rating'):
        return get_position_by_field(player=self, field=field)

    @property
    def nickname(self):
        return self.profile.nickname

    @property
    def lost_aircraft(self):
        return self.ditched + self.crashed + self.shotdown

    @property
    def not_takeoff(self):
        return self.sorties_total - self.takeoff

    @property
    def flight_time_hours(self):
        return self.flight_time / 3600

    @property
    def rating_format(self):
        if self.rating > 10000:
            return '{}K'.format(self.rating // 1000)
        else:
            return self.rating

    @property
    def ak_total_ai(self):
        aircraft_light = self.killboard_pve.get('aircraft_light', 0)
        aircraft_medium = self.killboard_pve.get('aircraft_medium', 0)
        aircraft_heavy = self.killboard_pve.get('aircraft_heavy', 0)
        aircraft_transport = self.killboard_pve.get('aircraft_transport', 0)
        return aircraft_light + aircraft_medium + aircraft_heavy + aircraft_transport

    def update_accuracy(self):
        if self.ammo['used_cartridges']:
            self.accuracy = round(self.ammo['hit_bullets'] * 100 / self.ammo['used_cartridges'], 1)

    def update_analytics(self):
        self.kd = round(self.ak_total / max(self.relive, 1), 2)
        self.kl = round(self.ak_total / max(self.lost_aircraft, 1), 2)
        self.ks = round(self.ak_total / max(self.sorties_total, 1), 2)
        self.khr = round(self.ak_total / max(self.flight_time_hours, 1), 2)
        self.gkd = round(self.gk_total / max(self.relive, 1), 2)
        self.gkl = round(self.gk_total / max(self.lost_aircraft, 1), 2)
        self.gks = round(self.gk_total / max(self.sorties_total, 1), 2)
        self.gkhr = round(self.gk_total / max(self.flight_time_hours, 1), 2)
        self.wl = round(self.ak_total / max(self.shotdown, 1), 2)
        self.ce = round(self.kl * self.khr / 10, 2)

    def update_rating(self):
        # score per death
        sd = self.score / max(self.relive, 1)
        # score per hour
        shr = self.score / max(self.flight_time_hours, 1)
        # self.rating = int((sd * shr * self.score) / 1000000)
        self.rating = int((sd * shr * self.score) / 1000)

    def update_ratio(self):
        ratio = Sortie.objects.filter(player_id=self.id).aggregate(ratio=Avg('ratio'))['ratio']
        if ratio:
            self.ratio = round(ratio, 2)

    def update_coal_pref(self):
        if self.sorties_total:
            coal_1 = round(self.sorties_coal[1] * 100 / self.sorties_total, 0)
            if coal_1 > 60:
                self.coal_pref = 1
            elif coal_1 < 40:
                self.coal_pref = 2
            else:
                self.coal_pref = 0
    """


class Mission_Object(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    # object_id = models.IntegerField(unique=True)
    object_id = models.IntegerField()
    object_name = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    country_id = models.IntegerField()
    tik = models.IntegerField()
    date_spawn = models.DateTimeField(blank=True, null=True)
    game_date_spawn = models.DateTimeField(blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True) # self.object_id


class Airfield(models.Model):
    # mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    airfield_id = models.IntegerField(unique=True)
    # country_id = models.IntegerField()
    pos_x = models.FloatField(blank=True, null=True)
    pos_y = models.FloatField(blank=True, null=True)
    pos_z = models.FloatField(blank=True, null=True)


class Airfield_Mission(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    airfield = models.ForeignKey(Airfield, on_delete=models.CASCADE)
    country_id = models.IntegerField()
    tik = models.IntegerField()


class Player_Craft(models.Model):
    mission_object_plane = models.ForeignKey(Mission_Object, on_delete=models.CASCADE)
    # mission_object_bot = models.ForeignKey(Mission_Object, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    # mission_object = models.IntegerField(blank=True, null=True)
    # player = models.IntegerField(blank=True, null=True)
    airfield = models.IntegerField(blank=True, null=True)

    pos_x = models.FloatField(blank=True, null=True)
    pos_y = models.FloatField(blank=True, null=True)
    pos_z = models.FloatField(blank=True, null=True)

    bot_id = models.IntegerField(blank=True, null=True)
    cartridges = models.IntegerField(blank=True, null=True)
    shells = models.IntegerField(blank=True, null=True)
    bombs = models.IntegerField(blank=True, null=True)
    rockets = models.IntegerField(blank=True, null=True)
    form = models.CharField(max_length=128)
    airstart = models.BooleanField()
    is_pilot = models.BooleanField()
    payload_id = models.IntegerField(blank=True, null=True)
    fuel = models.IntegerField(blank=True, null=True)
    skin = models.CharField(max_length=128)


class Sortie(models.Model):
    # nickname = models.CharField(max_length=128)
    tik = models.IntegerField(blank=True, null=True)

    player = models.ForeignKey(Player, related_name='sorties_list', on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, related_name='sorties_list', on_delete=models.CASCADE)
    player_craft = models.ForeignKey(Player_Craft, on_delete=models.CASCADE)

    type = (
        ('Pilot', 'plane pilot'),
        ('Gunner', 'plane gunner'),
        ('Tankman', 'tank player'),
        ('Tank_Gunner', 'Tank_Gunner'))

    player_role = models.CharField(max_length=25, choices=type, editable=False, default='Pilot')

    date_start = models.DateTimeField(blank=True, null=True)
    # TODO rework date_start since it is the same as Mission_Object.date_spawn
    date_end = models.DateTimeField(blank=True, null=True)
    date_takeoff = models.DateTimeField(blank=True, null=True)
    date_land = models.DateTimeField(blank=True, null=True)

    flight_time = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)

    is_alive = models.BooleanField(default=True)
    is_bailed = models.BooleanField(default=False)
    is_destroyed = models.BooleanField(default=False)
    is_disco_after_damage = models.BooleanField(default=False)
    is_disco_in_flight = models.BooleanField(default=False)
    is_in_flight = models.BooleanField(default=False)
    plane_damage = models.FloatField(default=0)
    pilot_damage = models.FloatField(default=0)
    hits = models.IntegerField(default=0)
    kills = models.IntegerField(default=0)
    hits_friend = models.IntegerField(default=0)
    kills_friend = models.IntegerField(default=0)

    # mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    # profile = models.ForeignKey(Profile, related_name='+', on_delete=models.CASCADE)
    # tour = models.ForeignKey(Tour, related_name='sorties', on_delete=models.CASCADE)
    # vlife = models.ForeignKey(VLife, related_name='sorties_list', on_delete=models.CASCADE, blank=True, null=True)
    """
    # parent = models.ForeignKey('self', related_name='children', blank=True, null=True, on_delete=models.PROTECT)

    aircraft = models.ForeignKey(Object, related_name='+', on_delete=models.PROTECT)

    fuel = models.IntegerField(default=100)  # в процентах!
    skin = models.CharField(max_length=256, blank=True)
    payload_id = models.IntegerField(default=0)
    weapon_mods_id = ArrayField(models.IntegerField(), default=list)
    """


# Mission Events class
class Mission_Event(models.Model):
    # name = models.CharField(max_length=256, blank=True, db_index=True)

    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    sortie = models.ForeignKey(Sortie, blank=True, null=True, on_delete=models.CASCADE)
    tik = models.IntegerField(blank=True, null=True, db_index=True)
    player = models.ForeignKey(Player, blank=True, null=True, on_delete=models.CASCADE)
    player_craft = models.ForeignKey(Player_Craft, blank=True, null=True, on_delete=models.CASCADE)
    # target = models.ForeignKey(Mission_Object, blank=True, null=True, on_delete=models.CASCADE)

    account_id = models.CharField(max_length=40, null=True, db_index=True)
    profile_id = models.CharField(max_length=40, null=True, db_index=True)

    area_id = models.IntegerField(blank=True, null=True)
    atype_id = models.IntegerField(blank=True, null=True)
    airfield_id = models.IntegerField(blank=True, null=True)
    aircraft_id = models.IntegerField(blank=True, null=True)
    attacker_id = models.IntegerField(blank=True, null=True)
    bot_id = models.IntegerField(blank=True, null=True)
    coal_id = models.IntegerField(blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    icon_type_id = models.IntegerField(blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    # members_id = models.IntegerField(blank=True, null=True)
    leader_id = models.IntegerField(blank=True, null=True)
    object_id = models.IntegerField(blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    payload_id = models.IntegerField(blank=True, null=True)
    target_id = models.IntegerField(blank=True, null=True)
    task_type_id = models.IntegerField(blank=True, null=True)

    ammo = sortie_status = models.CharField(max_length=40, blank=True, null=True)
    aircraft_name = models.CharField(max_length=128, blank=True, null=True)
    airstart = models.BooleanField(default=False)
    bombs = models.IntegerField(blank=True, null=True)
    cartridges = models.IntegerField(blank=True, null=True)
    damage = models.FloatField(blank=True, null=True)
    form = models.CharField(max_length=128, blank=True, null=True)
    fuel = models.IntegerField(blank=True, null=True)
    is_pilot = models.BooleanField(default=False)
    is_tracking_stat = models.BooleanField(default=False)
    name = models.CharField(max_length=128, blank=True, null=True)
    object_name = models.CharField(max_length=128, blank=True, null=True)
    rockets = models.IntegerField(blank=True, null=True)
    shells = models.IntegerField(blank=True, null=True)
    skin = models.CharField(max_length=128, blank=True, null=True)
    sortie_status = models.CharField(max_length=40, blank=True, null=True)
    success = models.IntegerField(blank=True, null=True)
    weapon_mods_id = models.IntegerField(blank=True, null=True)
    enabled = models.BooleanField(default=False)
    in_air = models.IntegerField(blank=True, null=True)
    friendly_fire = models.BooleanField(default=False)
    # boundary = models.IntegerField(blank=True, null=True)


    pos_x = models.FloatField(blank=True, null=True)
    pos_y = models.FloatField(blank=True, null=True)
    pos_z = models.FloatField(blank=True, null=True)

    # timestamp = models.IntegerField(unique=True)
    # data = models.JSONField(default=dict)


class Mission_Objective(models.Model):
    #{'tik': 1105, 'object_id': 64137, 'pos': {'x': 118595.8047, 'y': 67.232, 'z': 227313.5625}, 'coal_id': 1,
    #       'task_type_id': 14, 'success': True, 'icon_type_id': None, 'atype_id': 8}
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    coal = models.IntegerField()
    object = models.IntegerField()
    task_type = models.IntegerField()
    tik = models.IntegerField(blank=True, null=True, db_index=True)
    icon_type_id = models.IntegerField(blank=True, null=True)

    pos_x = models.FloatField(blank=True, null=True)
    pos_y = models.FloatField(blank=True, null=True)
    pos_z = models.FloatField(blank=True, null=True)

    success = models.BooleanField(default=False)


class Kill(models.Model):
    tik = models.IntegerField(blank=True, null=True)

    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='attacker_player')
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    sortie = models.ForeignKey(Sortie, on_delete=models.CASCADE)
    target = models.ForeignKey(Mission_Object, on_delete=models.CASCADE)

    """pos_x = models.FloatField(blank=True, null=True)
    pos_y = models.FloatField(blank=True, null=True)
    pos_z = models.FloatField(blank=True, null=True)"""

    target_object_name = models.CharField(max_length=128, blank=True, null=True)
    target_is_player = models.BooleanField(default=False)
    target_is_friend = models.BooleanField(default=False)
    target_is_kill = models.BooleanField(default=False)
    target_damage = models.FloatField(default=0.0)
    target_player = models.ForeignKey(Player, on_delete=models.CASCADE, blank=True, null=True, related_name='target_player')
    target_kill_share = models.FloatField(blank=True, null=True)    # share in % for this kill
    target_was_killed = models.BooleanField(default=False)
