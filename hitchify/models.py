from django.contrib.auth.models import User
from django.db import models
from django.db import connection
from django.db.models.signals import post_save
from django.dispatch import receiver


class MyUser(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # base_user = models.IntegerField(default=-1)
    base_user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20)
    birth_date = models.DateField()
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         MyUser.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.myuser.save()

    class Meta:
        managed = True
        db_table = 'myuser'


class Country(models.Model):
    country_name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=1500)
    national_currency = models.CharField(max_length=255)
    hitchrating = models.FloatField(blank=True, null=True)

    @property
    def loyal_users(self):
        with connection.cursor() as cursor:
            cursor.execute('SELECT username '
                           'FROM auth_user '
                           'WHERE NOT EXISTS (SELECT * '
                                             'FROM country INNER JOIN '
                                             'forum_post ON country.id = forum_post.country_id '
                                             'WHERE country.id = %s '
                                             'AND NOT EXISTS (SELECT * '
                                                             'FROM comment '
                                                             'WHERE comment.user_id = auth_user.id AND comment.post_id = forum_post.id ))',
                           [self.id])

            loyalists = cursor.fetchall()
            return loyalists

    @property
    def expert_users(self):
        with connection.cursor() as cursor:
            cursor.execute('SELECT auth_user.username, country.country_name, COUNT(hitchspot.id) AS spots ' 
                           'FROM ((auth_user INNER JOIN hitchspot ON auth_user.id = hitchspot.user_id) ' 
                           'INNER JOIN country ON country.id = hitchspot.country_id) ' 
                           'INNER JOIN forum_post ON forum_post.user_id = auth_user.id '
                           'WHERE country.id = %s '
                           'GROUP BY auth_user.username, country.country_name '
                           'HAVING COUNT(hitchspot.id)>=2;', [self.id])
            experts = cursor.fetchall()
            return experts
        
    @property
    def most_active_user(self):
        with connection.cursor() as cursor:
            cursor.execute('SELECT auth_user.username, COUNT(forum_post.user_id) AS posted_last_week '
                           'FROM forum_post INNER JOIN auth_user ON auth_user.id = forum_post.user_id '
                           'WHERE forum_post.country_id = %s '
                           'GROUP BY forum_post.user_id, auth_user.username '
                           'HAVING COUNT (forum_post.user_id)=( '
                           'SELECT MAX(mycount) '
                           'FROM (SELECT user_id,COUNT(forum_post.user_id) AS mycount '
                           'FROM forum_post '
                           'WHERE creation_date > current_date - interval \'7 days\' '
                           'GROUP BY user_id) AS auxTable );', [self.id])
            most_active_user = cursor.fetchall()
        return most_active_user

    @property
    def languages(self):
        res_languages = Language.objects.raw('SELECT id, language_name '
                                             'FROM language '
                                             'WHERE id IN (SELECT id '
                                             'FROM language_to_country '
                                             'WHERE country_id = %s)', [self.id])
        res_languages_list = []
        for lang in res_languages:
            res_languages_list.append(lang.language_name)

        return res_languages_list

    @property
    def hitchspots(self):
        res_hitchspots = Hitchspot.objects.raw('SELECT * '
                                               'FROM hitchspot '
                                               'WHERE country_id = %s', [self.id])
        res_hitchspots_list = []
        for spot in res_hitchspots:
            res_hitchspots_list.append(spot)
        return res_hitchspots_list

    @property
    def forum_posts(self):
        res_forum_posts = ForumPost.objects.raw(
            'SELECT * '
            'FROM forum_post '
            'INNER JOIN auth_user ON forum_post.user_id = auth_user.id '
            'WHERE country_id = %s', [self.id])
        res_forum_posts = list(res_forum_posts)
        return res_forum_posts

    class Meta:
        managed = True
        db_table = 'country'


class ForumPost(models.Model):
    title = models.CharField(max_length=255)
    body_text = models.TextField()
    likes = models.IntegerField(blank=True, null=True, default=0)
    creation_date = models.DateField(auto_now_add=True)
    last_update = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    country = models.ForeignKey(Country, models.DO_NOTHING)

    @property
    def photos(self):
        with connection.cursor() as cursor:
            cursor.execute('SELECT * '
                           'FROM photo '
                           'WHERE post_id = %s', [self.id])
            photos = cursor.fetchall()
            return photos

    @property
    def comments(self):
        res_comments = Comment.objects.raw('SELECT * '
                                           'FROM comment '
                                           'WHERE parent_comment_id IS NULL AND post_id = %s', [self.id])
        res_comments_list = []
        for comment in res_comments:
            res_comments_list.append(comment)

        return res_comments_list

        # with connection.cursor() as cursor:
        #     cursor.execute('SELECT * '
        #                    'FROM comment '
        #                    'WHERE post_id = %s ', [self.id])
        #     comments = cursor.fetchall()
        #     print(comments)
        #     return comments

    class Meta:
        managed = True
        db_table = 'forum_post'


