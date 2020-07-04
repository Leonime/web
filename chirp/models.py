from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from thumbnails import fields
from simple_history.models import HistoricalRecords


class ChirpLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chirp = models.ForeignKey("Chirp", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()


class ChirpQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username__iexact=username)

    def feed(self, user):
        profiles_exist = user.following.exists()
        followed_users_id = []
        if profiles_exist:
            followed_users_id = user.following.values_list("user__id", flat=True)
        return self.filter(
            Q(user__id__in=followed_users_id) | Q(user=user)
        ).distinct().order_by("-timestamp")


class ChirpManager(models.Manager):
    def get_queryset(self):
        return ChirpQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)


class Chirp(models.Model):
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, help_text='The parent chirp.')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                             help_text='Who is the owner of the chirp.')
    likes = models.ManyToManyField(User, related_name='chirp_user', blank=True, through=ChirpLike,
                                   help_text='It keeps a record on who likes the chirp.')
    content = models.TextField(blank=True, null=True, help_text='The content of the chirp.')
    image = fields.ImageField(upload_to='chirp/chirp/%Y/%m/%d/', max_length=1024, blank=True, null=True,
                              help_text='An image.')
    timestamp = models.DateTimeField(auto_now_add=True, help_text='The time when the chirp was created.')

    history = HistoricalRecords()

    objects = ChirpManager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.content}'

    @property
    def is_rechirp(self):
        return self.parent is not None
