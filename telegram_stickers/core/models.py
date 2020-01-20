from django.db import models


class Sticker(models.Model):
    preview = models.ImageField(null=True, blank=True)
    sticker_pack = models.ForeignKey(to='core.StickerPack', on_delete=models.CASCADE, related_name='stickers')


class StickerPack(models.Model):
    name = models.CharField(max_length=128)
    category = models.CharField(max_length=128)
    thumbnail = models.ImageField(null=True, blank=True)
    is_animated = models.BooleanField(default=False)
    installs = models.PositiveIntegerField(default=0)
    tme_url = models.CharField(max_length=128)