class Guide(models.Model):
    title = models.CharField(max_length=255)
    body_text = models.TextField()
    short_summary = models.TextField(blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING)

    @property
    def top_contributors(self):
        with connection.cursor() as cursor:
            cursor.execute('SELECT auth_user.username '
                           'FROM guide_feedback INNER JOIN auth_user on auth_user.id = guide_feedback.user_id '
                           'GROUP BY guide_feedback.user_id, auth_user.username '
                           'HAVING COUNT(guide_feedback.user_id) = (SELECT MAX(mycount)'
                           'FROM (SELECT guide_feedback.user_id, COUNT(guide_feedback.user_id) AS mycount '
                           'FROM guide_feedback '
                           'WHERE guide_id = %s '
                           'GROUP BY guide_feedback.user_id) AS bruh1)',
                           [self.id])
            top_contributor = cursor.fetchall()
            print(top_contributor)
            return top_contributor

    class Meta:
        managed = True
        db_table = 'guide'


class GuideFeedback(models.Model):
    title = models.CharField(max_length=255)
    suggestion_text = models.TextField()
    guide = models.ForeignKey(Guide, models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'guide_feedback'


class Hitchspot(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(blank=True, null=True)
    avg_hitchability = models.FloatField()
    avg_waiting_time = models.FloatField()
    creation_date = models.DateField(auto_now_add=True)
    last_update = models.DateField(blank=True, null=True)
    country = models.ForeignKey(Country, models.DO_NOTHING)
    #user = models.ForeignKey(MyUser, models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)

    @property
    def comments(self):
        res_comments = Comment.objects.raw('SELECT * '
                                           'FROM comment '
                                           'WHERE parent_comment_id IS NULL AND spot_id = %s', [self.id])
        res_comments_list = []
        for comment in res_comments:
            res_comments_list.append(comment)

        return res_comments_list

    class Meta:
        managed = True
        db_table = 'hitchspot'


class Language(models.Model):
    language_name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'language'


class LanguageToCountry(models.Model):
    language = models.ForeignKey(Language, models.DO_NOTHING)
    country = models.ForeignKey(Country, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'language_to_country'
        unique_together = (('language', 'country'),)


class Photo(models.Model):
    # url = models.CharField(max_length=255)
    src_file = models.ImageField(upload_to='photos/', default='default.jpg')
    post = models.ForeignKey(ForumPost, models.DO_NOTHING, blank=True, null=True)
    spot = models.ForeignKey(Hitchspot, models.DO_NOTHING, blank=True, null=True)
    guide = models.ForeignKey(Guide, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'photo'


class SpotFeedback(models.Model):
    hitchability = models.IntegerField()
    waiting_time = models.IntegerField()
    spot = models.ForeignKey(Hitchspot, models.DO_NOTHING)
    # user = models.ForeignKey(MyUser, models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'spot_feedback'


class Comment(models.Model):
    body_text = models.TextField()
    likes = models.IntegerField(blank=True, null=True, default=0)
    creation_date = models.DateField(auto_now_add=True)
    last_update = models.DateField(blank=True, null=True)
    parent_comment = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True,
                                          related_name='child_comment')
    spot = models.ForeignKey(Hitchspot, models.DO_NOTHING, blank=True, null=True)
    post = models.ForeignKey(ForumPost, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING)

    @property
    def sub_comments(self):
        res_subcomments = Comment.objects.raw('SELECT * '
                                              'FROM comment '
                                              'WHERE parent_comment_id = %s', [self.id])
        res_subcomments_list = []
        for subcomment in res_subcomments:
            res_subcomments_list.append(subcomment)

        return res_subcomments_list

        # with connection.cursor() as cursor:
        #     cursor.execute('SELECT * '
        #                    'FROM comment '
        #                    'WHERE parent_comment_id = %s', [self.id])
        #     sub_comments = cursor.fetchall()
        # return sub_comments

    @property
    def author_username(self):
        with connection.cursor() as cursor:
            cursor.execute('SELECT username '
                           'FROM auth_user '
                           'WHERE id = %s', [self.user.id])
            author_usn = cursor.fetchone()
            # print(author_usn)
            return author_usn

    class Meta:
        managed = True
        db_table = 'comment'


class UserLikedComment(models.Model):
    # user = models.ForeignKey(MyUser, models.DO_NOTHING, primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    comment = models.ForeignKey(Comment, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'user_liked_comment'
        unique_together = (('user', 'comment'),)


class UserLikedForumPost(models.Model):
    # user = models.ForeignKey(MyUser, models.DO_NOTHING, primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    post = models.ForeignKey(ForumPost, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'user_liked_forum_post'
        unique_together = (('user', 'post'),)
