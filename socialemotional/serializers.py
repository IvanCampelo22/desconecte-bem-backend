from rest_framework import serializers
from .models import SocialMidiaUse

class SocialMidiaUseSerializers(serializers.ModelSerializer):
    class Meta:
        model = SocialMidiaUse
        fields = ['id', 'user', 'use_of_social_midia', 'social_media_comparison', 'selfknowledge_about_social_media_use', 'check_social_networks_when_offline', 'would_prefer_to_use_less_social_media']


class GetSocialMidiaUseSerializers(serializers.ModelSerializer):
    class Meta:
        model = SocialMidiaUse
        fields = ['id','user', 'use_of_social_midia', 'social_media_comparison', 'selfknowledge_about_social_media_use', 'check_social_networks_when_offline', 'would_prefer_to_use_less_social_media', 'result']


class SocialMidiaUseResultSerializers(serializers.ModelSerializer):
    class Meta:
        model = SocialMidiaUse
        fields = ('id', 'user', 'result')
        extra_kwargs = {
            'result': {'read_only': True},
            'user': {'read_only': True}
        }