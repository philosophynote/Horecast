# Generated by Django 3.2.5 on 2021-09-18 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Horse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race_id', models.TextField(blank=True, null=True)),
                ('horse_id', models.TextField(blank=True, null=True)),
                ('frame_number', models.BigIntegerField(blank=True, null=True)),
                ('horse_number', models.BigIntegerField(blank=True, null=True)),
                ('horse_name', models.TextField(blank=True, null=True)),
                ('sex_age', models.TextField(blank=True, null=True)),
                ('jockey_name', models.TextField(blank=True, null=True)),
                ('jockey_weight', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'horse',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Predict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.BigIntegerField(blank=True, null=True)),
                ('race_id', models.TextField(blank=True, null=True)),
                ('horse_number', models.BigIntegerField(blank=True, null=True)),
                ('pred', models.BigIntegerField(blank=True, null=True)),
                ('favorite', models.BigIntegerField(blank=True, null=True)),
                ('bet', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'predict',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race_id', models.TextField(blank=True, null=True)),
                ('race_park', models.TextField(blank=True, null=True)),
                ('race_name', models.TextField(blank=True, null=True)),
                ('race_number', models.TextField(blank=True, null=True)),
                ('race_date', models.TextField(blank=True, null=True)),
                ('race_turn', models.TextField(blank=True, null=True)),
                ('course_len', models.BigIntegerField(blank=True, null=True)),
                ('weather', models.TextField(blank=True, null=True)),
                ('race_type', models.TextField(blank=True, null=True)),
                ('race_condition', models.TextField(blank=True, null=True)),
                ('n_horses', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'race',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race_id', models.TextField(blank=True, null=True)),
                ('rank', models.TextField(blank=True, null=True)),
                ('horse_number', models.TextField(blank=True, null=True)),
                ('favorite', models.TextField(blank=True, null=True)),
                ('odds', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'result',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sanrenpuku',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race_id', models.TextField(blank=True, null=True)),
                ('win_1', models.BigIntegerField(blank=True, null=True)),
                ('win_2', models.BigIntegerField(blank=True, null=True)),
                ('win_3', models.BigIntegerField(blank=True, null=True)),
                ('return_field', models.BigIntegerField(blank=True, db_column='return', null=True)),
            ],
            options={
                'db_table': 'sanrenpuku',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sanrentan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race_id', models.TextField(blank=True, null=True)),
                ('win_1', models.BigIntegerField(blank=True, null=True)),
                ('win_2', models.BigIntegerField(blank=True, null=True)),
                ('win_3', models.BigIntegerField(blank=True, null=True)),
                ('return_field', models.BigIntegerField(blank=True, db_column='return', null=True)),
            ],
            options={
                'db_table': 'sanrentan',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Umaren',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race_id', models.TextField(blank=True, null=True)),
                ('win_1', models.BigIntegerField(blank=True, null=True)),
                ('win_2', models.BigIntegerField(blank=True, null=True)),
                ('return_field', models.BigIntegerField(blank=True, db_column='return', null=True)),
            ],
            options={
                'db_table': 'umaren',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Umatan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race_id', models.TextField(blank=True, null=True)),
                ('win_1', models.BigIntegerField(blank=True, null=True)),
                ('win_2', models.BigIntegerField(blank=True, null=True)),
                ('return_field', models.BigIntegerField(blank=True, db_column='return', null=True)),
            ],
            options={
                'db_table': 'umatan',
                'managed': False,
            },
        ),
    ]
