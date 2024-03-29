from django.db import models
from django.contrib.auth.models import User
import datetime

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Horse(models.Model):
    race_id = models.TextField(blank=True, null=True)
    horse_id = models.TextField(blank=True, null=True)
    frame_number = models.BigIntegerField(blank=True, null=True)
    horse_number = models.BigIntegerField(blank=True, null=True)
    horse_name = models.TextField(blank=True, null=True)
    sex_age = models.TextField(blank=True, null=True)
    jockey_name = models.TextField(blank=True, null=True)
    jockey_weight = models.FloatField(blank=True, null=True)
    id = models.CharField(primary_key=True, max_length=14)

    class Meta:
        db_table = 'horse'

    def __str__(self):
            return str(self.horse_number)+'.'+self.horse_name


class Predict(models.Model):
    race = models.ForeignKey('Race', models.DO_NOTHING, blank=True, null=True)
    horse_number = models.BigIntegerField(blank=True, null=True)
    pred = models.BigIntegerField(blank=True, null=True)
    center = models.BigIntegerField(blank=True, null=True)
    bet = models.BigIntegerField(blank=True, null=True)
    id = models.CharField(primary_key=True, max_length=14)

    class Meta:
        db_table = 'predict'


class Race(models.Model):
    SAPPORO = '札幌'
    HAKODATE = '函館'
    FUKUSHIMA = '福島'
    NIIGATA = '新潟'
    TOKYO = '東京'
    NAKAYAMA = '中山'
    CYUKYO = '中京'
    KYOTO = '京都'
    HANSHIN = '阪神'
    KOKURA = '小倉'
    RACE_PARK_CHOICES = [
        (SAPPORO, '札幌'),
        (HAKODATE, '函館'),
        (FUKUSHIMA, '福島'),
        (NIIGATA, '新潟'),
        (TOKYO, '東京'),
        (NAKAYAMA, '中山'),
        (CYUKYO, '中京'),
        (KYOTO, '京都'),
        (HANSHIN, '阪神'),
        (KOKURA, '小倉'),
    ]
    RACE_NUMBER_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
    ]
    race_id = models.TextField(primary_key=True)
    race_park = models.TextField(blank=True, null=True)
    race_name = models.TextField(blank=True, null=True)
    race_number = models.TextField(blank=True, null=True)
    race_date = models.TextField(blank=True, null=True)
    race_turn = models.TextField(blank=True, null=True)
    course_len = models.BigIntegerField(blank=True, null=True)
    weather = models.TextField(blank=True, null=True)
    race_type = models.TextField(blank=True, null=True)
    race_condition = models.TextField(blank=True, null=True)
    n_horses = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'race'

    def __str__(self):
        return self.race_id

    def response_race_date(self):
        return self.race_date
    
    def response_race_data(self):
        return self.race_park+self.race_number+"R　"+self.race_name

        


class Result(models.Model):
    race_id = models.TextField(blank=True, null=True)
    rank = models.TextField(blank=True, null=True)
    horse_number = models.TextField(blank=True, null=True)
    favorite = models.TextField(blank=True, null=True)
    odds = models.TextField(blank=True, null=True)
    id = models.CharField(primary_key=True, max_length=14)

    class Meta:
        db_table = 'result'


class Sanrenpuku(models.Model):
    race_id = models.TextField(primary_key=True)
    win_1 = models.BigIntegerField(blank=True, null=True)
    win_2 = models.BigIntegerField(blank=True, null=True)
    win_3 = models.BigIntegerField(blank=True, null=True)
    return_field = models.BigIntegerField(db_column='return', blank=True, null=True)  # Field renamed because it was a Python reserved word.

    class Meta:
        db_table = 'sanrenpuku'


class Sanrentan(models.Model):
    race_id = models.TextField(primary_key=True)
    win_1 = models.BigIntegerField(blank=True, null=True)
    win_2 = models.BigIntegerField(blank=True, null=True)
    win_3 = models.BigIntegerField(blank=True, null=True)
    return_1 = models.BigIntegerField(db_column='return', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    win_4 = models.BigIntegerField(blank=True, null=True)
    win_5 = models.BigIntegerField(blank=True, null=True)
    win_6 = models.BigIntegerField(blank=True, null=True)
    return_2 = models.BigIntegerField(blank=True, null=True)
    
    class Meta:
        db_table = 'sanrentan'


class Umaren(models.Model):
    race_id = models.TextField(primary_key=True)
    win_1 = models.BigIntegerField(blank=True, null=True)
    win_2 = models.BigIntegerField(blank=True, null=True)
    return_1 = models.BigIntegerField(db_column='return', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    win_3 = models.BigIntegerField(blank=True, null=True)
    win_4 = models.BigIntegerField(blank=True, null=True)
    return_2 = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'umaren'


class Umatan(models.Model):
    race_id = models.TextField(primary_key=True)
    win_1 = models.BigIntegerField(blank=True, null=True)
    win_2 = models.BigIntegerField(blank=True, null=True)
    return_1 = models.BigIntegerField(db_column='return', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    win_3 = models.BigIntegerField(blank=True, null=True)
    win_4 = models.BigIntegerField(blank=True, null=True)
    return_2 = models.BigIntegerField(blank=True, null=True)
    class Meta:
        db_table = 'umatan'

class BeforeComment(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User,on_delete=models.PROTECT,blank=True,db_column='author',)
    favorite_horse = models.CharField('軸馬',max_length=50, blank=True, null=True)
    longshot_horse_1 = models.CharField('紐馬１',max_length=50, blank=True, null=True)
    longshot_horse_2 = models.CharField('紐馬２',max_length=50, blank=True, null=True)
    longshot_horse_3 = models.CharField('紐馬３',max_length=50, blank=True, null=True)
    forecast_reason = models.TextField('予想理由', blank=True, null=True)
    race = models.ForeignKey('Race', models.DO_NOTHING, db_column='race', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'before_comment'

    def __str__(self):
        return str(self.id)
    
    def race_data(self):
        return self.race


class AfterComment(models.Model):
    id = models.BigAutoField(primary_key=True)
    after_comment = models.TextField('レース後感想',  blank=True, null=True)
    attention_horse = models.CharField('注目馬',max_length=50, blank=True, null=True)
    attention_reason = models.TextField('注目理由', blank=True, null=True)
    race = models.ForeignKey('Race', models.DO_NOTHING, db_column='race', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    comment = models.ForeignKey('BeforeComment', models.CASCADE, db_column='comment', blank=True, null=True)

    class Meta:
        db_table = 'after_comment'

    def __str__(self):
        return str(self.id)
