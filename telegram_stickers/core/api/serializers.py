from rest_framework import serializers

from core.models import Sticker, StickerPack


class StickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sticker
        fields = (
            'preview',
        )


class StickerPackSerializer(serializers.ModelSerializer):
    stickers = StickerSerializer(many=True, read_only=True)

    class Meta:
        model = StickerPack
        fields = (
            'name',
            'category',
            'tme_url',
            'thumbnail',
            'is_animated',
            'installs',
            'stickers',
        )
