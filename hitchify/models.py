# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
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
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Comment(models.Model):
    comment_id = models.IntegerField(primary_key=True)
    body_text = models.TextField()
    likes = models.IntegerField()
    creation_date = models.DateField()
    last_update = models.DateField(blank=True, null=True)
    parent_comment_id = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True, related_name='child_comment')
    spot = models.ForeignKey('Hitchspot', models.DO_NOTHING, blank=True, null=True)
    post = models.ForeignKey('ForumPost', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comment'


class Country(models.Model):
    country_id = models.IntegerField(primary_key=True)
    country_name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    national_currency = models.CharField(max_length=255)
    hitchrating = models.FloatField()

    class Meta:
        managed = False
        db_table = 'country'


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


class ForumPost(models.Model):
    post_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    body_text = models.TextField()
    likes = models.IntegerField(blank=True, null=True)
    creation_date = models.DateField()
    last_update = models.DateField(blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    country = models.ForeignKey(Country, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'forum_post'


class Guide(models.Model):
    guide_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    body_text = models.TextField()
    short_summary = models.TextField(blank=True, null=True)
    creation_date = models.DateField()
    update_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'guide'


class GuideFeedback(models.Model):
    gf_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    suggestion_text = models.TextField()
    guide = models.ForeignKey(Guide, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'guide_feedback'


class Hitchspot(models.Model):
    spot_id = models.IntegerField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(blank=True, null=True)
    avg_hitchability = models.FloatField()
    avg_waiting_time = models.FloatField()
    creation_date = models.DateField()
    last_update = models.DateField(blank=True, null=True)
    country = models.ForeignKey(Country, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'hitchspot'


class Language(models.Model):
    language_id = models.IntegerField(primary_key=True)
    language_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'language'


class LanguageToCountry(models.Model):
    language = models.ForeignKey(Language, models.DO_NOTHING, primary_key=True)
    country = models.ForeignKey(Country, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'language_to_country'
        unique_together = (('language', 'country'),)


class Photo(models.Model):
    photo_id = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=255)
    post = models.ForeignKey(ForumPost, models.DO_NOTHING, blank=True, null=True)
    spot = models.ForeignKey(Hitchspot, models.DO_NOTHING, blank=True, null=True)
    guide = models.ForeignKey(Guide, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'photo'


class SpotFeedback(models.Model):
    sf_id = models.IntegerField(primary_key=True)
    hitchability = models.IntegerField()
    waiting_time = models.IntegerField()
    spot = models.ForeignKey(Hitchspot, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'spot_feedback'


class UserLikedComment(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, primary_key=True)
    comment = models.ForeignKey(Comment, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_liked_comment'
        unique_together = (('user', 'comment'),)


class UserLikedForumPost(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, primary_key=True)
    post = models.ForeignKey(ForumPost, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_liked_forum_post'
        unique_together = (('user', 'post'),)


class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    role = models.SmallIntegerField()
    gender = models.SmallIntegerField()
    birth_date = models.DateTimeField()
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    date_of_reg = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'
