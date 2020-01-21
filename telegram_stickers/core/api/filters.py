import django_filters
from django_filters import rest_framework as filters

from core.models import StickerPack


class StickerPackFilter(filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = StickerPack
        fields = (
            'name',
            'category',
            'is_animated',
        )
