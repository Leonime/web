from rest_framework import serializers

from chirp.models import Chirp
from codeshepherds.settings import CHIRP_ACTION_OPTIONS, MAX_CHIRP_LENGTH


class ChirpActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower().strip()
        if value not in CHIRP_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for tweets")
        return value


class ChirpCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Chirp
        fields = ['id', 'content', 'likes']

    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(value) > MAX_CHIRP_LENGTH:
            raise serializers.ValidationError("This chirp is too long")
        return value


class ChirpSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    parent = ChirpCreateSerializer(read_only=True)

    class Meta:
        model = Chirp
        fields = ['id', 'content', 'likes', 'is_rechirp', "parent"]

    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(value) > MAX_CHIRP_LENGTH:
            raise serializers.ValidationError("This chirp is too long")
        return value
