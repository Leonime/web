from rest_framework import serializers

from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    follower_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    chirp_count = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    thumbnail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'id',
            'bio',
            'location',
            'follower_count',
            'following_count',
            'chirp_count',
            'is_following',
            'username',
            'image',
            'thumbnail',
        ]

    def get_image(self, obj):
        if obj.image:
            return obj.image.url

    def get_thumbnail(self, obj):
        if obj.image:
            return obj.image.thumbnails.large.url if obj.image else None

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_username(self, obj):
        return obj.user.username

    def get_following_count(self, obj):
        if hasattr(obj, 'user__following__count'):
            return obj.user__following__count
        else:
            return obj.user.following.count()

    def get_follower_count(self, obj):
        if hasattr(obj, 'followers__count'):
            return obj.followers__count
        else:
            return obj.followers.count()

    def get_chirp_count(self, obj):
        if hasattr(obj, 'user__chirp__count'):
            return obj.user__chirp__count
        else:
            return obj.user.chirp_set.count()

    def get_is_following(self, obj):
        is_following = False
        context = self.context
        request = context.get('request')
        if request:
            user = request.user
            is_following = user in obj.followers.all()
        return is_following
